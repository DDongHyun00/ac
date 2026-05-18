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
        padding: 0.9rem 1rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 20px rgba(102,126,234,0.09);
        border: 1.5px solid rgba(102,126,234,0.12);
        backdrop-filter: blur(8px);
    }
    .section-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #4338ca;
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


# ── 하드코딩 제품 DB ─────────────────────────────────────────────────────────
PRODUCT_DB = {
    "chairs": [
        {
            "id": "chair_1",
            "name": "시디즈 T50 HF (메쉬 의자)",
            "price": 279000,
            "price_str": "279,000원",
            "height_range_cm": [38, 47],   # 좌판 높이 조절 범위
            "features": ["높이조절", "요추지지대", "목받침", "팔걸이4D조절", "메쉬등판"],
            "url": "https://kr.sidiz.com/pages/t50",
            "coupang_url": "https://www.coupang.com/np/search?q=%EC%8B%9C%EB%94%94%EC%A6%88+T50+HF",
            "tags": ["허리", "목", "어깨", "기본", "가성비"],
        },
        {
            "id": "chair_2",
            "name": "시디즈 T50 HLDA (풀옵션 메쉬 의자)",
            "price": 359000,
            "price_str": "359,000원",
            "height_range_cm": [43, 50],
            "features": ["높이조절", "요추지지대", "목받침조절", "팔걸이4D조절", "좌판깊이조절", "메쉬등판", "리미티드틸팅"],
            "url": "https://kr.sidiz.com/pages/t50",
            "coupang_url": "https://www.coupang.com/np/search?q=%EC%8B%9C%EB%94%94%EC%A6%88+T50+HLDA",
            "tags": ["허리", "목", "어깨", "골반", "풀옵션", "고급"],
        },
        {
            "id": "chair_3",
            "name": "시디즈 탭스퀘어 (가성비 의자)",
            "price": 199000,
            "price_str": "199,000원",
            "height_range_cm": [40, 50],
            "features": ["높이조절", "요추지지대", "팔걸이조절"],
            "url": "https://www.coupang.com/np/search?q=%EC%8B%9C%EB%94%94%EC%A6%88+%ED%83%AD%EC%8A%A4%ED%80%98%EC%96%B4",
            "coupang_url": "https://www.coupang.com/np/search?q=%EC%8B%9C%EB%94%94%EC%A6%88+%ED%83%AD%EC%8A%A4%EC%9D%98%EC%96%B4",
            "tags": ["허리", "가성비", "입문"],
        },
        {
            "id": "chair_4",
            "name": "시디즈 T50 AIR HLDA (에어메쉬 풀옵션)",
            "price": 439000,
            "price_str": "439,000원",
            "height_range_cm": [43, 50],
            "features": ["에어메쉬등판", "높이조절", "요추지지대", "목받침조절", "팔걸이4D", "좌판깊이조절", "틸팅"],
            "url": "https://kr.sidiz.com/pages/t50",
            "coupang_url": "https://www.coupang.com/np/search?q=%EC%8B%9C%EB%94%94%EC%A6%88+T50+AIR+HLDA",
            "tags": ["허리", "목", "어깨", "골반", "프리미엄", "통기성"],
        },
    ],
    "desks": [
        {
            "id": "desk_1",
            "name": "데스커 컴퓨터책상 1200×600 (고정형)",
            "price": 159000,
            "price_str": "159,000원",
            "height_cm": 72,              # 고정 높이
            "height_adjustable": False,
            "features": ["배선홀", "깔끔한디자인", "무료배송"],
            "url": "https://www.desker.co.kr/products/category?subCateNo=10&searchType=dtl&sort=best",
            "coupang_url": "https://www.coupang.com/np/search?q=%EB%8D%B0%EC%8A%A4%EC%BB%A4+%EC%BB%B4%ED%93%A8%ED%84%B0%EC%B1%85%EC%83%81",
            "tags": ["고정형", "가성비"],
        },
        {
            "id": "desk_2",
            "name": "데스커 알파 모션 스탠딩 책상 1400×700 (전동 높이조절)",
            "price": 538000,
            "price_str": "538,000원",
            "height_range_cm": [71, 116],  # 높이 조절 범위
            "height_adjustable": True,
            "features": ["전동높이조절", "스탠딩가능", "LINAK모터", "충돌방지", "높이기억4단계", "배선선반"],
            "url": "https://www.desker.co.kr/products/category?subCateNo=15&searchType=dtl&sort=best",
            "coupang_url": "https://www.coupang.com/np/search?q=%EB%8D%B0%EC%8A%A4%EC%BB%A4+%EB%AA%A8%EC%85%98+%EC%8A%A4%ED%83%A0%EB%94%A9%EC%B1%85%EC%83%81",
            "tags": ["전동높이조절", "스탠딩", "허리", "프리미엄"],
        },
        {
            "id": "desk_3",
            "name": "데스커 모션 컨트롤스위치 스탠딩 책상 1800×700",
            "price": 698000,
            "price_str": "698,000원",
            "height_range_cm": [68, 113],
            "height_adjustable": True,
            "features": ["전동높이조절", "스탠딩가능", "넓은작업공간", "LINAK모터", "높이기억"],
            "url": "https://www.desker.co.kr/products/category?subCateNo=15&searchType=dtl&sort=best",
            "coupang_url": "https://www.coupang.com/np/search?q=%EB%8D%B0%EC%8A%A4%EC%BB%A4+%EB%AA%A8%EC%85%98+%EC%8A%A4%ED%83%A0%EB%94%A9+1800",
            "tags": ["전동높이조절", "스탠딩", "대형", "허리", "프리미엄"],
        },
    ],
    "monitor_arms": [
        {
            "id": "arm_1",
            "name": "카멜마운트 MOS1 싱글 모니터암",
            "price": 65000,
            "price_str": "65,000원",
            "features": ["상하좌우각도조절", "높이조절", "VESA75/100호환", "최대9kg"],
            "url": "https://www.camelmountmall.com/goods/goods_list.php?cateCd=036001",
            "coupang_url": "https://www.coupang.com/np/search?q=%EC%B9%B4%EB%A9%9C%EB%A7%88%EC%9A%B4%ED%8A%B8+MOS1+%EB%AA%A8%EB%8B%88%ED%84%B0%EC%95%94",
            "tags": ["눈피로", "목", "어깨", "모니터높이조절", "싱글"],
        },
        {
            "id": "arm_2",
            "name": "카멜마운트 CA-1 싱글 모니터암 (베스트셀러)",
            "price": 29000,
            "price_str": "29,000원",
            "features": ["상하각도조절", "VESA75/100호환", "최대7kg", "가성비"],
            "url": "https://prod.danawa.com/info/?pcode=13115675",
            "coupang_url": "https://www.coupang.com/np/search?q=%EC%B9%B4%EB%A9%9C%EB%A7%88%EC%9A%B4%ED%8A%B8+CA-1+%EB%AA%A8%EB%8B%88%ED%84%B0%EC%95%94",
            "tags": ["눈피로", "목", "모니터높이조절", "가성비", "싱글"],
        },
    ],
    "footrests": [
        {
            "id": "foot_1",
            "name": "발편한 각도조절 발받침대 (사무용)",
            "price": 25000,
            "price_str": "25,000원",
            "features": ["각도조절", "미끄럼방지", "높이보정"],
            "url": "https://www.coupang.com/np/search?q=%EC%82%AC%EB%AC%B4%EC%9A%A9+%EB%B0%9C%EB%B0%9B%EC%B9%A8%EB%8C%80+%EA%B0%81%EB%8F%84%EC%A1%B0%EC%A0%88",
            "coupang_url": "https://www.coupang.com/np/search?q=%EC%82%AC%EB%AC%B4%EC%9A%A9+%EB%B0%9C%EB%B0%9B%EC%B9%A8%EB%8C%80",
            "tags": ["무릎", "발목", "다리저림", "키작은", "책상높이보정"],
        },
    ],
    "lumbar_supports": [
        {
            "id": "lumbar_1",
            "name": "메모리폼 허리쿠션 요추받침대",
            "price": 35000,
            "price_str": "35,000원",
            "features": ["메모리폼", "벨트고정", "허리곡선지지"],
            "url": "https://www.coupang.com/np/search?q=%ED%97%88%EB%A6%AC%EC%BF%A0%EC%85%98+%EC%9A%94%EC%B6%94%EB%B0%9B%EC%B9%A8%EB%8C%80+%EC%82%AC%EB%AC%B4%EC%9A%A9",
            "coupang_url": "https://www.coupang.com/np/search?q=%ED%97%88%EB%A6%AC%EC%BF%A0%EC%85%98+%EC%9A%94%EC%B6%94%EB%B0%9B%EC%B9%A8%EB%8C%80",
            "tags": ["허리", "보조용품", "가성비"],
        },
    ],
}

