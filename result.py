import streamlit as st
from openai import OpenAI
import base64
import json
from PIL import Image
import io
import requests
import urllib.parse
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


# ── 네이버 쇼핑 검색 ─────────────────────────────────────────────────────────
def search_naver_product(product_name: str):

    client_id = st.secrets["NAVER_CLIENT_ID"]
    client_secret = st.secrets["NAVER_CLIENT_SECRET"]

    query = urllib.parse.quote(product_name)

    url = (
        f"https://openapi.naver.com/v1/search/shop.json"
        f"?query={query}&display=1&sort=sim"
    )

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    items = response.json().get("items", [])

    if not items:
        return None

    item = items[0]

    clean_title = re.sub("<.*?>", "", item["title"])

    return {
        "title": clean_title,
        "link": item["link"],
        "price": item["lprice"],
        "mall": item["mallName"],
    }


# ── GPT 프롬프트 생성 ────────────────────────────────────────────────────────
def build_prompt(data: dict):

    has_images = bool(data.get("images"))
    has_budget = data.get("budget") is not None

    system = """
당신은 척추·자세 교정 전문가이자 인체공학 컨설턴트입니다.

반드시 아래 JSON 형식만 반환하세요.

{
  "problems": "...",
  "photo_analysis": "...",
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
      "url": ""
    }
  ],
  "furniture_note": "...",
  "monitor_tips": "..."
}

규칙:

1. furniture_recommendation:
- 실제 한국에서 판매 중인 제품명 추천
- URL 생성 금지
- url 값은 항상 빈 문자열("") 반환
- 실제 판매 제품명 형태로 작성

좋은 예시:
- 시디즈 T50 에어
- 한샘 샘책상 1400
- 듀오백 Q1W

나쁜 예시:
- 시디즈 의자
- 좋은 책상
"""

    lines = [
        f"키: {data['height']}cm",
        f"몸무게: {data['weight']}kg",
        f"불편사항: {', '.join(data['complaints'])}",
    ]

    if data.get("desk_h"):
        lines.append(f"현재 책상 높이: {data['desk_h']}cm")

    if data.get("chair_h"):
        lines.append(f"현재 의자 높이: {data['chair_h']}cm")

    if has_budget:
        lines.append(f"예산: {int(data['budget']):,}원")

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
def call_gpt(system: str, content):

    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": content},
        ],
        temperature=0.4,
        max_tokens=2500,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)


# ── 메인 ────────────────────────────────────────────────────────────────────
def show():

    inject_css()

    st.set_page_config(
        page_title="척추요정",
        page_icon="🧚",
        layout="wide",
    )

    st.title("🧚 척추요정")

    height = st.number_input("키(cm)", 100, 250, 170)
    weight = st.number_input("몸무게(kg)", 20, 200, 65)

    complaints = st.multiselect(
        "불편사항",
        [
            "목 통증",
            "허리 통증",
            "어깨 통증",
            "골반 통증",
            "두통",
            "눈 피로",
        ]
    )

    desk_input = st.text_input("현재 책상 높이(cm)")
    chair_input = st.text_input("현재 의자 높이(cm)")
    budget_input = st.text_input("예산(원)")

    uploaded_files = st.file_uploader(
        "자세 사진 업로드",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if st.button("분석하기"):

        def safe_float(v):
            try:
                return float(str(v).replace(",", "").strip())
            except:
                return None

        desk_h = safe_float(desk_input)
        chair_h = safe_float(chair_input)
        budget = safe_float(budget_input)

        images_b64 = []

        if uploaded_files:
            for f in uploaded_files:
                f.seek(0)
                images_b64.append(image_to_base64(f))

        data = {
            "height": height,
            "weight": weight,
            "complaints": complaints,
            "desk_h": desk_h,
            "chair_h": chair_h,
            "budget": budget,
            "images": images_b64 if images_b64 else None,
        }

        with st.spinner("분석 중입니다..."):

            system, content = build_prompt(data)

            result = call_gpt(system, content)

            # ── 네이버 쇼핑 실제 링크 연결 ───────────────────────────
            furniture_list = result.get("furniture_recommendation", [])

            for item in furniture_list:

                product = search_naver_product(item["name"])

                if product:
                    item["url"] = product["link"]
                    item["price_approx"] = f"{int(product['price']):,}원"

            st.session_state.result = result
            st.session_state.page = "result"

            st.success("분석 완료!")
            st.json(result)