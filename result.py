import streamlit as st


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
        font-size: 1.05rem;
        font-weight: 800;
        transition: all 0.3s;
        box-shadow: 0 5px 20px rgba(102,126,234,0.38);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102,126,234,0.50);
    }
    </style>
    """, unsafe_allow_html=True)


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

    # 3) 책상/의자 권장값
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
            delta=f"{round(rec_chair - current_chair, 1):+.1f} cm 조정 필요"
                  if (rec_chair and current_chair) else None,
        )
    with col_d:
        st.metric(
            label="🔵 권장 책상 높이",
            value=f"{rec_desk} cm" if rec_desk else "—",
            delta=f"{round(rec_desk - current_desk, 1):+.1f} cm 조정 필요"
                  if (rec_desk and current_desk) else None,
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
                if (
                    url
                    and url.startswith("http")
                    and "search" not in url.lower()
                    and "category" not in url.lower()
                    and "brand" not in url.lower()
                ):
                    st.markdown(f"**구매 링크:** [바로가기 →]({url})")
                else:
                    st.markdown("**구매 링크:** 정확한 상품 링크를 찾지 못했습니다.")
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

    st.markdown('</div>', unsafe_allow_html=True)


# ── 메인 show() ──────────────────────────────────────────────────────────────
def show():
    inject_css()

    # ✅ 결과 데이터가 없으면 메인 페이지로 자동 복귀
    if "result" not in st.session_state:
        st.warning("분석 결과가 없습니다. 입력 페이지로 돌아갑니다.")
        st.session_state.page = "main"
        st.rerun()
        return

    st.markdown('<div class="main-header">🧚 척추요정 분석 결과</div>', unsafe_allow_html=True)
    st.success("분석 완료! 아래 결과를 확인하세요 ✨", icon="🎉")

    # 결과 렌더링
    render_results(
        result=st.session_state.result,
        current_desk=st.session_state.get("desk_h"),
        current_chair=st.session_state.get("chair_h"),
    )

    # ✅ 다시 분석하기 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 다시 분석하기"):
        # 결과 데이터 초기화 후 메인으로 이동
        del st.session_state.result
        st.session_state.page = "main"
        st.rerun()
