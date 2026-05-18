import streamlit as st
from openai import OpenAI
import base64
import json
from PIL import Image
import io


# ── CSS ──────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f0fff8 100%);
    }
    .block-container {
        max-width: 900px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    .main-header {
        text-align: center;
        padding: 2.5rem 0 0.5rem 0;
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #667eea, #a855f7, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
    }
    .sub-header {
        text-align: center;
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 2.5rem;
        letter-spacing: 0.5px;
    }
    .section-card {
        background: rgba(255,255,255,0.88);
        border-radius: 20px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 20px rgba(102,126,234,0.09);
        border: 1.5px solid rgba(102,126,234,0.12);
        backdrop-filter: blur(8px);
    }
    .section-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #4338ca;
        margin-bottom: 1.1rem;
    }
    .badge-req {
        display: inline-block;
        background: #ef4444;
        color: #fff;
        border-radius: 999px;
        padding: 1px 9px;
        font-size: 0.68rem;
        font-weight: 700;
        margin-left: 7px;
        vertical-align: middle;
    }
    .badge-opt {
        display: inline-block;
        background: #22c55e;
        color: #fff;
        border-radius: 999px;
        padding: 1px 9px;
        font-size: 0.68rem;
        font-weight: 700;
        margin-left: 7px;
        vertical-align: middle;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #a855f7 100%);
        color: white !important;
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2.5rem;
        font-size: 1.15rem;
        font-weight: 800;
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 5px 20px rgba(102,126,234,0.38);
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102,126,234,0.50);
    }
    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.7);
        border-radius: 14px;
        padding: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


# ── OpenAI 클라이언트 ────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ── 이미지 → base64 변환 ─────────────────────────────────────────────────────
def image_to_base64(uploaded_file) -> str:
    img = Image.open(uploaded_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


# ── GPT-4o 프롬프트 생성 ─────────────────────────────────────────────────────
def build_prompt(data: dict) -> tuple:
    has_images = bool(data.get("images"))
    has_budget = data.get("budget") is not None

    system = """당신은 척추·자세 교정 전문가이자 인체공학(에르고노믹스) 컨설턴트입니다.
사용자의 신체 정보와 불편 증상을 바탕으로 다음 순서로 **한국어**로 답변하세요.

[출력 형식 – 반드시 아래 JSON만 반환, 코드블록(```) 없이]
{
  "problems": "...",
  "photo_analysis": "...(사진 없으면 null)",
  "desk_chair_solution": {
    "recommended_chair_height_cm": 숫자,
    "recommended_desk_height_cm": 숫자,
    "explanation": "..."
  },
  "furniture_recommendation": [
    {
      "name": "...",
      "reason": "...",
      "price_approx": "...",
      "url": "..."
    }
  ],
  "furniture_note": "...(예산 초과 또는 조절만으로 해결 가능 시 설명)",
  "monitor_tips": "..."
}

규칙:
1. problems: 입력된 불편사항과 신체 데이터를 바탕으로 예상 문제점을 설명 (사진 있으면 사진 분석 반영)
2. photo_analysis: 사진이 있을 때만 거북목/디스크/골반전방경사/척추측만 등 자세 문제를 분석, 없으면 null
3. desk_chair_solution: 허벅지 길이·앉은키 데이터가 있으면 정밀 계산, 없으면 키 기반 표준 추정값 제공
   - 의자 높이 계산 기준: 허벅지 길이 또는 키×0.25
   - 책상 높이 계산 기준: 의자 높이 + 앉은키×0.45 또는 키×0.43 추정
4. furniture_recommendation:
   현재 책상/의자 높이가 권장 범위를 벗어나고 조절이 불가한 경우에만 추천.

   예산이 있을 때:
   - 반드시 예산 내 실제 한국 판매 제품 추천

   예산이 없을 때:
   - 일반적인 가격대 제품 추천

   URL 규칙:
   - 반드시 실제 제품 상세 페이지 URL만 반환
   - 절대 브랜드 메인 홈페이지 반환 금지
   - 절대 검색 결과 페이지 반환 금지
   - 절대 카테고리 페이지 반환 금지
   - 사용자가 클릭 시 바로 해당 상품 구매 페이지로 이동 가능해야 함

   잘못된 예시:
   - https://www.sidiz.com
   - https://www.ikea.com/kr
   - https://shopping.naver.com

   올바른 예시:
   - https://www.sidiz.com/product/detail/12345
   - https://www.ikea.com/kr/ko/p/product-name-30512345/

   존재하지 않는 URL을 추측해서 생성하지 마라.
   정확한 URL을 찾지 못하면 "url": "" 반환.

   예산 초과 시:
   - furniture_note에 이유 설명
   - furniture_recommendation은 빈 배열 반환
5. monitor_tips: 모니터 눈높이와 적정 거리(40~70cm) 관련 구체적 팁
6. 모든 URL은 실제 존재하는 링크만 반환해야 한다.
7. 확신이 없는 링크는 생성하지 말고 빈 문자열("") 반환.
8. 추천 제품은 사용자 상황에 따라 다양하게 선택한다. 같은 브랜드나 제품만 반복 추천하지 마라 사용자 예산과 증상에 따라 다른 제품을 추천한다.
"""

    lines = [
        "## 사용자 신체 정보",
        f"- 키: {data['height']} cm",
        f"- 몸무게: {data['weight']} kg",
        f"- 불편사항: {', '.join(data['complaints'])}",
    ]
    if data.get("other_complaint"):
        lines.append(f"- 기타 불편사항: {data['other_complaint']}")
    if data.get("thigh_len"):
        lines.append(f"- 허벅지 길이: {data['thigh_len']} cm")
    if data.get("desk_h"):
        lines.append(f"- 현재 책상 높이: {data['desk_h']} cm")
    if data.get("chair_h"):
        lines.append(f"- 현재 의자 높이: {data['chair_h']} cm")
    if data.get("sitting_h"):
        lines.append(f"- 앉은키: {data['sitting_h']} cm")
    if has_budget:
        lines.append(f"- 소지자금(가구 예산): {int(data['budget']):,}원")
    else:
        lines.append("- 소지자금: 미입력 (일반적인 가격대로 추천)")

    if has_images:
        lines.append("\n## 첨부 사진")
        lines.append("아래 사진을 분석하여 자세 문제를 파악하고, 허벅지 길이와 앉은키도 추정해 주세요.")

    user_text = "\n".join(lines)

    if has_images:
        content = [{"type": "text", "text": user_text}]
        for b64 in data["images"]:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{b64}",
                    "detail": "high"
                }
            })
    else:
        content = user_text

    return system, content


