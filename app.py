import streamlit as st
from openai import OpenAI
import base64
import json
from PIL import Image
import io

# ── 페이지 설정 ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="척추요정 🧚",
    page_icon="🧚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 전체 CSS ─────────────────────────────────────────────────────────────────
st.markdown("""선 자세(정면/측면/후면) 총 4장의 사진을 업로드하면 
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f0fff8 100%);
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

.result-wrapper {
    background: rgba(255,255,255,0.97);
    border-radius: 22px;
    padding: 2.2rem 2.6rem;
    margin-top: 2rem;
    box-shadow: 0 8px 40px rgba(102,126,234,0.13);
    border-left: 6px solid #667eea;
}

.result-section {
    margin-bottom: 1.6rem;
}

.result-section h3 {
    font-size: 1.13rem;
    font-weight: 800;
    color: #4338ca;
    margin-bottom: 0.6rem;
    padding-bottom: 0.35rem;
    border-bottom: 2px solid #e0e7ff;
}

.tip-box {
    background: linear-gradient(135deg, #fffbeb, #fef9c3);
    border-radius: 14px;
    padding: 1.1rem 1.5rem;
    border-left: 5px solid #fbbf24;
    margin-top: 1.4rem;
}

.tip-box h3 {
    color: #b45309;
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
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
    # RGBA → RGB 변환 (JPEG 저장을 위해)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


# ── GPT-4o 프롬프트 생성 ─────────────────────────────────────────────────────
def build_prompt(data: dict) -> list:
    """
    data keys:
      height, weight, complaints, other_complaint,
      thigh_len (opt), desk_h (opt), chair_h (opt),
      sitting_h (opt), budget (opt),
      images (opt) : list of base64 strings
    """
    has_images = bool(data.get("images"))
    has_budget = data.get("budget") is not None

    # 시스템 메시지
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
   - 의자 높이 계산 기준: 허벅지 길이 또는 키×0.25 (대략적 오금 높이)
   - 책상 높이 계산 기준: 의자 높이 + 앉은키×0.45 (팔꿈치 높이 기준) 또는 키×0.43 추정
4. furniture_recommendation: 현재 책상/의자 높이가 권장 범위를 벗어나고 조절이 불가한 경우에만 추천.
   예산이 있을 때: 예산 내 실제 한국 판매 제품 추천 (쿠팡, 무신사, 오늘의집, 이케아코리아 등 실제 URL)
   예산이 없을 때: 일반적인 가격대 제품 추천
   예산 초과 시: furniture_note에 "예산 내 구매 가능한 제품을 찾지 못했습니다" 명시하고 빈 배열 반환
5. monitor_tips: 모니터 눈높이(모니터 상단이 눈높이와 같거나 약간 아래)와 적정 거리(40~70cm) 관련 구체적 팁
"""

    # 사용자 메시지 텍스트 구성
    lines = [
        f"## 사용자 신체 정보",
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
        lines.append("아래 사진 4장을 분석하여 자세 문제(거북목, 골반전방경사, 척추측만, 디스크 등)를 파악하고, 가능하면 허벅지 길이와 앉은키도 추정해 주세요.")

    user_text = "\n".join(lines)

    # 멀티모달 content 구성
    if has_images:
        content = [{"type": "text", "text": user_text}]
        for i, b64 in enumerate(data["images"], 1):
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{b64}",
                    "detail": "high"
                }
            })
    else:
        content = user_text  # 이미지 없을 때는 텍스트만

    return system, content


# ── GPT-4o 호출 ──────────────────────────────────────────────────────────────
def call_gpt(system: str, content) -> dict:
    client = get_client()

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": content},
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.4,
        max_tokens=2500,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    return json.loads(raw)


