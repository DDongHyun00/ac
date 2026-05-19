import streamlit as st


# ── CSS ──────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── 배경 & 레이아웃 ── */
    .stApp { background-color: #F5F2EC; }
    .stApp > header { background: transparent !important; }
    .block-container {
        max-width: 1060px !important;
        padding: 4rem 2rem 5rem 2rem !important;
        margin: 0 auto !important;
    }

    /* ── 페이지 헤더 ── */
    .page-header {
        padding: 3.5rem 0 0.4rem 0;
        border-bottom: 2px solid #1a1a1a;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
    }
    .page-header-left {}
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
        padding: 0 6px;
        border-radius: 4px;
    }
    .admin-badge {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #1a1a1a;
        background: #C8F04B;
        padding: 4px 12px;
        border-radius: 999px;
        margin-bottom: 0.6rem;
        display: inline-block;
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

    /* ── KPI 카드 ── */
    .kpi-card {
        background: #fff;
        border-radius: 14px;
        padding: 1.3rem 1.5rem 1.2rem;
        border: 1.5px solid #ede9e0;
        height: 100%;
    }
    .kpi-label {
        font-size: 0.67rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #aaa;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-family: 'DM Serif Display', serif;
        font-size: 2.6rem;
        color: #1a1a1a;
        line-height: 1;
        letter-spacing: -0.02em;
    }
    .kpi-unit {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        color: #aaa;
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
    .kpi-up   { background: #f0fde8; color: #4a8c1c; }
    .kpi-down { background: #fff3e8; color: #b85c00; }
    .kpi-neu  { background: #f0f0f0; color: #888; }

    /* ── 차트 래퍼 ── */
    .chart-wrap {
        background: #fff;
        border-radius: 14px;
        padding: 1.4rem 1.6rem 1.3rem;
        border: 1.5px solid #ede9e0;
    }
    .chart-title {
        font-size: 0.67rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #aaa;
        margin-bottom: 1.3rem;
    }

    /* ── 바 차트 ── */
    .bar-row {
        display: flex;
        align-items: center;
        margin-bottom: 0.65rem;
        gap: 10px;
    }
    .bar-label { font-size: 0.76rem; color: #aaa; min-width: 38px; text-align: right; }
    .bar-track  { flex: 1; background: #f0ede6; border-radius: 4px; height: 7px; overflow: hidden; }
    .bar-fill   { height: 100%; border-radius: 4px; background: #1a1a1a; }
    .bar-val    { font-size: 0.76rem; color: #888; min-width: 24px; text-align: right; font-weight: 600; }

    /* ── 범례 ── */
    .legend-row {
        display: flex;
        align-items: center;
        gap: 9px;
        margin-bottom: 0.65rem;
    }
    .legend-dot  { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .legend-text { font-size: 0.8rem; color: #555; flex: 1; }
    .legend-bar-track { width: 70px; background: #f0ede6; border-radius: 3px; height: 5px; overflow: hidden; }
    .legend-pct  { font-size: 0.78rem; font-weight: 600; color: #333; min-width: 30px; text-align: right; }

    /* ── 추천 제품 순위 카드 ── */
    .product-rank-card {
        background: #fff;
        border: 1.5px solid #ede9e0;
        border-radius: 14px;
        padding: 1rem 1.3rem;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .rank-num {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: #ddd;
        min-width: 32px;
        line-height: 1;
    }
    .rank-num-top { color: #1a1a1a !important; }
    .rank-info    { flex: 1; }
    .rank-name    { font-size: 0.87rem; font-weight: 600; color: #1a1a1a; margin-bottom: 0.15rem; }
    .rank-cat     { font-size: 0.72rem; color: #aaa; margin-bottom: 0.45rem; }
    .rank-bar-track { background: #f0ede6; border-radius: 3px; height: 4px; overflow: hidden; }
    .rank-bar-fill  { height: 100%; border-radius: 3px; background: #C8F04B; }
    .rank-count {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: #bbb;
        white-space: nowrap;
    }
    .rank-count span { font-family: 'DM Sans', sans-serif; font-size: 0.72rem; color: #bbb; margin-left: 2px; }

    /* ── 로그 테이블 ── */
    .log-table {
        background: #fff;
        border: 1.5px solid #ede9e0;
        border-radius: 14px;
        overflow: hidden;
        width: 100%;
    }
    .log-table table { width: 100%; border-collapse: collapse; }
    .log-table thead tr { border-bottom: 1.5px solid #f0ede6; }
    .log-table thead th {
        font-size: 0.63rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #aaa;
        padding: 0.85rem 1.2rem;
        text-align: left;
        white-space: nowrap;
    }
    .log-table tbody tr { border-bottom: 1px solid #f7f5f0; transition: background 0.12s; }
    .log-table tbody tr:last-child { border-bottom: none; }
    .log-table tbody tr:hover { background: #faf8f4; }
    .log-table tbody td { font-size: 0.82rem; color: #888; padding: 0.78rem 1.2rem; vertical-align: middle; }
    .td-id   { color: #1a1a1a !important; font-weight: 600; font-size: 0.78rem !important; }
    .td-body { color: #555 !important; }
    .tag {
        font-size: 0.65rem; font-weight: 600; padding: 2px 8px;
        border-radius: 999px; display: inline-block; margin-right: 3px;
    }
    .tag-back     { background: #e8f0ff; color: #3b6fd4; }
    .tag-neck     { background: #f0fde8; color: #4a8c1c; }
    .tag-shoulder { background: #fff7e6; color: #b06d00; }
    .tag-eye      { background: #f5eeff; color: #7c3aed; }
    .tag-pelvis   { background: #fff0ee; color: #c0392b; }
    .tag-other    { background: #f0f0f0; color: #888; }
    .photo-yes { color: #4a8c1c; font-weight: 700; }
    .photo-no  { color: #ddd; }
    .table-footer {
        text-align: right;
        font-size: 0.72rem;
        color: #bbb;
        margin-top: 0.7rem;
    }

    /* ── 완료 배너 ── */
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

    /* ── 뒤로 가기 버튼 ── */
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
    </style>
    """, unsafe_allow_html=True)


# ── 데이터 ───────────────────────────────────────────────────────────────────
ANALYSIS_LOGS = [
    {"id": "A-0891", "date": "2025-07-18", "height": 172, "weight": 68,  "complaints": ["허리 통증", "어깨 통증"], "chair": 43, "desk": 73, "photo": True},
    {"id": "A-0890", "date": "2025-07-18", "height": 158, "weight": 52,  "complaints": ["목 통증", "눈 피로"],     "chair": 39, "desk": 66, "photo": False},
    {"id": "A-0889", "date": "2025-07-17", "height": 180, "weight": 80,  "complaints": ["허리 통증"],              "chair": 45, "desk": 76, "photo": True},
    {"id": "A-0888", "date": "2025-07-17", "height": 165, "weight": 60,  "complaints": ["어깨 통증", "두통"],      "chair": 41, "desk": 70, "photo": False},
    {"id": "A-0887", "date": "2025-07-17", "height": 177, "weight": 74,  "complaints": ["골반 통증", "허리 통증"], "chair": 44, "desk": 75, "photo": True},
    {"id": "A-0886", "date": "2025-07-16", "height": 162, "weight": 55,  "complaints": ["목 통증"],                "chair": 40, "desk": 68, "photo": False},
    {"id": "A-0885", "date": "2025-07-16", "height": 170, "weight": 63,  "complaints": ["눈 피로", "두통"],        "chair": 42, "desk": 72, "photo": True},
    {"id": "A-0884", "date": "2025-07-16", "height": 183, "weight": 85,  "complaints": ["허리 통증", "골반 통증"], "chair": 46, "desk": 78, "photo": True},
    {"id": "A-0883", "date": "2025-07-15", "height": 155, "weight": 48,  "complaints": ["목 통증", "어깨 통증"],   "chair": 38, "desk": 65, "photo": False},
    {"id": "A-0882", "date": "2025-07-15", "height": 168, "weight": 70,  "complaints": ["손목/팔 저림"],           "chair": 42, "desk": 71, "photo": False},
    {"id": "A-0881", "date": "2025-07-15", "height": 175, "weight": 72,  "complaints": ["허리 통증"],              "chair": 43, "desk": 74, "photo": True},
    {"id": "A-0880", "date": "2025-07-14", "height": 160, "weight": 54,  "complaints": ["눈 피로"],                "chair": 40, "desk": 67, "photo": False},
    {"id": "A-0879", "date": "2025-07-14", "height": 178, "weight": 78,  "complaints": ["허리 통증", "목 통증"],   "chair": 44, "desk": 76, "photo": True},
    {"id": "A-0878", "date": "2025-07-14", "height": 166, "weight": 61,  "complaints": ["두통", "눈 피로"],        "chair": 41, "desk": 70, "photo": False},
    {"id": "A-0877", "date": "2025-07-13", "height": 171, "weight": 66,  "complaints": ["어깨 통증"],              "chair": 42, "desk": 73, "photo": True},
]

WEEKLY_COUNTS = [
    ("07/12", 18), ("07/13", 24), ("07/14", 31),
    ("07/15", 29), ("07/16", 38), ("07/17", 42), ("07/18", 35),
]

COMPLAINT_DIST = [
    ("허리 통증", 41, "#3b6fd4"),
    ("목 통증",   28, "#4a8c1c"),
    ("어깨 통증", 22, "#b06d00"),
    ("눈 피로",   17, "#7c3aed"),
    ("골반 통증", 12, "#c0392b"),
    ("두통",       9, "#0e9488"),
    ("기타",       8, "#aaa"),
]

PRODUCT_RANKS = [
    ("시디즈 T50 HF",           "의자",     84),
    ("시디즈 T50 HLDA",          "의자",     61),
    ("카멜마운트 CA-1 모니터암",  "모니터암", 47),
    ("데스커 알파 모션 스탠딩",   "책상",     39),
    ("메모리폼 허리쿠션",         "허리쿠션", 28),
]

TAG_CLASS = {
    "허리 통증": "tag-back",
    "목 통증": "tag-neck",
    "어깨 통증": "tag-shoulder",
    "눈 피로": "tag-eye",
    "골반 통증": "tag-pelvis",
    "두통": "tag-other",
    "손목/팔 저림": "tag-other",
    "기타": "tag-other",
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

    # ── 페이지 헤더 ──
    st.markdown("""
    <div class="page-header">
        <div class="page-header-left">
            <div class="page-header-eyebrow">Admin Dashboard</div>
            <div class="page-header-title">
                척추<span class="page-header-accent">요정</span>
            </div>
        </div>
        <div class="admin-badge">관리자 모드</div>
    </div>
    <div class="page-sub">서비스 현황 및 분석 데이터를 확인합니다</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="done-banner">✓ &nbsp; 데이터 기준일: 2026-05-19 &nbsp;·&nbsp; 총 891건 누적</div>', unsafe_allow_html=True)

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

    # ── 차트 ──
    st.markdown('<div class="section-label">Analytics</div>', unsafe_allow_html=True)
    chart_col, dist_col = st.columns([3, 2])

    with chart_col:
        max_v = max(v for _, v in WEEKLY_COUNTS)
        bars_html = ""
        for day, cnt in WEEKLY_COUNTS:
            pct = round(cnt / max_v * 100)
            bars_html += (
                f'<div class="bar-row">'
                f'<div class="bar-label">{day}</div>'
                f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>'
                f'<div class="bar-val">{cnt}</div>'
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
                f'<div class="legend-dot" style="background:{color}"></div>'
                f'<div class="legend-text">{label}</div>'
                f'<div class="legend-bar-track">'
                f'<div style="width:{pct}%;height:100%;background:{color};border-radius:3px;"></div>'
                f'</div>'
                f'<div class="legend-pct">{pct}%</div>'
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
            f'<td class="td-id">{row["id"]}</td>'
            f'<td class="td-body">{row["date"]}</td>'
            f'<td class="td-body">{row["height"]}cm / {row["weight"]}kg</td>'
            f'<td>{tags_html}</td>'
            f'<td class="td-body">{row["chair"]} cm</td>'
            f'<td class="td-body">{row["desk"]} cm</td>'
            f'<td>{photo_html}</td>'
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

    # ── 뒤로 가기 ──
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← 메인으로"):
        st.session_state.page = "main"
        st.rerun()