# ── GPT-4o 호출 ──────────────────────────────────────────────────────────────
def call_gpt(system: str, content) -> dict:
    client = get_client()
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": content},
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=1.0,
        max_tokens=2500,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


# ── 메인 show() ──────────────────────────────────────────────────────────────
def show():
    inject_css()

    # 페이지 설정
    st.set_page_config(
        page_title="척추요정 🧚",
        page_icon="🧚",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown('<div class="main-header">🧚 척추요정</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">당신의 자세를 분석하고, 맞춤 솔루션을 제안해 드려요</div>',
        unsafe_allow_html=True,
    )

    # ── 필수 입력 ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">📋 기본 정보 <span class="badge-req">필수</span></div>',
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("키 (cm)", min_value=100, max_value=250, value=170, step=1)
    with col2:
        weight = st.number_input("몸무게 (kg)", min_value=20, max_value=200, value=65, step=1)

    st.markdown("**불편사항** (해당하는 것 모두 선택)")
    complaint_options = [
        "목 통증", "허리 통증", "어깨 통증",
        "골반 통증", "무릎/발목 통증", "두통",
        "손목/팔 저림", "눈 피로", "기타",
    ]
    selected_complaints = []
    cols = st.columns(3)
    for i, opt in enumerate(complaint_options):
        with cols[i % 3]:
            if st.checkbox(opt, key=f"chk_{opt}"):
                selected_complaints.append(opt)

    other_complaint = ""
    if "기타" in selected_complaints:
        other_complaint = st.text_input(
            "기타 불편사항을 직접 입력하세요",
            placeholder="예: 등이 뻐근함, 앉으면 다리가 저림 등",
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 선택 입력 ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">📐 신체 치수 <span class="badge-opt">선택</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("입력할수록 더 정밀한 분석이 가능합니다.")
    col3, col4, col5, col6 = st.columns(4)
    with col3:
        thigh_input = st.text_input("허벅지 길이 (cm)", placeholder="예: 42")
    with col4:
        desk_input = st.text_input("현재 책상 높이 (cm)", placeholder="예: 73")
    with col5:
        chair_input = st.text_input("현재 의자 높이 (cm)", placeholder="예: 45")
    with col6:
        sitting_input = st.text_input("앉은키 (cm)", placeholder="예: 88")

    budget_raw = st.text_input(
        "💰 소지자금 / 가구 구매 예산 (원)",
        placeholder="예: 300000  ← 입력 시 예산 내 가구 추천",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 사진 업로드 ────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">📸 자세 사진 <span class="badge-opt">선택 · 최대 4장</span></div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "선 자세(정면/측면/후면) 총 4장의 사진을 업로드하면 "
        "거북목·골반 전방경사·척추측만 등을 자동 분석합니다."
    )
    uploaded_files = st.file_uploader(
        "사진 선택 (JPG / PNG, 최대 4장)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="photo_uploader",
    )
    if uploaded_files:
        uploaded_files = uploaded_files[:4]
        prev_cols = st.columns(len(uploaded_files))
        for i, f in enumerate(uploaded_files):
            with prev_cols[i]:
                st.image(f, caption=f"사진 {i+1}", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 분석 버튼 ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🧚 척추요정에게 분석 요청하기")

    if analyze_btn:
        # 유효성 검사
        errors = []
        if not selected_complaints:
            errors.append("불편사항을 1개 이상 선택해 주세요.")
        if "기타" in selected_complaints and not other_complaint.strip():
            errors.append("'기타' 선택 시 구체적인 불편사항을 입력해 주세요.")
        if errors:
            for e in errors:
                st.error(e, icon="🚨")
            st.stop()

        # 데이터 정제
        def safe_float(val):
            try:
                v = float(str(val).replace(",", "").strip())
                return v if v > 0 else None
            except Exception:
                return None

        thigh_len = safe_float(thigh_input)
        desk_h    = safe_float(desk_input)
        chair_h   = safe_float(chair_input)
        sitting_h = safe_float(sitting_input)
        budget    = safe_float(budget_raw)

        images_b64 = []
        if uploaded_files:
            for f in uploaded_files:
                f.seek(0)
                images_b64.append(image_to_base64(f))

        final_complaints = []
        for c in selected_complaints:
            if c == "기타":
                final_complaints.append(f"기타: {other_complaint.strip()}")
            else:
                final_complaints.append(c)

        data = {
            "height":          height,
            "weight":          weight,
            "complaints":      final_complaints,
            "other_complaint": other_complaint.strip() if "기타" in selected_complaints else None,
            "thigh_len":       thigh_len,
            "desk_h":          desk_h,
            "chair_h":         chair_h,
            "sitting_h":       sitting_h,
            "budget":          budget,
            "images":          images_b64 if images_b64 else None,
        }

       # GPT 호출
with st.spinner("🧚 척추요정이 분석 중입니다... 잠시만 기다려 주세요!"):
    try:
        system, content = build_prompt(data)
        result = call_gpt(system, content)

        # ── 하드코딩 가구 추천 ─────────────────────────────

        hardcoded_products = []

        # 허리 통증 사용자
        if "허리 통증" in final_complaints:

            if budget and budget >= 300000:

                hardcoded_products.append({
                    "name": "시디즈 T50 의자",
                    "reason": "허리 지지 기능이 뛰어나 장시간 착석 시 부담을 줄여줍니다.",
                    "price_approx": "320,000원",
                    "url": "https://kr.sidiz.com"
                })

                hardcoded_products.append({
                    "name": "이케아 BEKANT 책상",
                    "reason": "높이 조절이 가능하여 바른 자세 유지에 도움됩니다.",
                    "price_approx": "250,000원",
                    "url": "https://www.ikea.com/kr/ko/"
                })

            else:

                hardcoded_products.append({
                    "name": "듀오백 Q1W",
                    "reason": "가성비가 좋은 인체공학 의자입니다.",
                    "price_approx": "190,000원",
                    "url": "https://www.duoback.co.kr"
                })

        # 목 통증 사용자
        elif "목 통증" in final_complaints:

            hardcoded_products.append({
                "name": "시디즈 TAB+",
                "reason": "목과 어깨 부담 완화에 도움되는 자세 교정형 의자입니다.",
                "price_approx": "230,000원",
                "url": "https://kr.sidiz.com"
            })

        # 어깨 통증 사용자
        elif "어깨 통증" in final_complaints:

            hardcoded_products.append({
                "name": "한샘 샘책상",
                "reason": "적절한 높이로 어깨 긴장을 줄여줍니다.",
                "price_approx": "180,000원",
                "url": "https://www.hanssem.com"
            })

        # 기본 추천
        else:

            hardcoded_products.append({
                "name": "시디즈 T40",
                "reason": "기본적인 자세 교정에 적합한 인체공학 의자입니다.",
                "price_approx": "260,000원",
                "url": "https://kr.sidiz.com"
            })

        # GPT 결과 덮어쓰기
        result["furniture_recommendation"] = hardcoded_products

        # ✅ session_state에 결과 저장 후 result 페이지로 이동
        st.session_state.result = result
        st.session_state.desk_h = desk_h
        st.session_state.chair_h = chair_h
        st.session_state.page = "result"

        st.rerun()

    except json.JSONDecodeError:
        st.error("GPT 응답 파싱에 실패했습니다. 다시 시도해 주세요.", icon="❌")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}", icon="❌")
