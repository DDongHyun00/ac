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
        background-color: #111110;
    }
    .stApp > header { background: transparent !important; }
    .block-container {
        max-width: 1100px !important;
        padding: 4rem 2.5rem 5rem 2.5rem !important;
        margin: 0 auto !important;
    }

    /* ── 상단 바 ── */
    .admin-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid #2a2a28;
        margin-bottom: 2.8rem;
    }
    .admin-logo {
        font-family: 'DM Serif Display', serif;
        font-size: 1.35rem;
        color: #f5f2ec;
        letter-spacing: -0.01em;
    }
    .admin-logo span {
        display: inline-block;
        background: #C8F04B;
        color: #111110;
        padding: 1px 7px;
        border-radius: 4px;
        margin-left: 2px;
    }
    .admin-badge {
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #C8F04B;
        background: rgba(200,240,75,0.10);
        border: 1px solid rgba(200,240,75,0.22);
        padding: 4px 12px;
        border-radius: 999px;
    }

    /* ── 섹션 레이블 ── */
    .section-label {
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #444;
        margin-bottom: 1rem;
        margin-top: 2.6rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: #222;
    }

    /* ── KPI 카드 ── */
    .kpi-card {
        background: #1a1a18;
        border: 1px solid #2a2a28;
        border-radius: 14px;
        padding: 1.3rem 1.5rem 1.2rem;
    }
    .kpi-label {
        font-size: 0.67rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-family: 'DM Serif Display', serif;
        font-size: 2.6rem;
        color: #f5f2ec;
        line-height: 1;
        letter-spacing: -0.02em;
    }
    .kpi-unit {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        color: #555;
        margin-left: 3px;
    }
    .kpi-delta {
        font-size: 0.74rem;
        font-weight: 500;
        margin-top: 0.55rem;
        display: inline-block;
        padding: 2px 9px;
        border-radius: 999px;
    }
    .kpi-up   { background: rgba(200,240,75,0.13); color: #a8d400; }
    .kpi-down { background: rgba(255,100,80,0.12); color: #ff7060; }
    .kpi-neu  { background: rgba(255,255,255,0.06); color: #666; }

    /* ── 차트 래퍼 ── */
    .chart-wrap {
        background: #1a1a18;
        border: 1px solid #2a2a28;
        border-radius: 14px;
        padding: 1.4rem 1.6rem 1.3rem;
    }
    .chart-title {
        font-size: 0.67rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 1.3rem;
    }

    /* ── 바 차트 ── */
    .bar-row {
        display: flex;
        align-items: center;
        margin-bottom: 0.65rem;
        gap: 10px;
    }
    .bar-label { font-size: 0.76rem; color: #666; min-width: 38px; text-align: right; }
    .bar-track  { flex: 1; background: #222; border-radius: 4px; height: 7px; overflow: hidden; }
    .bar-fill   { height: 100%; border-radius: 4px; background: #C8F04B; }
    .bar-val    { font-size: 0.76rem; color: #666; min-width: 24px; text-align: right; }

    /* ── 범례 ── */
    .legend-row {
        display: flex;
        align-items: center;
        gap: 9px;
        margin-bottom: 0.65rem;
    }
    .legend-dot  { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .legend-text { font-size: 0.8rem; color: #888; flex: 1; }
    .legend-bar-track { width: 70px; background: #222; border-radius: 3px; height: 5px; overflow: hidden; }
    .legend-pct  { font-size: 0.78rem; font-weight: 600; color: #bbb; min-width: 30px; text-align: right; }

    /* ── 추천 제품 카드 ── */
    .product-rank-card {
        background: #1a1a18;
        border: 1px solid #2a2a28;
        border-radius: 14px;
        padding: 1rem 1.3rem;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .rank-num     { font-family: 'DM Serif Display', serif; font-size: 1.5rem; color: #2e2e2c; min-width: 32px; line-height: 1; }
    .rank-num-top { color: #C8F04B !important; }
    .rank-info    { flex: 1; }
    .rank-name    { font-size: 0.87rem; font-weight: 600; color: #f0ede6; margin-bottom: 0.15rem; }
    .rank-cat     { font-size: 0.72rem; color: #555; margin-bottom: 0.45rem; }
    .rank-bar-track { background: #222; border-radius: 3px; height: 4px; overflow: hidden; }
    .rank-bar-fill  { height: 100%; border-radius: 3px; background: #C8F04B; }
    .rank-count   { font-family: 'DM Serif Display', serif; font-size: 1.5rem; color: #555; white-space: nowrap; }
    .rank-count span { font-family: 'DM Sans', sans-serif; font-size: 0.72rem; color: #444; margin-left: 2px; }

    /* ── 로그 테이블 ── */
    .log-table { background: #1a1a18; border: 1px solid #2a2a28; border-radius: 14px; overflow: hidden; width: 100%; }
    .log-table table { width: 100%; border-collapse: collapse; }
    .log-table thead tr { border-bottom: 1px solid #252523; }
    .log-table thead th {
        font-size: 0.63rem; font-weight: 600; letter-spacing: 0.12em;
        text-transform: uppercase; color: #444;
        padding: 0.85rem 1.1rem; text-align: left; white-space: nowrap;
    }
    .log-table tbody tr { border-bottom: 1px solid #1e1e1c; }
    .log-table tbody tr:last-child { border-bottom: none; }
    .log-table tbody td { font-size: 0.82rem; color: #888; padding: 0.75rem 1.1rem; vertical-align: middle; }
    .td-id   { color: #f0ede6 !important; font-weight: 600; font-size: 0.78rem !important; }
    .td-body { color: #bbb !important; }
    .tag {
        font-size: 0.65rem; font-weight: 600; padding: 2px 7px;
        border-radius: 999px; display: inline-block; margin-right: 3px;
    }
    .tag-back     { background: rgba(100,160,255,0.13); color: #7ab0ff; }
    .tag-neck     { background: rgba(200,240,75,0.12);  color: #a8d400; }
    .tag-shoulder { background: rgba(255,180,50,0.12);  color: #ffb432; }
    .tag-eye      { background: rgba(200,100,255,0.12); color: #cc80ff; }
    .tag-pelvis   { background: rgba(255,100,80,0.12);  color: #ff7060; }
    .tag-other    { background: rgba(255,255,255,0.07); color: #666; }
    .photo-yes { color: #C8F04B; font-weight: 600; }
    .photo-no  { color: #2e2e2c; }
    .table-footer { text-align: right; font-size: 0.7rem; color: #333; margin-top: 0.7rem; }

    /* ── 뒤로 가기 버튼 ── */
    .stButton > button {
        background: transparent !important;
        color: #666 !important;
        border: 1px solid #2a2a28 !important;
        border-radius: 8px !important;
        padding: 0.38rem 1rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.04em !important;
        width: auto !important;
        transition: all 0.18s !important;
    }
    .stButton > button:hover {
        border-color: #C8F04B !important;
        color: #C8F04B !important;
        transform: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ── 데이터 ───────────────────────────────────────────────────────────────────
ANALYSIS_LOGS = [
    {"id": "A-0891", "date": "2025-07-18", "height": 172, "weight": 68,  "complaints": ["허리 통증", "어깨 통증"], "chair": 43, "desk": 73, "photo": True},
    {"id": "A-0890", "date": "2025-07-18", "height": 158, "weight": 52,  "complaints": ["목 통증", "눈 피로"],    "chair": 39, "desk": 66, "photo": False},
    {"id": "A-0889", "date": "2025-07-17", "height": 180, "weight": 80,  "complaints": ["허리 통증"],             "chair": 45, "desk": 76, "photo": True},
    {"id": "A-0888", "date": "2025-07-17", "height": 165, "weight": 60,  "complaints": ["어깨 통증", "두통"],     "chair": 41, "desk": 70, "photo": False},
    {"id": "A-0887", "date": "2025-07-17", "height": 177, "weight": 74,  "complaints": ["골반 통증", "허리 통증"],"chair": 44, "desk": 75, "photo": True},
    {"id": "A-0886", "date": "2025-07-16", "height": 162, "weight": 55,  "complaints": ["목 통증"],               "chair": 40, "desk": 68, "photo": False},
    {"id": "A-0885", "date": "2025-07-16", "height": 170, "weight": 63,  "complaints": ["눈 피로", "두통"],       "chair": 42, "desk": 72, "photo": True},
    {"id": "A-0884", "date": "2025-07-16", "height": 183, "weight": 85,  "complaints": ["허리 통증", "골반 통증"],"chair": 46, "desk": 78, "photo": True},
    {"id": "A-0883", "date": "2025-07-15", "height": 155, "weight": 48,  "complaints": ["목 통증", "어깨 통증"],  "chair": 38, "desk": 65, "photo": False},
    {"id": "A-0882", "date": "2025-07-15", "height": 168, "weight": 70,  "complaints": ["손목/팔 저림"],          "chair": 42, "desk": 71, "photo": False},
    {"id": "A-0881", "date": "2025-07-15", "height": 175, "weight": 72,  "complaints": ["허리 통증"],             "chair": 43, "desk": 74, "photo": True},
    {"id": "A-0880", "date": "2025-07-14", "height": 160, "weight": 54,  "complaints": ["눈 피로"],               "chair": 40, "desk": 67, "photo": False},
    {"id": "A-0879", "date": "2025-07-14", "height": 178, "weight": 78,  "complaints": ["허리 통증", "목 통증"],  "chair": 44, "desk": 76, "photo": True},
    {"id": "A-0878", "date": "2025-07-14", "height": 166, "weight": 61,  "complaints": ["두통", "눈 피로"],       "chair": 41, "desk": 70, "photo": False},
    {"id": "A-0877", "date": "2025-07-13", "height": 171, "weight": 66,  "complaints": ["어깨 통증"],             "chair": 42, "desk": 73, "photo": True},
]

WEEKLY_COUNTS = [
    ("07/12", 18), ("07/13", 24), ("07/14", 31),
    ("07/15", 29), ("07/16", 38), ("07/17", 42), ("07/18", 35),
]

COMPLAINT_DIST = [
    ("허리 통증", 41, "#7ab0ff"),
    ("목 통증",   28, "#C8F04B"),
    ("어깨 통증", 22, "#ffb432"),
    ("눈 피로",   17, "#cc80ff"),
    ("골반 통증", 12, "#ff7060"),
    ("두통",       9, "#60d4c8"),
    ("기타",       8, "#444"),
]

PRODUCT_RANKS = [
    ("시디즈 T50 HF",           "의자",     84),
    ("시디즈 T50 HLDA",          "의자",     61),
    ("카멜마운트 CA-1 모니터암",  "모니터암", 47),
    ("데스커 알파 모션 스탠딩",   "책상",     39),
    ("메모리폼 허리쿠션",         "허리쿠션", 28),
]

TAG_CLASS = {
    "허리 통증": "tag-back", "목 통증": "tag-neck",
    "어깨 통증": "tag-shoulder", "눈 피로": "tag-eye",
    "골반 통증": "tag-pelvis", "두통": "tag-other",
    "손목/팔 저림": "tag-other", "기타": "tag-other",
}


# ── show() ───────────────────────────────────────────────────────────────────
def show():
    inject_css()

    st.set_page_config(
        page_title="척추요정 · 관리자",
        page_icon="🧚",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # ── 상단 바 ──
    logo_col, back_col = st.columns([9, 1])
    with logo_col:
        st.markdown("""
        <div class="admin-topbar">
            <div class="admin-logo">척추<span>요정</span></div>
            <div class="admin-badge">Admin Dashboard</div>
        </div>
        """, unsafe_allow_html=True)
    with back_col:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← 메인"):
            st.session_state.page = "main"
            st.rerun()

    # ── KPI ──
    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        (k1, "누적 분석 수",   "891", "건", "+12%", "kpi-up",  "이번 달 기준"),
        (k2, "이번 주 분석",   "217", "건", "+8%",  "kpi-up",  "전주 대비"),
        (k3, "사진 업로드율",  "54",  "%",  "−3%",  "kpi-down","전주 대비"),
        (k4, "평균 응답 시간", "4.2", "초", "±0",   "kpi-neu", "GPT-4o 기준"),
    ]
    for col, label, val, unit, delta, dcls, sub in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}<span class="kpi-unit">{unit}</span></div>
                <span class="kpi-delta {dcls}">{delta}&nbsp; {sub}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── 차트 영역 ──
    st.markdown('<div class="section-label">Analytics</div>', unsafe_allow_html=True)
    chart_col, dist_col = st.columns([3, 2])

    with chart_col:
        max_v = max(v for _, v in WEEKLY_COUNTS)
        bars_html = ""
        for day, cnt in WEEKLY_COUNTS:
            pct = round(cnt / max_v * 100)
            bars_html += (
                f'<div class="bar-row">'
                f'  <div class="bar-label">{day}</div>'
                f'  <div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>'
                f'  <div class="bar-val">{cnt}</div>'
                f'</div>'
            )
        st.markdown(
            f'<div class="chart-wrap"><div class="chart-title">일별 분석 요청 수 (최근 7일)</div>{bars_html}</div>',
            unsafe_allow_html=True,
        )

    with dist_col:
        total = sum(v for _, v, _ in COMPLAINT_DIST)
        legends_html = ""
        for label, cnt, color in COMPLAINT_DIST:
            pct = round(cnt / total * 100)
            legends_html += (
                f'<div class="legend-row">'
                f'  <div class="legend-dot" style="background:{color}"></div>'
                f'  <div class="legend-text">{label}</div>'
                f'  <div class="legend-bar-track">'
                f'    <div style="width:{pct}%;height:100%;background:{color};border-radius:3px;"></div>'
                f'  </div>'
                f'  <div class="legend-pct">{pct}%</div>'
                f'</div>'
            )
        st.markdown(
            f'<div class="chart-wrap"><div class="chart-title">불편사항 분포 (누적)</div>{legends_html}</div>',
            unsafe_allow_html=True,
        )

    # ── 추천 제품 순위 ──
    st.markdown('<div class="section-label">Top Recommended Products</div>', unsafe_allow_html=True)
    max_cnt = PRODUCT_RANKS[0][2]
    for i, (name, cat, cnt) in enumerate(PRODUCT_RANKS):
        rank_cls = "rank-num-top" if i == 0 else ""
        pct = round(cnt / max_cnt * 100)
        st.markdown(f"""
        <div class="product-rank-card">
            <div class="rank-num {rank_cls}">0{i+1}</div>
            <div class="rank-info">
                <div class="rank-name">{name}</div>
                <div class="rank-cat">{cat}</div>
                <div class="rank-bar-track"><div class="rank-bar-fill" style="width:{pct}%"></div></div>
            </div>
            <div class="rank-count">{cnt}<span>건</span></div>
        </div>
        """, unsafe_allow_html=True)

    # ── 로그 테이블 ──
    st.markdown('<div class="section-label">Recent Analysis Logs</div>', unsafe_allow_html=True)

    rows_html = ""
    for row in ANALYSIS_LOGS:
        tags_html = "".join(
            f'<span class="tag {TAG_CLASS.get(c, "tag-other")}">{c}</span>'
            for c in row["complaints"][:2]
        )
        photo_html = '<span class="photo-yes">✓</span>' if row["photo"] else '<span class="photo-no">—</span>'
        rows_html += (
            f'<tr>'
            f'  <td class="td-id">{row["id"]}</td>'
            f'  <td class="td-body">{row["date"]}</td>'
            f'  <td class="td-body">{row["height"]}cm / {row["weight"]}kg</td>'
            f'  <td>{tags_html}</td>'
            f'  <td class="td-body">{row["chair"]} cm</td>'
            f'  <td class="td-body">{row["desk"]} cm</td>'
            f'  <td>{photo_html}</td>'
            f'</tr>'
        )

    st.markdown(f"""
    <div class="log-table">
        <table>
            <thead><tr>
                <th>ID</th><th>날짜</th><th>키 / 몸무게</th>
                <th>불편사항</th><th>권장 의자</th><th>권장 책상</th><th>사진</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    <div class="table-footer">최근 15건 표시 중 &nbsp;·&nbsp; 총 891건</div>
    """, unsafe_allow_html=True)