def get_product_catalog_text() -> str:
    """GPT에게 넘길 제품 카탈로그 텍스트 생성"""
    lines = ["## 추천 가능한 제품 카탈로그 (이 목록에서만 선택할 것)"]

    lines.append("\n### [의자]")
    for p in PRODUCT_DB["chairs"]:
        lines.append(f"- id: {p['id']} | {p['name']} | {p['price_str']} | 좌판높이: {p.get('height_range_cm', ['?'])[0]}~{p.get('height_range_cm', ['?', '?'])[1]}cm | 태그: {', '.join(p['tags'])}")

    lines.append("\n### [책상]")
    for p in PRODUCT_DB["desks"]:
        if p["height_adjustable"]:
            h = f"높이조절 {p['height_range_cm'][0]}~{p['height_range_cm'][1]}cm"
        else:
            h = f"고정높이 {p['height_cm']}cm"
        lines.append(f"- id: {p['id']} | {p['name']} | {p['price_str']} | {h} | 태그: {', '.join(p['tags'])}")

    lines.append("\n### [모니터암]")
    for p in PRODUCT_DB["monitor_arms"]:
        lines.append(f"- id: {p['id']} | {p['name']} | {p['price_str']} | 태그: {', '.join(p['tags'])}")

    lines.append("\n### [발받침대]")
    for p in PRODUCT_DB["footrests"]:
        lines.append(f"- id: {p['id']} | {p['name']} | {p['price_str']} | 태그: {', '.join(p['tags'])}")

    lines.append("\n### [허리쿠션]")
    for p in PRODUCT_DB["lumbar_supports"]:
        lines.append(f"- id: {p['id']} | {p['name']} | {p['price_str']} | 태그: {', '.join(p['tags'])}")

    return "\n".join(lines)

