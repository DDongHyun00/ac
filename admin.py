import streamlit as st
import datetime

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
    .block-container {
        max-width: 1100px !important;
        padding: 0 2.5rem 5rem 2.5rem !important;
        margin: 0 auto !important;
    }

    /* ── 상단 네비 ── */
    .admin-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.6rem 0 0 0;
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
        background: rgba(200,240,75,0.12);
        border: 1px solid rgba(200,240,75,0.25);
        padding: 3px 10px;
        border-radius: 999px;
    }

    /* ── 섹션 레이블 ── */
    .section-label {
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 1rem;
        margin-top: 2.8rem;
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
        padding: 1.3rem 1.5rem;
        height: 100%;
    }
    .kpi-label {
        font-size: 0.67rem;
        font-weight: 600;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-family: 'DM Serif Display', serif;
        font-size: 2.5rem;
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
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 0.5rem;
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
    }
    .kpi-up   { background: rgba(200,240,75,0.13); color: #a8d400; }
    .kpi-down { background: rgba(255,100,80,0.12); color: #ff7060; }
    .kpi-neu  { background: rgba(255,255,255,0.06); color: #888; }

    /* ── 바 차트 (CSS-only) ── */
    .bar-wrap {
        background: #1a1a18;
        border: 1px solid #2a2a28;
        border-radius: 14px;
        padding: 1.4rem 1.6rem 1.2rem;
    }
    .bar-chart-title {
        font-size: 0.67rem;
        font-weight: 600;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 1.2rem;
    }
    .bar-row {
        display: flex;
        align-items: center;
        margin-bottom: 0.65rem;
        gap: 10px;
    }
    .bar-label {
        font-size: 0.78rem;
        color: #888;
        min-width: 90px;
        text-align: right;
    }
    .bar-track {
        flex: 1;
        background: #222;
        border-radius: 4px;
        height: 8px;
        overflow: hidden;
    }
    .bar-fill {
        height: 100%;
        border-radius: 4px;
        background: #C8F04B;
    }
    .bar-val {
        font-size: 0.78rem;
        color: #888;
        min-width: 32px;
        text-align: right;
    }

    /* ── 테이블 ── */
    .data-table {
        background: #1a1a18;
        border: 1px solid #2a2a28;
        border-radius: 14px;
        overflow: hidden;
        width: 100%;
    }
    .data-table table {
        width: 100%;
        border-collapse: collapse;
    }
    .data-table thead tr {
        border-bottom: 1px solid #2a2a28;
    }
    .data-table thead th {
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        color: #555;
        padding: 0.85rem 1.2rem;
        text-align: left;
    }
    .data-table tbody tr {
        border-bottom: 1px solid #1e1e1c;
        transition: background 0.12s;
    }
    .data-table tbody tr:last-child { border-bottom: none; }
    .data-table tbody tr:hover { background: #202020; }
    .data-table tbody td {
        font-size: 0.83rem;
        color: #bbb;
        padding: 0.8rem 1.2rem;
        vertical-align: middle;
    }
    .td-name { color: #f0ede6 !important; font-weight: 500; }
    .tag {
        font-size: 0.67rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 999px;
        display: inline-block;
    }
    .tag-neck    { background: rgba(200,240,75,0.13); color: #a8d400; }
    .tag-back    { background: rgba(100,160,255,0.13); color: #7ab0ff; }
    .tag-shoulder{ background: rgba(255,180,50,0.13); color: #ffb432; }
    .tag-eye     { background: rgba(200,100,255,0.13); color: #cc80ff; }
    .tag-pelvis  { background: rgba(255,100,80,0.13); color: #ff7060; }
    .tag-other   { background: rgba(255,255,255,0.07); color: #888; }

    /* ── 인기 제품 카드 ── */
    .product-rank-card {
        background: #1a1a18;
        border: 1px solid #2a2a28;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .rank-num {
        font-family: 'DM Serif Display', serif;
        font-size: 1.6rem;
        color: #333;
        min-width: 30px;
        line-height: 1;
    }
    .rank-num-top { color: #C8F04B; }
    .rank-info { flex: 1; }
    .rank-name {
        font-size: 0.87rem;
        font-weight: 600;
        color: #f0ede6;
        margin-bottom: 0.2rem;
    }
    .rank-category {
        font-size: 0.72rem;
        color: #555;
    }
    .rank-count {
        font-family: 'DM Serif Display', serif;
        font-size: 1.4rem;
        color: #888;
    }

    /* ── 뒤로 버튼 ── */
    .stButton > button {
        background: transparent !important;
        color: #888 !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        padding: 0.4rem 1.1rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        width: auto !important;
        transition: all 0.18s !important;
    }
    .stButton > button:hover {
        border-color: #C8F04B !important;
        color: #C8F04B !important;
        transform: none !important;
    }

    /* ── 도넛 차트 컨테이너 ── */
    .donut-wrap {
        background: #1a1a18;
        border: 1px solid #2a2a28;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
    }
    .donut-chart-title {
        font-size: 0.67rem;
        font-weight: 600;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 1.2rem;
    }
    .legend-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.5rem;
    }
    .legend-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .legend-text {
        font-size: 0.8rem;
        color: #888;
        flex: 1;
    }
    .legend-pct {
        font-size: 0.8rem;
        font-weight: 600;
        color: #ccc;
    }
    </style>
    """, unsafe_allow_html=True)


# ── 하드코딩 데이터 ───────────────────────────────────────────────────────────

# 최근 분석 로그 (30건)
ANALYSIS_LOGS = [
    {"id": "A-0891", "date": "2025-07-18", "height": 172, "weight": 68, "complaints": ["허리 통증", "어깨 통증"], "recommended_chair": 43, "recommended_desk": 73, "has_photo": True},
    {"id": "A-0890", "date": "2025-07-18", "height": 158, "weight": 52, "complaints": ["목 통증", "눈 피로"], "recommended_chair": 39, "recommended_desk": 66, "has_photo": False},
    {"id": "A-0889", "date": "2025-07-17", "height": 180, "weight": 80, "complaints": ["허리 통증"], "recommended_chair": 45, "recommended_desk": 76, "has_photo": True},
    {"id": "A-0888", "date": "2025-07-17", "height": 165, "weight": 60, "complaints": ["어깨 통증", "두통"], "recommended_chair": 41, "recommended_desk": 70, "has_photo": False},
    {"id": "A-0887", "date": "2025-07-17", "height": 177, "weight": 74, "complaints": ["골반 통증", "허리 통증"], "recommended_chair": 44, "recommended_desk": 75, "has_photo": True},
    {"id": "A-0886", "date": "2025-07-16", "height": 162, "weight": 55, "complaints": ["목 통증"], "recommended_chair": 40, "recommended_desk": 68, "has_photo": False},
    {"id": "A-0885", "date": "2025-07-16", "height": 170, "weight": 63, "complaints": ["눈 피로", "두통"], "recommended_chair": 42, "recommended_desk": 72, "has_photo": True},
    {"id": "A-0884", "date": "2025-07-16", "height": 183, "weight": 85, "complaints": ["허리 통증", "골반 통증", "어깨 통증"], "recommended_chair": 46, "recommended_desk": 78, "has_photo": True},
    {"id": "A-0883", "date": "2025-07-15", "height": 155, "weight": 48, "complaints": ["목 통증", "어깨 통증"], "recommended_chair": 38, "recommended_desk": 65, "has_photo": False},
    {"id": "A-0882", "date": "2025-07-15", "height": 168, "weight": 70, "complaints": ["손목/팔 저림", "어깨 통증"], "recommended_chair": 42, "recommended_desk": 71, "has_photo": False},
    {"id": "A-0881", "date": "2025-07-15", "height": 175, "weight": 72, "complaints": ["허리 통증"], "recommended_chair": 43, "recommended_desk": 74, "has_photo": True},
    {"id": "A-0880", "date": "2025-07-14", "height": 160, "weight": 54, "complaints": ["눈 피로"], "recommended_chair": 40, "recommended_desk": 67, "has_photo": False},
    {"id": "A-0879", "date": "2025-07-14", "height": 178, "weight": 78, "complaints": ["허리 통증", "목 통증"], "recommended_chair": 44, "recommended_desk": 76, "has_photo": True},
    {"id": "A-0878", "date": "2025-07-14", "height": 166, "weight": 61, "complaints": ["두통", "눈 피로"], "recommended_chair": 41, "recommended_desk": 70, "has_photo": False},
    {"id": "A-0877", "date": "2025-07-13", "height": 171, "weight": 66, "complaints": ["어깨 통증"], "recommended_chair": 42, "recommended_desk": 73, "has_photo": True},
]

# 주간 분석 수 (최근 7일)
WEEKLY_COUNTS = [
    ("07/12", 18), ("07/13", 24), ("07/14", 31), ("07/15", 29),
    ("07/16", 38), ("07/17", 42), ("07/18", 35),
]

# 불편사항 분포
COMPLAINT_DIST = [
    ("허리 통증", 41, "#7ab0ff"),
    ("목 통증",   28, "#C8F04B"),
    ("어깨 통증", 22, "#ffb432"),
    ("눈 피로",   17, "#cc80ff"),
    ("골반 통증", 12, "#ff7060"),
    ("두통",       9, "#60d4c8"),
    ("기타",       8, "#555"),
]

# 추천 제품 순위
PRODUCT_RANKS = [
    ("시디즈 T50 HF", "의자", 84),
    ("시디즈 T50 HLDA", "의자", 61),
    ("카멜마운트 CA-1 모니터암", "모니터암", 47),
    ("데스커 알파 모션 스탠딩", "책상", 39),
    ("메모리폼 허리쿠션", "허리쿠션", 28),
]

# ── 불편사항 태그 CSS 클래스 매핑 ────────────────────────────────────────────
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


# ── 렌더링 ─────────────────────────────────────────────────────────────────
def show():
    inject_css()

    st.set_page_config(
        page_title="척추요정 · 관리자",
        page_icon="🧚",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # ── 상단 바 ──
    col_logo, col_back = st.columns([6, 1])
    with col_logo:
        st.markdown("""
        <div class="admin-topbar">
            <div class="admin-logo">척추<span>요정</span></div>
            <div class="admin-badge">Admin Dashboard</div>
        </div>
        """, unsafe_allow_html=True)
    with col_back:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("← 메인으로"):
            st.session_state.page = "main"
            st.rerun()

    # ── KPI 카드 ──
    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        (k1, "누적 분석 수",    "891",  "건", "+12%", "kpi-up",  "이번 달 기준"),
        (k2, "이번 주 분석",    "217",  "건", "+8%",  "kpi-up",  "전주 대비"),
        (k3, "사진 업로드율",   "54",   "%",  "−3%",  "kpi-down","전주 대비"),
        (k4, "평균 응답 시간",  "4.2",  "초", "±0",   "kpi-neu", "GPT-4o 기준"),
    ]
    for col, label, val, unit, delta, delta_cls, sub in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}<span class="kpi-unit">{unit}</span></div>
                <span class="kpi-delta {delta_cls}">{delta} &nbsp;{sub}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── 주간 분석 바 차트 + 불편사항 분포 ──
    st.markdown('<div class="section-label">Analytics</div>', unsafe_allow_html=True)

    chart_col, dist_col = st.columns([3, 2])

    with chart_col:
        max_val = max(v for _, v in WEEKLY_COUNTS)
        bars_html = ""
        for day, cnt in WEEKLY_COUNTS:
            pct = round(cnt / max_val * 100)
            bars_html += f"""
            <div class="bar-row">
                <div class="bar-label">{day}</div>
                <div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>
                <div class="bar-val">{cnt}</div>
            </div>"""
        st.markdown(f"""
        <div class="bar-wrap">
            <div class="bar-chart-title">일별 분석 요청 수 (최근 7일)</div>
            {bars_html}
        </div>
        """, unsafe_allow_html=True)

    with dist_col:
        total_complaints = sum(v for _, v, _ in COMPLAINT_DIST)
        legend_html = ""
        for label, cnt, color in COMPLAINT_DIST:
            pct = round(cnt / total_complaints * 100)
            legend_html += f"""
            <div class="legend-row">
                <div class="legend-dot" style="background:{color}"></div>
                <div class="legend-text">{label}</div>
                <div class="legend-pct">{pct}%</div>
            </div>"""
        st.markdown(f"""
        <div class="donut-wrap">
            <div class="donut-chart-title">불편사항 분포 (누적)</div>
            {legend_html}
        </div>
        """, unsafe_allow_html=True)

    # ── 추천 제품 순위 ──
    st.markdown('<div class="section-label">Top Recommended Products</div>', unsafe_allow_html=True)

    max_cnt = PRODUCT_RANKS[0][2]
    for i, (name, category, cnt) in enumerate(PRODUCT_RANKS):
        rank_cls = "rank-num-top" if i == 0 else ""
        pct = round(cnt / max_cnt * 100)
        st.markdown(f"""
        <div class="product-rank-card">
            <div class="rank-num {rank_cls}">0{i+1}</div>
            <div class="rank-info">
                <div class="rank-name">{name}</div>
                <div class="rank-category">{category}</div>
                <div style="margin-top:0.5rem; background:#222; border-radius:4px; height:4px; overflow:hidden;">
                    <div style="width:{pct}%; height:100%; background:#C8F04B; border-radius:4px;"></div>
                </div>
            </div>
            <div class="rank-count">{cnt}<span style="font-family:'DM Sans',sans-serif;font-size:0.72rem;color:#555;margin-left:3px;">건</span></div>
        </div>
        """, unsafe_allow_html=True)

    # ── 최근 분석 로그 ──
    st.markdown('<div class="section-label">Recent Analysis Logs</div>', unsafe_allow_html=True)

    header_html = """
    <div class="data-table">
    <table>
    <thead><tr>
        <th>ID</th><th>날짜</th><th>키 / 몸무게</th>
        <th>주요 불편사항</th><th>권장 의자</th><th>권장 책상</th><th>사진</th>
    </tr></thead>
    <tbody>
    """
    rows_html = ""
    for row in ANALYSIS_LOGS:
        tags = "".join(
            f'<span class="tag {TAG_CLASS.get(c, "tag-other")}">{c}</span> '
            for c in row["complaints"][:2]
        )
        photo = '<span style="color:#C8F04B;">✓</span>' if row["has_photo"] else '<span style="color:#333;">—</span>'
        rows_html += f"""
        <tr>
            <td class="td-name">{row['id']}</td>
            <td>{row['date']}</td>
            <td>{row['height']}cm / {row['weight']}kg</td>
            <td>{tags}</td>
            <td>{row['recommended_chair']} cm</td>
            <td>{row['recommended_desk']} cm</td>
            <td>{photo}</td>
        </tr>"""

    st.markdown(header_html + rows_html + "</tbody></table></div>", unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align:right;font-size:0.72rem;color:#444;margin-top:0.8rem;">최근 15건 표시 중 · 총 891건</div>',
        unsafe_allow_html=True,
    )
