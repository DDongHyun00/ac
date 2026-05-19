import streamlit as st


# ── CSS ──────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background-color: #F5F2EC;
    }
    .block-container {
        max-width: 780px !important;
        padding: 0 2rem 4rem 2rem !important;
        margin: 0 auto !important;
    }

    /* ── 헤더 ── */
    .page-header {
        padding: 3.5rem 0 0.4rem 0;
        border-bottom: 2px solid #1a1a1a;
        margin-bottom: 0.35rem;
    }
    .page-header-eyebrow {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 0.6rem;
    }
    .page-header-title {
        font-family: 'DM Serif Display', serif;
        font-size: 3.8rem;
        line-height: 1.0;
        color: #1a1a1a;
        letter-spacing: -0.02em;
    }
    .page-header-accent {
        display: inline-block;
        background: #C8F04B;
        color: #1a1a1a;
        font-style: normal;
        padding: 0 6px;
        border-radius: 4px;
    }
    .page-sub {
        font-size: 0.88rem;
        color: #888;
        margin-top: 0.6rem;
        margin-bottom: 2.6rem;
        font-weight: 300;
    }

    /* ── 섹션 레이블 ── */
    .section-label {
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #aaa;
        margin-bottom: 0.9rem;
        margin-top: 2.4rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: #ddd;
    }

    /* ── 결과 카드 ── */
    .result-card {
        background: #fff;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        border: 1.5px solid #ede9e0;
    }
    .result-card p {
        font-size: 0.9rem;
        line-height: 1.75;
        color: #333;
        margin: 0;
    }

    /* ── 수치 카드 ── */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        flex: 1;
        background: #fff;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        border: 1.5px solid #ede9e0;
    }
    .metric-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #aaa;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-family: 'DM Serif Display', serif;
        font-size: 2.4rem;
        color: #1a1a1a;
        line-height: 1;
    }
    .metric-unit {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        font-weight: 400;
        color: #888;
        margin-left: 2px;
    }
    .metric-delta {
        font-size: 0.78rem;
        font-weight: 500;
        margin-top: 0.4rem;
        padding: 2px 8px;
        border-radius: 999px;
        display: inline-block;
    }
    .metric-delta-pos {
        background: #f0fde8;
        color: #4a8c1c;
    }
    .metric-delta-neg {
        background: #fff3e8;
        color: #b85c00;
    }
    .metric-delta-zero {
        background: #f0f0f0;
        color: #888;
    }

    /* ── 설명 박스 ── */
    .info-box {
        background: #f9f8f4;
        border-left: 3px solid #C8F04B;
        border-radius: 0 10px 10px 0;
        padding: 0.85rem 1.1rem;
        margin-top: 0.8rem;
        font-size: 0.87rem;
        color: #444;
        line-height: 1.65;
    }

    /* ── 제품 카드 ── */
    .product-card {
        background: #fff;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.75rem;
        border: 1.5px solid #ede9e0;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .product-name {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1a1a1a;
    }
    .product-price {
        font-size: 0.82rem;
        color: #888;
        font-weight: 400;
    }
    .product-reason {
        font-size: 0.84rem;
        color: #555;
        line-height: 1.6;
    }
    .product-link-row {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-top: 0.25rem;
    }
    .product-link {
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 999px;
        text-decoration: none !important;
        transition: background 0.15s;
        display: inline-block;
    }
    .link-primary {
        background: #1a1a1a;
        color: #C8F04B !important;
    }
    .link-secondary {
        background: #f0f0f0;
        color: #333 !important;
    }

    /* ── 모니터 팁 ── */
    .tip-card {
        background: #1a1a1a;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
    }
    .tip-card p {
        font-size: 0.9rem;
        color: #d4d0c8;
        line-height: 1.75;
        margin: 0;
    }
    .tip-card-title {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #C8F04B;
        margin-bottom: 0.7rem;
    }

    /* ── 다시 분석 버튼 ── */
    .stButton > button {
        background: transparent !important;
        color: #1a1a1a !important;
        border: 1.5px solid #1a1a1a !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
        transition: background 0.18s, color 0.18s !important;
    }
    .stButton > button:hover {
        background: #1a1a1a !important;
        color: #C8F04B !important;
    }

    /* 완료 배너 */
    .done-banner {
        background: #C8F04B;
        border-radius: 12px;
        padding: 0.75rem 1.2rem;
        font-size: 0.88rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        letter-spacing: 0.01em;
    }
    </style>
    """, unsafe_allow_html=True)


# ── 결과 렌더링 ──────────────────────────────────────────────────────────────
def render_results(result: dict, current_desk: float | None, current_chair: float | None):

    # 1) 사진 분석
    if result.get("photo_analysis"):
        st.markdown('<div class="section-label">사진 분석 결과</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-card"><p>{result["photo_analysis"]}</p></div>', unsafe_allow_html=True)

    # 2) 예상 문제점
    st.markdown('<div class="section-label">예상 문제점</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-card"><p>{result.get("problems", "—")}</p></div>', unsafe_allow_html=True)

    # 3) 책상/의자 권장값
    st.markdown('<div class="section-label">권장 높이</div>', unsafe_allow_html=True)
    sol = result.get("desk_chair_solution", {})
    rec_chair = sol.get("recommended_chair_height_cm")
    rec_desk  = sol.get("recommended_desk_height_cm")

    def delta_class(delta):
        if delta is None:
            return "metric-delta-zero", "—"
        if delta > 0:
            return "metric-delta-pos", f"+{delta:.1f} cm 높여야 해요"
        elif delta < 0:
            return "metric-delta-neg", f"{delta:.1f} cm 낮춰야 해요"
        else:
            return "metric-delta-zero", "현재 적정"

    chair_delta = round(rec_chair - current_chair, 1) if (rec_chair and current_chair) else None
    desk_delta  = round(rec_desk - current_desk, 1)   if (rec_desk and current_desk) else None

    chair_cls, chair_msg = delta_class(chair_delta)
    desk_cls,  desk_msg  = delta_class(desk_delta)

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-label">의자 높이</div>
            <div class="metric-value">{rec_chair if rec_chair else '—'}<span class="metric-unit">cm</span></div>
            <span class="metric-delta {chair_cls}">{chair_msg}</span>
        </div>
        <div class="metric-card">
            <div class="metric-label">책상 높이</div>
            <div class="metric-value">{rec_desk if rec_desk else '—'}<span class="metric-unit">cm</span></div>
            <span class="metric-delta {desk_cls}">{desk_msg}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if sol.get("explanation"):
        st.markdown(f'<div class="info-box">{sol["explanation"]}</div>', unsafe_allow_html=True)

    # 4) 가구 추천
    st.markdown('<div class="section-label">가구 추천</div>', unsafe_allow_html=True)
    furniture_list = result.get("furniture_recommendation", [])
    furniture_note = result.get("furniture_note", "")

    if furniture_note:
        st.markdown(f'<div class="info-box">{furniture_note}</div>', unsafe_allow_html=True)

    if furniture_list:
        for item in furniture_list:
            url = item.get("url", "")
            coup = item.get("coupang_url", "")
            links_html = ""
            if url and url.startswith("http"):
                links_html += f'<a href="{url}" target="_blank" class="product-link link-primary">공식 사이트 →</a>'
            if coup and coup.startswith("http"):
                links_html += f'<a href="{coup}" target="_blank" class="product-link link-secondary">쿠팡 검색</a>'

            st.markdown(f"""
            <div class="product-card">
                <div>
                    <span class="product-name">{item.get('name', '제품명 없음')}</span>
                    <span class="product-price"> &nbsp;{item.get('price_approx', '')}</span>
                </div>
                <div class="product-reason">{item.get('reason', '')}</div>
                <div class="product-link-row">{links_html}</div>
            </div>
            """, unsafe_allow_html=True)
    elif not furniture_note:
        st.markdown('<div class="info-box">현재 가구 높이 조절만으로 충분히 해결 가능합니다. 별도 구매 불필요 ✓</div>', unsafe_allow_html=True)

    # 5) 모니터 팁
    tips = result.get("monitor_tips", "")
    if tips:
        st.markdown('<div class="section-label">모니터 & 눈 건강 팁</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tip-card">
            <div class="tip-card-title">Monitor Tips</div>
            <p>{tips}</p>
        </div>
        """, unsafe_allow_html=True)


# ── 메인 show() ──────────────────────────────────────────────────────────────
def show():
    inject_css()

    st.set_page_config(
        page_title="척추요정",
        page_icon="🧚",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown("""
    <div class="page-header">
        <div class="page-header-eyebrow">Analysis Result</div>
        <div class="page-header-title">
            척추<span class="page-header-accent">요정</span>
        </div>
    </div>
    <div class="page-sub">분석이 완료되었습니다. 아래 결과를 확인하세요.</div>
    """, unsafe_allow_html=True)

    if "result" not in st.session_state:
        st.warning("분석 결과가 없습니다. 입력 페이지로 돌아갑니다.")
        st.session_state.page = "main"
        st.rerun()
        return

    st.markdown('<div class="done-banner">✓ &nbsp; 분석 완료 — 맞춤 솔루션이 준비되었습니다</div>', unsafe_allow_html=True)

    render_results(
        result=st.session_state.result,
        current_desk=st.session_state.get("desk_h"),
        current_chair=st.session_state.get("chair_h"),
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← 다시 분석하기"):
        del st.session_state.result
        st.session_state.page = "main"
        st.rerun()
