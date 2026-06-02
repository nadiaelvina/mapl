import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from itertools import combinations

st.set_page_config(
    page_title="MAPL+ | Portfolio Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .main { background: #0f0f12; }
    .stApp { background: #0f0f12; }

    section[data-testid="stSidebar"] {
        background: #16161a;
        border-right: 1px solid #2a2a35;
    }
    section[data-testid="stSidebar"] * { color: #c8c8d4 !important; }

    .block-container { padding: 2rem 2.5rem; max-width: 1400px; }

    h1, h2, h3 { color: #f0f0f5 !important; }
    p, span, div { color: #a8a8b8; }

    .metric-card {
        background: #16161a;
        border: 1px solid #2a2a35;
        border-radius: 12px;
        padding: 20px 24px;
    }
    .metric-value { font-size: 28px; font-weight: 600; color: #f0f0f5; font-family: 'DM Mono', monospace; }
    .metric-label { font-size: 12px; color: #6868808; letter-spacing: 0.06em; text-transform: uppercase; margin-top: 4px; }
    .metric-delta-pos { color: #34d399; font-size: 13px; }
    .metric-delta-neg { color: #f87171; font-size: 13px; }

    .section-header {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6868a8 !important;
        margin-bottom: 12px;
        margin-top: 28px;
    }

    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 500;
    }
    .badge-risk-high { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
    .badge-risk-med  { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
    .badge-risk-low  { background: rgba(52,211,153,0.15);  color: #34d399; border: 1px solid rgba(52,211,153,0.3); }

    .ai-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #3a3a5c;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 16px;
    }
    .ai-card-title { font-size: 12px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: #818cf8; margin-bottom: 10px; }
    .ai-card-body  { font-size: 14px; color: #c8c8e8; line-height: 1.7; }

    .stSlider > div > div { background: #2a2a35; }
    .stSlider > div > div > div { background: #818cf8; }

    div[data-testid="stMetric"] {
        background: #16161a;
        border: 1px solid #2a2a35;
        border-radius: 12px;
        padding: 16px 20px;
    }
    div[data-testid="stMetric"] label { color: #6868a8 !important; font-size: 11px; letter-spacing: .06em; text-transform: uppercase; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #f0f0f5 !important; font-family: 'DM Mono', monospace; }
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] svg { display: none; }

    .stTabs [data-baseweb="tab-list"] { background: #16161a; border-radius: 10px; padding: 4px; border: 1px solid #2a2a35; gap: 4px; }
    .stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px; color: #6868a8 !important; font-size: 13px; padding: 8px 18px; }
    .stTabs [aria-selected="true"] { background: #2a2a40 !important; color: #f0f0f5 !important; }

    div[data-testid="stSelectbox"] > div { background: #16161a; border: 1px solid #2a2a35; border-radius: 8px; color: #f0f0f5; }
    div[data-testid="stMultiSelect"] > div { background: #16161a; border: 1px solid #2a2a35; border-radius: 8px; }
    .stButton > button {
        background: #3a3a6c;
        color: #c8c8f5;
        border: 1px solid #5a5a9c;
        border-radius: 8px;
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        padding: 8px 20px;
        transition: all .2s;
    }
    .stButton > button:hover { background: #4a4a8c; border-color: #818cf8; color: #f0f0f5; }

    hr { border-color: #2a2a35; }
</style>
""", unsafe_allow_html=True)


# ── Simulated Data ──────────────────────────────────────────────
@st.cache_data
def load_data():
    np.random.seed(42)
    products = [
        {"id": "P01", "name": "Nextar Blueberry Jam",    "category": "Jam",      "price": 13000, "base_sales": 618},
        {"id": "P02", "name": "Nextar Pineapple Jam",    "category": "Jam",      "price": 9270,  "base_sales": 505},
        {"id": "P03", "name": "AMO Milky Soda Strawberry","category": "Beverage", "price": 7850,  "base_sales": 670},
        {"id": "P04", "name": "AMO Milky Soda Original", "category": "Beverage", "price": 7670,  "base_sales": 779},
        {"id": "P05", "name": "Nabati Cheese Wafer",     "category": "Snack",    "price": 5500,  "base_sales": 920},
        {"id": "P06", "name": "Nabati Chocolate Wafer",  "category": "Snack",    "price": 5500,  "base_sales": 840},
        {"id": "P07", "name": "Richoco Drink",           "category": "Beverage", "price": 6200,  "base_sales": 430},
    ]

    # Cross-price elasticity matrix (how product i affects product j when i is discounted)
    # Negative = cannibalization (i steals sales from j)
    cross_elast = {
        ("P01","P02"): -0.72,  # Blueberry jam heavily cannibalizes Pineapple jam
        ("P02","P01"): -0.65,
        ("P03","P04"): -0.58,  # AMO flavors cannibalize each other
        ("P04","P03"): -0.51,
        ("P05","P06"): -0.63,  # Nabati wafers cannibalize each other
        ("P06","P05"): -0.55,
        ("P03","P07"): -0.34,  # Beverage cross-effect
        ("P04","P07"): -0.28,
        ("P07","P03"): -0.22,
        ("P01","P05"): -0.08,  # Weak cross-category
        ("P02","P06"): -0.06,
    }

    # Own-price elasticity (negative = demand drops when price rises)
    own_elast = {
        "P01": -1.8, "P02": -2.1, "P03": -1.6, "P04": -1.5,
        "P05": -2.3, "P06": -2.0, "P07": -1.4,
    }

    return products, cross_elast, own_elast


products, cross_elast, own_elast = load_data()
prod_map  = {p["id"]: p for p in products}
prod_names = {p["id"]: p["name"] for p in products}
prod_ids   = [p["id"] for p in products]


def compute_portfolio(discounts: dict) -> dict:
    """
    discounts: {pid: discount_pct (0-1)}
    Returns per-product and portfolio-level impact.
    """
    results = {}
    for p in products:
        pid = p["id"]
        d   = discounts.get(pid, 0)

        # Own-price effect
        own_delta_pct = own_elast[pid] * (-d)   # discount = price drop = positive qty effect
        own_qty_delta = p["base_sales"] * own_delta_pct

        # Cross-price effect (other products discounted → steal from this one)
        cross_qty_delta = 0
        cannibalizers   = []
        for other_p in products:
            oid = other_p["id"]
            if oid == pid:
                continue
            od = discounts.get(oid, 0)
            if od > 0:
                e = cross_elast.get((oid, pid), 0)
                effect = other_p["base_sales"] * e * od
                cross_qty_delta += effect
                if effect < -5:
                    cannibalizers.append({"from": oid, "effect": effect})

        new_qty   = max(0, p["base_sales"] + own_qty_delta + cross_qty_delta)
        new_price = p["price"] * (1 - d)
        base_rev  = p["base_sales"] * p["price"]
        new_rev   = new_qty * new_price

        results[pid] = {
            "name":            p["name"],
            "category":        p["category"],
            "base_qty":        p["base_sales"],
            "new_qty":         new_qty,
            "qty_delta":       new_qty - p["base_sales"],
            "qty_delta_pct":   (new_qty - p["base_sales"]) / p["base_sales"] * 100,
            "base_rev":        base_rev,
            "new_rev":         new_rev,
            "rev_delta":       new_rev - base_rev,
            "discount":        d,
            "cannibalizers":   cannibalizers,
            "cross_qty_delta": cross_qty_delta,
            "own_qty_delta":   own_qty_delta,
        }

    total_base = sum(r["base_rev"] for r in results.values())
    total_new  = sum(r["new_rev"]  for r in results.values())
    return results, total_base, total_new


def risk_level(e):
    if abs(e) >= 0.5:  return "High",   "badge-risk-high"
    if abs(e) >= 0.25: return "Medium", "badge-risk-med"
    return "Low", "badge-risk-low"


def generate_ai_insight(results, total_base, total_new, discounts):
    """Rule-based AI insight (swap in Claude API for real version)."""
    net = total_new - total_base
    net_pct = net / total_base * 100

    worst = min(results.values(), key=lambda r: r["rev_delta"])
    best  = max(results.values(), key=lambda r: r["rev_delta"])

    cannib_victims = [r for r in results.values() if r["cross_qty_delta"] < -20]

    active = [pid for pid, d in discounts.items() if d > 0]
    if not active:
        return "Belum ada skenario diskon yang dipilih. Gunakan slider di sidebar untuk mensimulasikan dampak promosi."

    lines = []
    if net >= 0:
        lines.append(f"✅ Skenario ini menghasilkan **net revenue +Rp {net:,.0f}** ({net_pct:+.1f}%) dibanding baseline.")
    else:
        lines.append(f"⚠️ Skenario ini berpotensi menurunkan portfolio revenue sebesar **Rp {abs(net):,.0f}** ({net_pct:.1f}%).")

    if cannib_victims:
        victims_str = ", ".join(v["name"].split()[0] + " " + v["name"].split()[1] for v in cannib_victims[:2])
        lines.append(f"🔴 Terdeteksi **cannibalization** pada {victims_str} — permintaan turun karena efek silang dari produk yang sedang dipromosikan.")

    if worst["rev_delta"] < -50000:
        lines.append(f"📉 Produk paling terdampak negatif: **{worst['name']}** ({worst['rev_delta']:,.0f} revenue delta).")

    if best["rev_delta"] > 0:
        lines.append(f"📈 Produk dengan uplift terbesar: **{best['name']}** (+{best['rev_delta']:,.0f}).")

    if any(d > 0.2 for d in discounts.values()):
        lines.append("💡 Diskon >20% pada produk sejenis berisiko tinggi saling kanibal — pertimbangkan untuk tidak mempromosikan dua produk dalam kategori yang sama secara bersamaan.")

    return "\n\n".join(lines)


# ── Sidebar ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 MAPL+")
    st.markdown("<p style='font-size:12px;color:#6868a8;margin-top:-8px;'>Portfolio Price Intelligence</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<p class='section-header'>Scenario: Discount Settings</p>", unsafe_allow_html=True)

    discounts = {}
    categories = sorted(set(p["category"] for p in products))
    for cat in categories:
        st.markdown(f"<p style='font-size:11px;color:#818cf8;font-weight:600;letter-spacing:.06em;margin-top:12px'>{cat.upper()}</p>", unsafe_allow_html=True)
        for p in [x for x in products if x["category"] == cat]:
            val = st.slider(
                p["name"].split()[-2] + " " + p["name"].split()[-1],
                min_value=0, max_value=50, value=0, step=5,
                key=f"disc_{p['id']}",
                format="%d%%"
            )
            discounts[p["id"]] = val / 100

    st.markdown("---")
    run = st.button("▶ Run Simulation", use_container_width=True)


# ── Main Layout ──────────────────────────────────────────────────
col_title, col_badge = st.columns([4, 1])
with col_title:
    st.markdown("## MAPL+ Portfolio Simulator")
    st.markdown("<p style='margin-top:-10px;font-size:14px;color:#6868a8'>Simulate pricing & detect cannibalization across your product portfolio</p>", unsafe_allow_html=True)
with col_badge:
    active_n = sum(1 for d in discounts.values() if d > 0)
    st.markdown(f"<div style='margin-top:16px;text-align:right'><span class='badge badge-risk-med'>{active_n} products discounted</span></div>", unsafe_allow_html=True)

st.markdown("---")

results, total_base, total_new = compute_portfolio(discounts)
net_rev    = total_new - total_base
net_pct    = net_rev / total_base * 100
canib_loss = sum(r["cross_qty_delta"] * prod_map[pid]["price"] for pid, r in results.items() if r["cross_qty_delta"] < 0)

tab1, tab2, tab3 = st.tabs(["📈 Portfolio Impact", "🔥 Cannibalization Map", "🤖 AI Insights"])

# ── Tab 1: Portfolio Impact ──────────────────────────────────────
with tab1:
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Base Revenue",    f"Rp {total_base/1e6:.2f}M")
    with m2:
        st.metric("Simulated Revenue", f"Rp {total_new/1e6:.2f}M", delta=f"{net_pct:+.1f}%")
    with m3:
        st.metric("Net Revenue Δ",  f"Rp {net_rev/1e3:+.1f}K")
    with m4:
        st.metric("Cannib. Loss Est.", f"Rp {abs(canib_loss)/1e3:.1f}K")

    st.markdown("<p class='section-header'>Per-Product Revenue Impact</p>", unsafe_allow_html=True)

    df = pd.DataFrame([{
        "Product":     r["name"],
        "Category":    r["category"],
        "Base Sales":  int(r["base_qty"]),
        "Sim. Sales":  int(r["new_qty"]),
        "Qty Δ":       int(r["qty_delta"]),
        "Qty Δ%":      f"{r['qty_delta_pct']:+.1f}%",
        "Base Rev":    f"Rp {r['base_rev']/1e3:.0f}K",
        "Sim. Rev":    f"Rp {r['new_rev']/1e3:.0f}K",
        "Rev Δ":       f"Rp {r['rev_delta']/1e3:+.0f}K",
        "Discount":    f"{r['discount']*100:.0f}%",
    } for pid, r in results.items()])

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<p class='section-header'>Revenue Waterfall by Product</p>", unsafe_allow_html=True)

    fig = go.Figure()
    names = [r["name"].replace("AMO Milky Soda ","AMO ").replace("Nabati ","") for r in results.values()]
    deltas = [r["rev_delta"] for r in results.values()]
    colors = ["#34d399" if d >= 0 else "#f87171" for d in deltas]

    fig.add_trace(go.Bar(
        x=names, y=deltas,
        marker_color=colors,
        text=[f"Rp {d/1e3:+.0f}K" for d in deltas],
        textposition="outside",
        textfont=dict(size=11, color="#c8c8d4"),
    ))
    fig.add_hline(y=0, line_color="#3a3a50", line_width=1)
    fig.update_layout(
        plot_bgcolor="#16161a", paper_bgcolor="#0f0f12",
        font=dict(color="#a8a8b8", family="DM Sans"),
        margin=dict(t=20, b=20, l=20, r=20),
        yaxis=dict(showgrid=True, gridcolor="#2a2a35", zeroline=False, tickprefix="Rp "),
        xaxis=dict(showgrid=False),
        showlegend=False, height=320,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<p class='section-header'>Own-Price vs Cross-Price Effect Breakdown</p>", unsafe_allow_html=True)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name="Own-price effect (promo uplift)",
        x=names,
        y=[r["own_qty_delta"] for r in results.values()],
        marker_color="#818cf8",
    ))
    fig2.add_trace(go.Bar(
        name="Cross-price effect (cannibalization loss)",
        x=names,
        y=[r["cross_qty_delta"] for r in results.values()],
        marker_color="#f87171",
    ))
    fig2.update_layout(
        barmode="relative",
        plot_bgcolor="#16161a", paper_bgcolor="#0f0f12",
        font=dict(color="#a8a8b8", family="DM Sans"),
        margin=dict(t=20, b=20, l=20, r=20),
        yaxis=dict(showgrid=True, gridcolor="#2a2a35", zeroline=True, zerolinecolor="#3a3a50"),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1, bgcolor="rgba(0,0,0,0)"),
        height=320,
    )
    st.plotly_chart(fig2, use_container_width=True)


# ── Tab 2: Cannibalization Heatmap ──────────────────────────────
with tab2:
    st.markdown("<p class='section-header'>Cross-Price Elasticity Matrix</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px'>Nilai negatif = produk di baris melemahkan penjualan produk di kolom saat dipromosikan. Semakin merah, semakin tinggi risiko kanibalisasi.</p>", unsafe_allow_html=True)

    n = len(prod_ids)
    matrix = np.zeros((n, n))
    for i, pid_i in enumerate(prod_ids):
        for j, pid_j in enumerate(prod_ids):
            if i != j:
                matrix[i][j] = cross_elast.get((pid_i, pid_j), 0)

    short_names = [p["name"].replace("AMO Milky Soda ","AMO ").replace("Nabati ","").replace("Nextar ","") for p in products]

    fig3 = go.Figure(data=go.Heatmap(
        z=matrix,
        x=short_names, y=short_names,
        colorscale=[
            [0.0,  "#7f1d1d"],
            [0.35, "#ef4444"],
            [0.5,  "#1e1e2e"],
            [0.65, "#1e1e2e"],
            [1.0,  "#1e1e2e"],
        ],
        zmid=0, zmin=-1, zmax=0,
        text=[[f"{matrix[i][j]:.2f}" if matrix[i][j] != 0 else "" for j in range(n)] for i in range(n)],
        texttemplate="%{text}",
        textfont=dict(size=11, color="#f0f0f5"),
        hovertemplate="Promoter: %{y}<br>Victim: %{x}<br>Elasticity: %{z:.2f}<extra></extra>",
        showscale=True,
        colorbar=dict(
            title="Cross-elasticity",
            titlefont=dict(color="#a8a8b8"),
            tickfont=dict(color="#a8a8b8"),
            bgcolor="#16161a",
        )
    ))
    fig3.update_layout(
        plot_bgcolor="#16161a", paper_bgcolor="#0f0f12",
        font=dict(color="#a8a8b8", family="DM Sans"),
        margin=dict(t=20, b=60, l=100, r=20),
        height=420,
        xaxis=dict(side="bottom", tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<p class='section-header'>High-Risk Product Pairs</p>", unsafe_allow_html=True)

    pairs = []
    for (pid_i, pid_j), e in cross_elast.items():
        if e < 0:
            lvl, badge = risk_level(e)
            pairs.append({
                "Promoter":    prod_names[pid_i],
                "Victim":      prod_names[pid_j],
                "Elasticity":  e,
                "Risk":        lvl,
            })
    pairs_df = pd.DataFrame(pairs).sort_values("Elasticity")

    for _, row in pairs_df.iterrows():
        lvl, badge = risk_level(row["Elasticity"])
        col_a, col_b, col_c, col_d = st.columns([3, 3, 1.5, 1])
        col_a.markdown(f"<span style='color:#f0f0f5;font-size:13px'>{row['Promoter']}</span>", unsafe_allow_html=True)
        col_b.markdown(f"<span style='color:#f87171;font-size:13px'>→ {row['Victim']}</span>", unsafe_allow_html=True)
        col_c.markdown(f"<span style='color:#a8a8b8;font-family:DM Mono,monospace;font-size:12px'>{row['Elasticity']:.2f}</span>", unsafe_allow_html=True)
        col_d.markdown(f"<span class='badge {badge}'>{lvl}</span>", unsafe_allow_html=True)


# ── Tab 3: AI Insights ──────────────────────────────────────────
with tab3:
    st.markdown("<p class='section-header'>AI-Generated Recommendation</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px;margin-bottom:16px'>Insight otomatis berdasarkan skenario simulasi yang sedang aktif. Di production, ini akan di-generate menggunakan Claude API.</p>", unsafe_allow_html=True)

    insight = generate_ai_insight(results, total_base, total_new, discounts)

    st.markdown(f"""
    <div class='ai-card'>
        <div class='ai-card-title'>🤖 Portfolio Intelligence Report</div>
        <div class='ai-card-body'>{insight.replace(chr(10), '<br>')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p class='section-header' style='margin-top:28px'>Cannibalization Risk per Active Promo</p>", unsafe_allow_html=True)

    active_promos = [(pid, d) for pid, d in discounts.items() if d > 0]
    if not active_promos:
        st.info("Aktifkan minimal satu diskon dari sidebar untuk melihat risk assessment.")
    else:
        for pid, d in active_promos:
            p = prod_map[pid]
            victims = [(cross_elast.get((pid, oid), 0), oid) for oid in prod_ids if oid != pid and cross_elast.get((pid, oid), 0) < 0]
            victims.sort()

            with st.expander(f"🎯 {p['name']} — {d*100:.0f}% discount", expanded=True):
                if victims:
                    for e, oid in victims:
                        lvl, badge = risk_level(e)
                        est_loss = abs(prod_map[oid]["base_sales"] * e * d * prod_map[oid]["price"])
                        c1, c2, c3 = st.columns([3, 1.5, 2])
                        c1.markdown(f"<span style='font-size:13px;color:#f0f0f5'>{prod_names[oid]}</span>", unsafe_allow_html=True)
                        c2.markdown(f"<span class='badge {badge}'>{lvl} ε={e:.2f}</span>", unsafe_allow_html=True)
                        c3.markdown(f"<span style='font-size:12px;color:#f87171'>~Rp {est_loss:,.0f} lost</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:#34d399;font-size:13px'>✓ No significant cannibalization detected</span>", unsafe_allow_html=True)

    st.markdown("<p class='section-header'>Recommended Actions</p>", unsafe_allow_html=True)

    active_cats = {}
    for pid, d in discounts.items():
        if d > 0:
            cat = prod_map[pid]["category"]
            active_cats.setdefault(cat, []).append(prod_map[pid]["name"])

    recs = []
    for cat, names_list in active_cats.items():
        if len(names_list) > 1:
            recs.append(f"⚠️ Hindari promosi **{names_list[0]}** dan **{names_list[1]}** secara bersamaan — keduanya dalam kategori {cat} dengan elastisitas silang tinggi.")

    if net_pct < -5:
        recs.append("📉 Net revenue turun signifikan. Pertimbangkan untuk mengurangi diskon pada produk dengan elastisitas silang tinggi.")

    if not recs:
        recs.append("✅ Tidak ada konflik serius terdeteksi pada skenario ini. Anda dapat melanjutkan strategi promosi yang direncanakan.")

    for r in recs:
        st.markdown(f"<div style='background:#1a1a2e;border:1px solid #3a3a5c;border-radius:8px;padding:12px 16px;margin-bottom:8px;font-size:13px;color:#c8c8e8'>{r}</div>", unsafe_allow_html=True)
