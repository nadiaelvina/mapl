import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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
.stApp { background: #0f0f12; }
section[data-testid="stSidebar"] { background: #16161a; border-right: 1px solid #2a2a35; }
section[data-testid="stSidebar"] * { color: #c8c8d4 !important; }
.block-container { padding: 2rem 2.5rem; max-width: 1400px; }
h1,h2,h3 { color: #f0f0f5 !important; }
.section-header {
    font-size: 11px; font-weight: 600; letter-spacing: .12em;
    text-transform: uppercase; color: #6868a8 !important;
    margin-bottom: 10px; margin-top: 24px;
}
.badge { display:inline-block; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:500; }
.badge-high { background:rgba(248,113,113,.15); color:#f87171; border:1px solid rgba(248,113,113,.3); }
.badge-med  { background:rgba(251,191,36,.15);  color:#fbbf24; border:1px solid rgba(251,191,36,.3); }
.badge-low  { background:rgba(52,211,153,.15);  color:#34d399; border:1px solid rgba(52,211,153,.3); }
.ai-card { background:#1a1a2e; border:1px solid #3a3a5c; border-radius:12px; padding:20px 24px; margin-top:12px; }
.ai-card-title { font-size:12px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#818cf8; margin-bottom:8px; }
.ai-card-body  { font-size:14px; color:#c8c8e8; line-height:1.7; }
div[data-testid="stMetric"] { background:#16161a; border:1px solid #2a2a35; border-radius:12px; padding:14px 18px; }
div[data-testid="stMetric"] label { color:#6868a8 !important; font-size:11px; letter-spacing:.06em; text-transform:uppercase; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:#f0f0f5 !important; font-family:'DM Mono',monospace; }
.stTabs [data-baseweb="tab-list"] { background:#16161a; border-radius:10px; padding:4px; border:1px solid #2a2a35; }
.stTabs [data-baseweb="tab"] { background:transparent; border-radius:8px; color:#6868a8 !important; font-size:13px; padding:8px 18px; }
.stTabs [aria-selected="true"] { background:#2a2a40 !important; color:#f0f0f5 !important; }
.stButton > button { background:#3a3a6c; color:#c8c8f5; border:1px solid #5a5a9c; border-radius:8px; font-size:13px; padding:8px 20px; }
.stButton > button:hover { background:#4a4a8c; border-color:#818cf8; color:#f0f0f5; }
hr { border-color:#2a2a35; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────

DUMMY_PRODUCTS = pd.DataFrame([
    {"id":"P01","name":"Nextar Blueberry Jam",     "category":"Jam",      "price":13000,"base_sales":618},
    {"id":"P02","name":"Nextar Pineapple Jam",     "category":"Jam",      "price":9270, "base_sales":505},
    {"id":"P03","name":"AMO Milky Soda Strawberry","category":"Beverage", "price":7850, "base_sales":670},
    {"id":"P04","name":"AMO Milky Soda Original",  "category":"Beverage", "price":7670, "base_sales":779},
    {"id":"P05","name":"Nabati Cheese Wafer",      "category":"Snack",    "price":5500, "base_sales":920},
    {"id":"P06","name":"Nabati Chocolate Wafer",   "category":"Snack",    "price":5500, "base_sales":840},
    {"id":"P07","name":"Richoco Drink",            "category":"Beverage", "price":6200, "base_sales":430},
])

DUMMY_ELASTICITY = pd.DataFrame([
    {"promoter_id":"P01","victim_id":"P02","elasticity":-0.72},
    {"promoter_id":"P02","victim_id":"P01","elasticity":-0.65},
    {"promoter_id":"P03","victim_id":"P04","elasticity":-0.58},
    {"promoter_id":"P04","victim_id":"P03","elasticity":-0.51},
    {"promoter_id":"P05","victim_id":"P06","elasticity":-0.63},
    {"promoter_id":"P06","victim_id":"P05","elasticity":-0.55},
    {"promoter_id":"P03","victim_id":"P07","elasticity":-0.34},
    {"promoter_id":"P04","victim_id":"P07","elasticity":-0.28},
    {"promoter_id":"P07","victim_id":"P03","elasticity":-0.22},
    {"promoter_id":"P01","victim_id":"P05","elasticity":-0.08},
    {"promoter_id":"P02","victim_id":"P06","elasticity":-0.06},
])

DUMMY_OWN = pd.DataFrame([
    {"id":"P01","own_elasticity":-1.8},
    {"id":"P02","own_elasticity":-2.1},
    {"id":"P03","own_elasticity":-1.6},
    {"id":"P04","own_elasticity":-1.5},
    {"id":"P05","own_elasticity":-2.3},
    {"id":"P06","own_elasticity":-2.0},
    {"id":"P07","own_elasticity":-1.4},
])

@st.cache_data
def load_from_github(raw_url: str) -> pd.DataFrame:
    return pd.read_csv(raw_url)

def try_load_csv(label, required_cols, fallback_df):
    """Try to load from GitHub URL or return fallback."""
    url = st.sidebar.text_input(f"GitHub raw URL — {label}", key=f"url_{label}", placeholder="https://raw.githubusercontent.com/...")
    if url.strip():
        try:
            df = load_from_github(url.strip())
            missing = [c for c in required_cols if c not in df.columns]
            if missing:
                st.sidebar.error(f"{label}: kolom tidak ditemukan: {missing}")
                return fallback_df
            st.sidebar.success(f"{label}: {len(df)} rows loaded ✓")
            return df
        except Exception as ex:
            st.sidebar.error(f"{label}: gagal load — {ex}")
            return fallback_df
    return fallback_df

# ─────────────────────────────────────────────
# SIDEBAR — Data + Discount Controls
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 MAPL+")
    st.markdown("<p style='font-size:12px;color:#6868a8;margin-top:-8px'>Portfolio Price Intelligence</p>", unsafe_allow_html=True)
    st.markdown("---")

    with st.expander("🗂 Load Data dari GitHub CSV", expanded=False):
        st.markdown("<p style='font-size:11px;color:#818cf8'>Paste URL raw CSV dari repo kamu. Kolom wajib ada di tabel format di README.</p>", unsafe_allow_html=True)
        df_products   = try_load_csv("products",   ["id","name","category","price","base_sales"], DUMMY_PRODUCTS)
        df_elasticity = try_load_csv("elasticity", ["promoter_id","victim_id","elasticity"],      DUMMY_ELASTICITY)
        df_own        = try_load_csv("own_elast",  ["id","own_elasticity"],                       DUMMY_OWN)
    
    if len(df_products) == len(DUMMY_PRODUCTS) and df_products.equals(DUMMY_PRODUCTS):
        st.sidebar.caption("⚠️ Menggunakan data dummy. Load CSV di atas untuk data real.")

    st.markdown("---")
    st.markdown("<p class='section-header'>Scenario: Discount per Produk</p>", unsafe_allow_html=True)

    discounts = {}
    categories = sorted(df_products["category"].unique())
    for cat in categories:
        st.markdown(f"<p style='font-size:11px;color:#818cf8;font-weight:600;letter-spacing:.06em;margin-top:10px'>{cat.upper()}</p>", unsafe_allow_html=True)
        cat_prods = df_products[df_products["category"] == cat]
        for _, row in cat_prods.iterrows():
            short = " ".join(row["name"].split()[-2:])
            val = st.slider(short, 0, 50, 0, 5, key=f"disc_{row['id']}", format="%d%%")
            discounts[row["id"]] = val / 100

# ─────────────────────────────────────────────
# BUILD LOOKUP DICTS
# ─────────────────────────────────────────────
products    = df_products.to_dict("records")
prod_map    = {p["id"]: p for p in products}
prod_names  = {p["id"]: p["name"] for p in products}
prod_ids    = [p["id"] for p in products]

cross_elast = {
    (r["promoter_id"], r["victim_id"]): float(r["elasticity"])
    for _, r in df_elasticity.iterrows()
}
own_elast = {r["id"]: float(r["own_elasticity"]) for _, r in df_own.iterrows()}

# ─────────────────────────────────────────────
# SIMULATION ENGINE
# ─────────────────────────────────────────────
def compute_portfolio(discounts):
    results = {}
    for p in products:
        pid = p["id"]
        d   = discounts.get(pid, 0)
        oe  = own_elast.get(pid, -1.5)

        own_qty_delta   = p["base_sales"] * oe * (-d)
        cross_qty_delta = 0.0

        for other in products:
            oid = other["id"]
            if oid == pid: continue
            od = discounts.get(oid, 0)
            if od > 0:
                e = cross_elast.get((oid, pid), 0.0)
                cross_qty_delta += other["base_sales"] * e * od

        new_qty   = max(0.0, p["base_sales"] + own_qty_delta + cross_qty_delta)
        new_price = p["price"] * (1 - d)
        base_rev  = p["base_sales"] * p["price"]
        new_rev   = new_qty * new_price

        results[pid] = {
            "name":            p["name"],
            "category":        p["category"],
            "base_qty":        p["base_sales"],
            "new_qty":         new_qty,
            "qty_delta":       new_qty - p["base_sales"],
            "qty_delta_pct":   (new_qty - p["base_sales"]) / max(p["base_sales"], 1) * 100,
            "base_rev":        base_rev,
            "new_rev":         new_rev,
            "rev_delta":       new_rev - base_rev,
            "discount":        d,
            "own_qty_delta":   own_qty_delta,
            "cross_qty_delta": cross_qty_delta,
        }
    total_base = sum(r["base_rev"] for r in results.values())
    total_new  = sum(r["new_rev"]  for r in results.values())
    return results, total_base, total_new

def badge(e):
    if abs(e) >= 0.5: return "High",   "badge-high"
    if abs(e) >= 0.25: return "Medium", "badge-med"
    return "Low", "badge-low"

PLOT_THEME = dict(
    plot_bgcolor="#16161a", paper_bgcolor="#0f0f12",
    font=dict(color="#a8a8b8", family="DM Sans"),
    margin=dict(t=20, b=20, l=20, r=20),
)

# ─────────────────────────────────────────────
# COMPUTE
# ─────────────────────────────────────────────
results, total_base, total_new = compute_portfolio(discounts)
net_rev  = total_new - total_base
net_pct  = net_rev / max(total_base, 1) * 100
canib_loss = sum(
    r["cross_qty_delta"] * prod_map[pid]["price"]
    for pid, r in results.items() if r["cross_qty_delta"] < 0
)
active_n = sum(1 for d in discounts.values() if d > 0)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
c1, c2 = st.columns([5, 1])
with c1:
    st.markdown("## MAPL+ Portfolio Simulator")
    st.markdown("<p style='margin-top:-10px;font-size:14px;color:#6868a8'>Detect cannibalization & simulate pricing impact across your product portfolio</p>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='margin-top:20px;text-align:right'><span class='badge badge-med'>{active_n} aktif</span></div>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📈 Portfolio Impact", "🔥 Cannibalization Map", "🤖 AI Insights"])

# ─────────────────────────────────────────────
# TAB 1 — PORTFOLIO IMPACT
# ─────────────────────────────────────────────
with tab1:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Base Revenue",       f"Rp {total_base/1e6:.2f}M")
    m2.metric("Simulated Revenue",  f"Rp {total_new/1e6:.2f}M",  delta=f"{net_pct:+.1f}%")
    m3.metric("Net Revenue Δ",      f"Rp {net_rev/1e3:+.1f}K")
    m4.metric("Cannib. Loss Est.",  f"Rp {abs(canib_loss)/1e3:.1f}K")

    st.markdown("<p class='section-header'>Per-Product Revenue Impact</p>", unsafe_allow_html=True)
    df_show = pd.DataFrame([{
        "Product":   r["name"],
        "Category":  r["category"],
        "Discount":  f"{r['discount']*100:.0f}%",
        "Base Sales": int(r["base_qty"]),
        "Sim Sales":  int(r["new_qty"]),
        "Qty Δ":      f"{r['qty_delta_pct']:+.1f}%",
        "Rev Δ":      f"Rp {r['rev_delta']/1e3:+.0f}K",
    } for r in results.values()])
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    # Waterfall chart
    st.markdown("<p class='section-header'>Revenue Delta per Product</p>", unsafe_allow_html=True)
    names  = [r["name"].split()[-1] + " " + r["name"].split()[-2] if len(r["name"].split()) > 1 else r["name"] for r in results.values()]
    names  = [p["name"] for p in products]   # keep full names, plotly will truncate
    deltas = [r["rev_delta"] for r in results.values()]
    colors = ["#34d399" if d >= 0 else "#f87171" for d in deltas]

    fig1 = go.Figure(go.Bar(
        x=names, y=deltas,
        marker_color=colors,
        text=[f"Rp {d/1e3:+.0f}K" for d in deltas],
        textposition="outside",
        textfont=dict(size=11, color="#c8c8d4"),
    ))
    fig1.add_hline(y=0, line_color="#3a3a50", line_width=1)
    fig1.update_layout(
        **PLOT_THEME,
        height=320,
        showlegend=False,
        yaxis=dict(showgrid=True, gridcolor="#2a2a35", zeroline=False),
        xaxis=dict(showgrid=False, tickangle=-20),
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Stacked bar: own vs cross effect
    st.markdown("<p class='section-header'>Own-Price vs Cross-Price Qty Effect</p>", unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="Own-price uplift",         x=names, y=[r["own_qty_delta"]   for r in results.values()], marker_color="#818cf8"))
    fig2.add_trace(go.Bar(name="Cross-price (cannib loss)", x=names, y=[r["cross_qty_delta"] for r in results.values()], marker_color="#f87171"))
    fig2.update_layout(
        **PLOT_THEME,
        barmode="relative", height=300,
        yaxis=dict(showgrid=True, gridcolor="#2a2a35", zeroline=True, zerolinecolor="#3a3a50"),
        xaxis=dict(showgrid=False, tickangle=-20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 2 — CANNIBALIZATION HEATMAP
# ─────────────────────────────────────────────
with tab2:
    st.markdown("<p class='section-header'>Cross-Price Elasticity Matrix</p>", unsafe_allow_html=True)
    st.caption("Baris = promoter (produk yang didiskon). Kolom = victim (produk yang terdampak). Nilai negatif = kanibalisasi.")

    n      = len(prod_ids)
    matrix = np.zeros((n, n))
    for i, pid_i in enumerate(prod_ids):
        for j, pid_j in enumerate(prod_ids):
            if i != j:
                matrix[i][j] = cross_elast.get((pid_i, pid_j), 0.0)

    labels = [p["name"] for p in products]

    # text annotation — blank on diagonal / zero cells
    text_vals = []
    for i in range(n):
        row_txt = []
        for j in range(n):
            v = matrix[i][j]
            row_txt.append(f"{v:.2f}" if v != 0 else "")
        text_vals.append(row_txt)

    # colorscale: red (most negative) → dark neutral (zero/positive)
    colorscale = [
        [0.0,  "#7f1d1d"],
        [0.4,  "#dc2626"],
        [0.7,  "#2a2a3a"],
        [1.0,  "#2a2a3a"],
    ]

    vmin = matrix.min() if matrix.min() < 0 else -1
    vmax = 0.0   # cap at 0 so the colour range is always negative → zero

    fig3 = go.Figure(go.Heatmap(
        z=matrix,
        x=labels, y=labels,
        zmin=vmin, zmax=vmax,
        colorscale=colorscale,
        text=text_vals,
        texttemplate="%{text}",
        textfont=dict(size=11, color="#e0e0f0"),
        hovertemplate="Promoter: %{y}<br>Victim: %{x}<br>Elasticity: %{z:.3f}<extra></extra>",
        showscale=True,
        colorbar=dict(
            title=dict(text="Cross-ε", font=dict(color="#a8a8b8")),
            tickfont=dict(color="#a8a8b8"),
            thickness=14,
        ),
        xgap=2, ygap=2,
    ))
    fig3.update_layout(
        **PLOT_THEME,
        height=440,
        margin=dict(t=20, b=80, l=160, r=20),
        xaxis=dict(tickfont=dict(size=11), tickangle=-30, side="bottom"),
        yaxis=dict(tickfont=dict(size=11), autorange="reversed"),
    )
    st.plotly_chart(fig3, use_container_width=True)

    # High-risk pairs table
    st.markdown("<p class='section-header'>High-Risk Product Pairs</p>", unsafe_allow_html=True)
    pairs = sorted(
        [(pid_i, pid_j, e) for (pid_i, pid_j), e in cross_elast.items() if e < 0],
        key=lambda x: x[2]
    )
    if not pairs:
        st.info("Tidak ada data elastisitas negatif ditemukan.")
    else:
        for pid_i, pid_j, e in pairs:
            lvl, cls = badge(e)
            ca, cb, cc, cd = st.columns([3, 3, 1.5, 1])
            ca.markdown(f"<span style='color:#f0f0f5;font-size:13px'>{prod_names.get(pid_i, pid_i)}</span>", unsafe_allow_html=True)
            cb.markdown(f"<span style='color:#f87171;font-size:13px'>→ {prod_names.get(pid_j, pid_j)}</span>", unsafe_allow_html=True)
            cc.markdown(f"<span style='color:#a8a8b8;font-family:DM Mono,monospace;font-size:12px'>{e:.2f}</span>", unsafe_allow_html=True)
            cd.markdown(f"<span class='badge {cls}'>{lvl}</span>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 3 — AI INSIGHTS
# ─────────────────────────────────────────────
with tab3:
    st.markdown("<p class='section-header'>Portfolio Insight</p>", unsafe_allow_html=True)

    active_promos = [(pid, d) for pid, d in discounts.items() if d > 0]

    if not active_promos:
        st.info("Aktifkan minimal satu diskon dari sidebar untuk melihat insight.")
    else:
        # Build insight text
        lines = []
        delta_sign = "naik" if net_pct >= 0 else "turun"
        lines.append(f"📊 Net portfolio revenue **{delta_sign} {abs(net_pct):.1f}%** (Rp {net_rev/1e3:+.0f}K) dari skenario ini.")

        cannib_victims = [r for r in results.values() if r["cross_qty_delta"] < -20]
        if cannib_victims:
            vnames = ", ".join(v["name"] for v in cannib_victims[:2])
            lines.append(f"🔴 Terdeteksi cannibalization pada: **{vnames}** — volume turun akibat efek silang produk lain yang dipromosikan.")

        worst = min(results.values(), key=lambda r: r["rev_delta"])
        if worst["rev_delta"] < 0:
            lines.append(f"📉 Produk paling terdampak negatif: **{worst['name']}** (Rp {worst['rev_delta']/1e3:.0f}K revenue lost).")

        best = max(results.values(), key=lambda r: r["rev_delta"])
        if best["rev_delta"] > 0:
            lines.append(f"📈 Produk dengan uplift terbesar: **{best['name']}** (+Rp {best['rev_delta']/1e3:.0f}K).")

        # Category conflict check
        cat_active = {}
        for pid, d in active_promos:
            cat = prod_map[pid]["category"]
            cat_active.setdefault(cat, []).append(prod_map[pid]["name"])
        for cat, ns in cat_active.items():
            if len(ns) > 1:
                lines.append(f"⚠️ **{ns[0]}** dan **{ns[1]}** dipromosikan bersamaan dalam kategori {cat} — risiko kanibalisasi tinggi.")

        insight_html = "<br><br>".join(lines)
        st.markdown(f"""
        <div class='ai-card'>
            <div class='ai-card-title'>🤖 AI Portfolio Report</div>
            <div class='ai-card-body'>{insight_html}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p class='section-header' style='margin-top:28px'>Risk per Active Promo</p>", unsafe_allow_html=True)
        for pid, d in active_promos:
            p = prod_map[pid]
            victims = sorted(
                [(cross_elast.get((pid, oid), 0.0), oid)
                 for oid in prod_ids if oid != pid and cross_elast.get((pid, oid), 0.0) < 0]
            )
            with st.expander(f"🎯 {p['name']} — {d*100:.0f}% diskon", expanded=True):
                if victims:
                    for e_val, oid in victims:
                        if oid not in prod_map: continue
                        lvl, cls = badge(e_val)
                        est = abs(prod_map[oid]["base_sales"] * e_val * d * prod_map[oid]["price"])
                        c1, c2, c3 = st.columns([3, 1.5, 2])
                        c1.markdown(f"<span style='font-size:13px;color:#f0f0f5'>{prod_names.get(oid,oid)}</span>", unsafe_allow_html=True)
                        c2.markdown(f"<span class='badge {cls}'>{lvl} ε={e_val:.2f}</span>", unsafe_allow_html=True)
                        c3.markdown(f"<span style='font-size:12px;color:#f87171'>~Rp {est:,.0f} hilang</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:#34d399;font-size:13px'>✓ Tidak ada cannibalization terdeteksi</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p class='section-header'>Upgrade ke Claude API</p>", unsafe_allow_html=True)
    st.code("""# Di secrets.toml → ANTHROPIC_API_KEY = "sk-ant-..."
import anthropic
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

msg = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=600,
    messages=[{"role":"user","content": f"Kamu pricing analyst Nabati. Beri rekomendasi bisnis: {summary}"}]
)
st.write(msg.content[0].text)""", language="python")