# ── 결과 렌더링 ──────────────────────────────────────────────────────────────
def render_results(result: dict, current_desk: float | None, current_chair: float | None):
    st.markdown('<div class="result-wrapper">', unsafe_allow_html=True)

    # 1) 사진 분석
    if result.get("photo_analysis"):
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### 📸 사진 분석 결과")
        st.markdown(result["photo_analysis"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()

    # 2) 문제점
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.markdown("### 🔍 예상 문제점")
    st.markdown(result.get("problems", "—"))
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    # 3) 책상/의자 조절 솔루션
    sol = result.get("desk_chair_solution", {})
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.markdown("### 🪑 책상 · 의자 높이 권장값")

    col_c, col_d = st.columns(2)
    rec_chair = sol.get("recommended_chair_height_cm")
    rec_desk  = sol.get("recommended_desk_height_cm")

    with col_c:
        st.metric(
            label="🟢 권장 의자 높이",
            value=f"{rec_chair} cm" if rec_chair else "—",
            delta=f"{round(rec_chair - current_chair, 1):+.1f} cm 조정 필요" if (rec_chair and current_chair) else None,
        )
    with col_d:
        st.metric(
            label="🔵 권장 책상 높이",
            value=f"{rec_desk} cm" if rec_desk else "—",
            delta=f"{round(rec_desk - current_desk, 1):+.1f} cm 조정 필요" if (rec_desk and current_desk) else None,
        )

    if sol.get("explanation"):
        st.info(sol["explanation"], icon="💡")
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    # 4) 가구 추천
    furniture_list = result.get("furniture_recommendation", [])
    furniture_note = result.get("furniture_note", "")
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.markdown("### 🛒 가구 추천")

    if furniture_note:
        st.warning(furniture_note, icon="⚠️")

    if furniture_list:
        for item in furniture_list:
            with st.expander(f"🛋️ {item.get('name', '제품명 없음')}  —  {item.get('price_approx', '')}"):
                st.markdown(f"**추천 이유:** {item.get('reason', '—')}")
                url = item.get("url", "")
                if url and url.startswith("http"):
                    st.markdown(f"**구매 링크:** [바로가기 →]({url})")
                else:
                    st.markdown(f"**참고:** {url}")
    elif not furniture_note:
        st.success("현재 가구 높이 조절만으로 충분히 해결 가능합니다! 별도 구매 불필요 🎉", icon="✅")

    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    # 5) 모니터 팁
    tips = result.get("monitor_tips", "")
    if tips:
        st.markdown("""
        <div class="tip-box">
            <h3>🖥️ 모니터 눈높이 & 거리 팁</h3>
        """, unsafe_allow_html=True)
        st.markdown(tips)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # result-wrapper 닫기


# ════════════════════════════════════════════════════════════════════════════
#  메인 UI
# ════════════════════════════════════════════════════════════════════════════
def main():
    # 헤더
    st.markdown('<div class="main-header">🧚 척추요정</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">당신의 자세를 분석하고, 맞춤 솔루션을 제안해 드려요</div>',
        unsafe_allow_html=True,
    )

    # ── 필수 입력 ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">📋 기본 정보 <span class="badge-req">필수</span></div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input(
            "키 (cm)", min_value=100, max_value=250, value=170, step=1
        )
    with col2:
        weight = st.number_input(
            "몸무게 (kg)", min_value=20, max_value=200, value=65, step=1
        )

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

    # ── 선택 입력 ────────────────────────────────────────────────────────────
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

    # ── 사진 업로드 ──────────────────────────────────────────────────────────
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

    # 미리보기
    if uploaded_files:
        n = min(len(uploaded_files), 4)
        uploaded_files = uploaded_files[:4]
        prev_cols = st.columns(n)
        for i, f in enumerate(uploaded_files):
            with prev_cols[i]:
                st.image(f, caption=f"사진 {i+1}", use_container_width=True)
        if len(uploaded_files) > 4:
            st.warning("4장까지만 분석됩니다. 처음 4장이 사용됩니다.", icon="⚠️")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── 분석 버튼 ────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🧚 척추요정에게 분석 요청하기")

    if analyze_btn:
        # ── 유효성 검사 ───────────────────────────────────────────────────────
        errors = []
        if not selected_complaints:
            errors.append("불편사항을 1개 이상 선택해 주세요.")
        if "기타" in selected_complaints and not other_complaint.strip():
            errors.append("'기타' 선택 시 구체적인 불편사항을 입력해 주세요.")

        if errors:
            for e in errors:
                st.error(e, icon="🚨")
            st.stop()

        # ── 데이터 정제 ───────────────────────────────────────────────────────
        def safe_float(val):
            try:
                v = float(str(val).replace(",", "").strip())
                return v if v > 0 else None
            except Exception:
                return None

        thigh_len  = safe_float(thigh_input)
        desk_h     = safe_float(desk_input)
        chair_h    = safe_float(chair_input)
        sitting_h  = safe_float(sitting_input)
        budget     = safe_float(budget_raw)

        # 이미지 처리
        images_b64 = []
        if uploaded_files:
            for f in uploaded_files:
                f.seek(0)
                images_b64.append(image_to_base64(f))

        # 최종 complaint 리스트 (기타 → 실제 입력으로 대체)
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

        # ── GPT 호출 ──────────────────────────────────────────────────────────
        with st.spinner("🧚 척추요정이 분석 중입니다... 잠시만 기다려 주세요!"):
            try:
                system, content = build_prompt(data)
                result = call_gpt(system, content)
                st.success("분석 완료! 아래 결과를 확인하세요 ✨", icon="🎉")
                render_results(result, desk_h, chair_h)
            except json.JSONDecodeError:
                st.error("GPT 응답 파싱에 실패했습니다. 다시 시도해 주세요.", icon="❌")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}", icon="❌")


if __name__ == "__main__":
    main()