def resolve_products(product_ids: list) -> list:
    """GPT가 고른 id 목록을 실제 제품 정보로 변환"""
    all_products = (
        PRODUCT_DB["chairs"]
        + PRODUCT_DB["desks"]
        + PRODUCT_DB["monitor_arms"]
        + PRODUCT_DB["footrests"]
        + PRODUCT_DB["lumbar_supports"]
    )
    id_map = {p["id"]: p for p in all_products}
    result = []
    for pid in product_ids:
        if pid in id_map:
            p = id_map[pid]
            result.append({
                "name": p["name"],
                "reason": "",   # GPT가 채울 예정
                "price_approx": p["price_str"],
                "url": p["url"],
                "coupang_url": p.get("coupang_url", p["url"]),
            })
    return result


# ── GPT-4o 프롬프트 생성 ─────────────────────────────────────────────────────
def build_prompt(data: dict) -> tuple:
    has_images = bool(data.get("images"))
    has_budget = data.get("budget") is not None

    catalog_text = get_product_catalog_text()

    system = f"""당신은 척추·자세 교정 전문가이자 인체공학(에르고노믹스) 컨설턴트입니다.
사용자의 신체 정보와 불편 증상을 바탕으로 **한국어**로 답변하세요.

{catalog_text}

[출력 형식 – 반드시 아래 JSON만 반환, 코드블록(```) 없이]
{{
  "problems": "...",
  "photo_analysis": "...(사진 없으면 null)",
  "desk_chair_solution": {{
    "recommended_chair_height_cm": 숫자,
    "recommended_desk_height_cm": 숫자,
    "explanation": "..."
  }},
  "furniture_recommendation": [
    {{
      "product_id": "카탈로그의 id 값 (예: chair_2)",
      "reason": "이 사용자에게 이 제품이 필요한 구체적 이유"
    }}
  ],
  "furniture_note": "...(예산 초과 또는 조절만으로 해결 가능 시 설명, 해당없으면 null)",
  "monitor_tips": "..."
}}

규칙:
1. problems: 입력된 불편사항과 신체 데이터를 바탕으로 예상 문제점 설명 (사진 있으면 반영)
2. photo_analysis: 사진 있을 때만 거북목/디스크/골반전방경사/척추측만 분석, 없으면 null
3. desk_chair_solution: 허벅지 길이·앉은키 있으면 정밀 계산, 없으면 키 기반 추정
   - 의자 높이: 허벅지 길이 또는 키×0.25
   - 책상 높이: 의자 높이 + 앉은키×0.45 또는 키×0.43
4. furniture_recommendation:
   - 반드시 위 카탈로그의 id만 사용할 것 (임의 제품 추천 절대 금지)
   - 현재 의자/책상 높이가 권장 범위를 벗어나거나 조절 불가 시 의자/책상 추천
   - 눈 피로·목 통증 있으면 모니터암 추천
   - 의자가 너무 높아 발이 뜨는 경우 발받침대 추천
   - 허리 통증인데 의자 교체 예산이 없으면 허리쿠션 추천
   - 예산 있을 때: 예산 내 제품만 선택 (price 필드 기준)
   - 예산 초과 제품만 있으면: 빈 배열 반환 + furniture_note에 설명
5. monitor_tips: 모니터 눈높이·거리(40~70cm) 팁
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
        temperature=0.4,
        max_tokens=2500,
        response_format={"type": "json_object"},
    )
    raw = json.loads(response.choices[0].message.content)

    # furniture_recommendation: product_id → 실제 제품 정보로 변환
    all_products = (
        PRODUCT_DB["chairs"]
        + PRODUCT_DB["desks"]
        + PRODUCT_DB["monitor_arms"]
        + PRODUCT_DB["footrests"]
        + PRODUCT_DB["lumbar_supports"]
    )
    id_map = {p["id"]: p for p in all_products}

    resolved = []
    for item in raw.get("furniture_recommendation", []):
        pid = item.get("product_id", "")
        if pid in id_map:
            p = id_map[pid]
            resolved.append({
                "name": p["name"],
                "reason": item.get("reason", ""),
                "price_approx": p["price_str"],
                "url": p["url"],
                "coupang_url": p.get("coupang_url", p["url"]),
            })
    raw["furniture_recommendation"] = resolved
    return raw


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
    st.markdown(
        '<div class="section-card"><div class="section-title">📋 기본 정보 <span class="badge-req">필수</span></div></div>',
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
    st.markdown(
        '<div class="section-card"><div class="section-title">📐 신체 치수 <span class="badge-opt">선택</span></div></div>',
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
    st.markdown(
        '<div class="section-card"><div class="section-title">📸 자세 사진 <span class="badge-opt">선택 · 최대 4장</span></div></div>',
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

                # ✅ session_state에 결과 저장 후 result 페이지로 이동
                st.session_state.result     = result
                st.session_state.desk_h     = desk_h
                st.session_state.chair_h    = chair_h
                st.session_state.page       = "result"
                st.rerun()

            except json.JSONDecodeError:
                st.error("GPT 응답 파싱에 실패했습니다. 다시 시도해 주세요.", icon="❌")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}", icon="❌")