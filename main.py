import streamlit as st
from openai import OpenAI
import base64
import json
from PIL import Image
import io
import requests
import re


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
    }

    .sub-header {
        text-align: center;
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 2.5rem;
    }

    .section-card {
        background: rgba(255,255,255,0.88);
        border-radius: 20px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 20px rgba(102,126,234,0.09);
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


# ── 네이버 쇼핑 API 검색 ────────────────────────────────────────────────────
def search_naver_product(query, limit=2):
    client_id = st.secrets["NAVER_CLIENT_ID"]
    client_secret = st.secrets["NAVER_CLIENT_SECRET"]

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    url = "https://openapi.naver.com/v1/search/shop.json"

    params = {
        "query": query,
        "display": limit,
        "sort": "sim"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    results = []

    for item in data.get("items", []):
        title = re.sub(r"<.*?>", "", item["title"])

        results.append({
            "name": title,
            "reason": f"{query} 관련 추천 제품",
            "price_approx": f"{int(item['lprice']):,}원",
            "url": item["link"]
        })

    return results


# ── GPT 프롬프트 생성 ───────────────────────────────────────────────────────
def build_prompt(data: dict) -> tuple:
    has_images = bool(data.get("images"))

    system = """
당신은 척추·자세 교정 전문가입니다.

반드시 아래 JSON만 반환하세요.

{
  "problems": "...",
  "photo_analysis": "...",
  "desk_chair_solution": {
    "recommended_chair_height_cm": 숫자,
    "recommended_desk_height_cm": 숫자,
    "explanation": "..."
  },
  "furniture_recommendation": [],
  "furniture_note": "...",
  "monitor_tips": "..."
}

규칙:
- furniture_recommendation은 반드시 빈 배열([]) 반환
- 제품 추천은 하지 말 것
- problems는 자세 문제 설명
- monitor_tips는 눈높이/거리 설명
"""

    lines = [
        f"키: {data['height']}cm",
        f"몸무게: {data['weight']}kg",
        f"불편사항: {', '.join(data['complaints'])}",
    ]

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


# ── GPT 호출 ────────────────────────────────────────────────────────────────
def call_gpt(system: str, content) -> dict:
    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": content},
        ],
        temperature=0.3,
        max_tokens=2500,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)


# ── 메인 ────────────────────────────────────────────────────────────────────
def show():
    inject_css()

    st.set_page_config(
        page_title="척추요정 🧚",
        page_icon="🧚",
        layout="wide",
    )

    st.markdown('<div class="main-header">🧚 척추요정</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sub-header">자세 분석 + 실제 구매 가능한 가구 추천</div>',
        unsafe_allow_html=True,
    )

    # 기본정보
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📋 기본 정보 <span class="badge-req">필수</span></div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        height = st.number_input("키", 100, 250, 170)

    with col2:
        weight = st.number_input("몸무게", 20, 200, 65)

    complaint_options = [
        "목 통증",
        "허리 통증",
        "어깨 통증",
        "골반 통증",
        "눈 피로",
        "손목/팔 저림"
    ]

    selected_complaints = []

    cols = st.columns(3)

    for i, opt in enumerate(complaint_options):
        with cols[i % 3]:
            if st.checkbox(opt):
                selected_complaints.append(opt)

    st.markdown('</div>', unsafe_allow_html=True)

    # 사진 업로드
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "자세 사진 업로드",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # 분석 버튼
    analyze_btn = st.button("🧚 분석 시작")

    if analyze_btn:

        images_b64 = []

        if uploaded_files:
            for f in uploaded_files:
                f.seek(0)
                images_b64.append(image_to_base64(f))

        data = {
            "height": height,
            "weight": weight,
            "complaints": selected_complaints,
            "images": images_b64 if images_b64 else None,
        }

        with st.spinner("분석 중입니다..."):

            system, content = build_prompt(data)

            result = call_gpt(system, content)

            # ── 실제 상품 검색 ─────────────────────────────────────
            product_queries = []

            if any("허리" in c or "골반" in c for c in selected_complaints):
                product_queries.append("시디즈 T50 정품")

            if any("목" in c or "어깨" in c for c in selected_complaints):
                product_queries.append("허먼밀러 에어론")

            if any("눈" in c for c in selected_complaints):
                product_queries.append("루나랩 모니터암")

            if any("손목" in c for c in selected_complaints):
                product_queries.append("로지텍 MX 팜레스트")

            if not product_queries:
                product_queries.append("인체공학 의자")

            real_products = []

            for q in product_queries:
                real_products.extend(search_naver_product(q))

            result["furniture_recommendation"] = real_products[:4]

            # 결과 출력
            st.success("분석 완료!")

            st.subheader("📌 예상 문제")

            st.write(result["problems"])

            if result["photo_analysis"]:
                st.subheader("📸 사진 분석")
                st.write(result["photo_analysis"])

            st.subheader("🪑 추천 책상/의자 높이")

            st.write(
                f"추천 의자 높이: {result['desk_chair_solution']['recommended_chair_height_cm']} cm"
            )

            st.write(
                f"추천 책상 높이: {result['desk_chair_solution']['recommended_desk_height_cm']} cm"
            )

            st.write(result["desk_chair_solution"]["explanation"])

            st.subheader("🛒 실제 구매 가능한 추천 제품")

            for item in result["furniture_recommendation"]:

                st.markdown(f"### {item['name']}")

                st.write(item["reason"])

                st.write(f"가격: {item['price_approx']}")

                st.markdown(
                    f"[구매 링크 바로가기]({item['url']})"
                )

            st.subheader("🖥️ 모니터 팁")

            st.write(result["monitor_tips"])
