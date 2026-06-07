import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from itertools import combinations

st.set_page_config(
    page_title="MAPL+ | Portfolio Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');
*, html, body { font-family: 'DM Sans', sans-serif; box-sizing: border-box; }
.stApp { background: #0c0c10; }
section[data-testid="stSidebar"] { background: #111116; border-right: 1px solid #1e1e28; }
section[data-testid="stSidebar"] * { color: #b0b0c0 !important; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1440px; }
h1,h2,h3 { color: #eeeef5 !important; }

.sec-label {
    font-size: 10px; font-weight: 600; letter-spacing: .14em;
    text-transform: uppercase; color: #5a5a7a !important;
    margin: 28px 0 10px;
}

/* metric cards */
div[data-testid="stMetric"] {
    background: #111116; border: 1px solid #1e1e28;
    border-radius: 10px; padding: 14px 18px;
}
div[data-testid="stMetric"] label { color: #5a5a7a !important; font-size: 10px; letter-spacing: .1em; text-transform: uppercase; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #eeeef5 !important; font-family: 'DM Mono', monospace; font-size: 22px; }
div[data-testid="stMetric"] [data-testid="stMetricDelta"] svg { display: none; }

/* tabs */
.stTabs [data-baseweb="tab-list"] { background: #111116; border-radius: 10px; padding: 4px; border: 1px solid #1e1e28; gap: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent; border-radius: 7px; color: #5a5a7a !important; font-size: 13px; padding: 7px 16px; }
.stTabs [aria-selected="true"] { background: #1e1e2e !important; color: #eeeef5 !important; }

/* badges */
.badge { display:inline-block; padding:2px 9px; border-radius:20px; font-size:11px; font-weight:500; }
.b-high { background:rgba(248,113,113,.12); color:#f87171; border:1px solid rgba(248,113,113,.25); }
.b-med  { background:rgba(251,191,36,.12);  color:#fbbf24; border:1px solid rgba(251,191,36,.25); }
.b-low  { background:rgba(52,211,153,.12);  color:#34d399; border:1px solid rgba(52,211,153,.25); }
.b-info { background:rgba(129,140,248,.12); color:#818cf8; border:1px solid rgba(129,140,248,.25); }

/* ai card */
.ai-card { background:#0e0e1a; border:1px solid #2a2a44; border-radius:10px; padding:18px 22px; margin-top:12px; }
.ai-card-title { font-size:10px; font-weight:600; letter-spacing:.1em; text-transform:uppercase; color:#818cf8; margin-bottom:10px; }
.ai-card-body  { font-size:13px; color:#b8b8d8; line-height:1.75; }

/* rec card */
.rec-card { background:#0e0e1a; border:1px solid #2a2a44; border-radius:8px; padding:11px 15px; margin-bottom:7px; font-size:13px; color:#b8b8d8; }

/* sidebar slider label */
.cat-label { font-size:10px !important; font-weight:600 !important; letter-spacing:.1em !important; color:#818cf8 !important; margin-top:14px !important; }

/* buttons */
.stButton>button { background:#1e1e3a; color:#b0b0e0; border:1px solid #3a3a6a; border-radius:8px; font-size:13px; padding:7px 18px; transition:all .15s; }
.stButton>button:hover { background:#2a2a50; border-color:#818cf8; color:#eeeef5; }
hr { border-color:#1e1e28; }

/* dataframe */
div[data-testid="stDataFrame"] { border: 1px solid #1e1e28; border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

PLOT = dict(
    plot_bgcolor="#111116", paper_bgcolor="#0c0c10",
    font=dict(color="#8888a8", family="DM Sans"),
    margin=dict(t=24, b=24, l=24, r=24),
)

# ─────────────────────────────────────────────
# DATA — 20 SKU Nabati real
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    products = [
        # Richeese
        {"id":"S001","name":"Richeese Wafer Keju 50g",        "brand":"Richeese","category":"Wafer",           "price":5500,  "base_sales":920},
        {"id":"S002","name":"Richeese Wafer Pink Lava 50g",   "brand":"Richeese","category":"Wafer",           "price":5500,  "base_sales":840},
        {"id":"S003","name":"Richeese Wafer Keju 10g Renceng","brand":"Richeese","category":"Wafer",           "price":2000,  "base_sales":760},
        {"id":"S004","name":"Richeese Mi Instan Goreng",      "brand":"Richeese","category":"Mi Instan",       "price":3500,  "base_sales":680},
        {"id":"S005","name":"Richeese Mi Instan Ramen Keju",  "brand":"Richeese","category":"Mi Instan",       "price":3800,  "base_sales":610},
        {"id":"S006","name":"Richeese Mi Instan Keju Pedas",  "brand":"Richeese","category":"Mi Instan",       "price":3800,  "base_sales":590},
        {"id":"S007","name":"Richeese Siip Keju 20g",         "brand":"Richeese","category":"Extruded Snack",  "price":2500,  "base_sales":920},
        {"id":"S008","name":"Richeese Siip Jagung Bakar 20g", "brand":"Richeese","category":"Extruded Snack",  "price":2500,  "base_sales":880},
        {"id":"S009","name":"Nabati Drinko Richeese 150ml",   "brand":"Richeese","category":"Minuman",         "price":4500,  "base_sales":430},
        {"id":"S010","name":"Nabati Biskuit Rasa Kelapa",     "brand":"Richeese","category":"Biskuit",         "price":3000,  "base_sales":510},
        # Richoco
        {"id":"S011","name":"Richoco Wafer Cokelat 50g",      "brand":"Richoco", "category":"Wafer",           "price":5500,  "base_sales":770},
        {"id":"S012","name":"Richoco Wafer Hazelnut 50g",     "brand":"Richoco", "category":"Wafer",           "price":5500,  "base_sales":690},
        {"id":"S013","name":"Richoco Wafer Cokelat 10g Renceng","brand":"Richoco","category":"Wafer",          "price":2000,  "base_sales":650},
        {"id":"S014","name":"Richoco Ahh! Extruded 15g",      "brand":"Richoco", "category":"Extruded Snack",  "price":2000,  "base_sales":580},
        {"id":"S015","name":"Nabati Drinko Richoco 150ml",    "brand":"Richoco", "category":"Minuman",         "price":4500,  "base_sales":410},
        {"id":"S016","name":"Nabati Biskuit Rasa Cokelat",    "brand":"Richoco", "category":"Biskuit",         "price":3000,  "base_sales":490},
        # Nextar
        {"id":"S017","name":"Nextar Nastar Pie 30g",          "brand":"Nextar",  "category":"Kue/Pie",         "price":4000,  "base_sales":618},
        {"id":"S018","name":"Nextar Choco Delight 40g",       "brand":"Nextar",  "category":"Kue/Pie",         "price":4500,  "base_sales":505},
        {"id":"S019","name":"Nextar Pineapple Pie 30g",       "brand":"Nextar",  "category":"Kue/Pie",         "price":4000,  "base_sales":480},
        {"id":"S020","name":"Nextar Brownies Pie 40g",        "brand":"Nextar",  "category":"Kue/Pie",         "price":4500,  "base_sales":460},
    ]

    # Cross-price elasticity — same category pairs (from EDA candidates)
    # (promoter_id, victim_id): elasticity
    cross_elast = {
        # Wafer — same category cross-brand
        ("S001","S002"): -0.55, ("S002","S001"): -0.48,
        ("S001","S003"): -0.38, ("S003","S001"): -0.42,
        ("S001","S011"): -0.34, ("S011","S001"): -0.29,
        ("S001","S012"): -0.28, ("S012","S001"): -0.22,
        ("S002","S011"): -0.45, ("S011","S002"): -0.51,
        ("S002","S012"): -0.31, ("S012","S002"): -0.26,
        ("S002","S003"): -0.63, ("S003","S002"): -0.58,
        ("S011","S013"): -0.44, ("S013","S011"): -0.38,
        ("S011","S012"): -0.39, ("S012","S011"): -0.33,
        # Mi Instan
        ("S005","S004"): -0.52, ("S004","S005"): -0.41,
        ("S006","S004"): -0.38, ("S004","S006"): -0.32,
        ("S005","S006"): -0.29, ("S006","S005"): -0.25,
        # Kue/Pie — Nextar
        ("S017","S018"): -0.65, ("S018","S017"): -0.72,
        ("S020","S018"): -0.58, ("S018","S020"): -0.51,
        ("S018","S019"): -0.47, ("S019","S018"): -0.42,
        ("S020","S017"): -0.38, ("S017","S020"): -0.33,
        # Extruded Snack
        ("S007","S008"): -0.22, ("S008","S007"): -0.18,
        ("S007","S014"): -0.19, ("S014","S007"): -0.16,
    }

    own_elast = {
        "S001":-1.8,"S002":-2.1,"S003":-1.9,"S004":-1.6,"S005":-1.7,
        "S006":-1.8,"S007":-2.3,"S008":-2.1,"S009":-1.4,"S010":-1.5,
        "S011":-1.9,"S012":-1.7,"S013":-2.0,"S014":-1.8,"S015":-1.4,
        "S016":-1.5,"S017":-1.8,"S018":-2.1,"S019":-1.7,"S020":-1.9,
    }

    return products, cross_elast, own_elast

products, cross_elast, own_elast = load_data()
prod_map   = {p["id"]: p for p in products}
prod_ids   = [p["id"] for p in products]
prod_names = {p["id"]: p["name"] for p in products}
categories = sorted(set(p["category"] for p in products))
brands     = sorted(set(p["brand"] for p in products))

BRAND_COLOR = {"Richeese":"#E8472A","Richoco":"#6B3FA0","Nextar":"#1A7FC1"}
PROMO_COLOR = {"Promo Normal":"#4AABDB","Promo Bundling":"#F5A623","Promo Seasonal High":"#E8472A"}

# ─────────────────────────────────────────────
# ENGINE
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

        results[pid] = {
            "name":            p["name"],
            "brand":           p["brand"],
            "category":        p["category"],
            "base_qty":        p["base_sales"],
            "new_qty":         new_qty,
            "qty_delta":       new_qty - p["base_sales"],
            "qty_delta_pct":   (new_qty - p["base_sales"]) / max(p["base_sales"],1) * 100,
            "base_rev":        p["base_sales"] * p["price"],
            "new_rev":         new_qty * new_price,
            "rev_delta":       new_qty * new_price - p["base_sales"] * p["price"],
            "discount":        d,
            "own_qty_delta":   own_qty_delta,
            "cross_qty_delta": cross_qty_delta,
        }

    total_base = sum(r["base_rev"] for r in results.values())
    total_new  = sum(r["new_rev"]  for r in results.values())
    return results, total_base, total_new

def badge(e):
    if abs(e) >= 0.5: return "High",   "b-high"
    if abs(e) >= 0.3: return "Medium", "b-med"
    return "Low", "b-low"

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 MAPL+")
    st.markdown("<p style='font-size:11px;color:#5a5a7a;margin-top:-8px'>Portfolio Price Intelligence · Nabati</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Filter category
    st.markdown("<p class='cat-label'>FILTER KATEGORI</p>", unsafe_allow_html=True)
    sel_cats = st.multiselect("", categories, default=categories, label_visibility="collapsed", key="sel_cats")

    st.markdown("<p class='cat-label' style='margin-top:16px'>SCENARIO: PROMO TYPE</p>", unsafe_allow_html=True)
    promo_type_global = st.selectbox("", ["Promo Normal","Promo Bundling","Promo Seasonal High"],
                                     label_visibility="collapsed", key="promo_type")

    st.markdown("<p class='cat-label' style='margin-top:16px'>SCENARIO: DISCOUNT PER SKU</p>", unsafe_allow_html=True)

    discounts = {}
    for cat in categories:
        if cat not in sel_cats:
            continue
        st.markdown(f"<p style='font-size:10px;color:#818cf8;font-weight:600;letter-spacing:.08em;margin-top:10px'>{cat.upper()}</p>", unsafe_allow_html=True)
        for p in [x for x in products if x["category"] == cat]:
            short = " ".join(p["name"].split()[-2:])
            val = st.slider(short, 0, 50, 0, 5, key=f"d_{p['id']}", format="%d%%")
            discounts[p["id"]] = val / 100

    st.markdown("---")
    active_n = sum(1 for d in discounts.values() if d > 0)
    st.markdown(f"<p style='font-size:12px;color:#5a5a7a'>{active_n} SKU aktif · {promo_type_global}</p>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# COMPUTE
# ─────────────────────────────────────────────
results, total_base, total_new = compute_portfolio(discounts)
net_rev  = total_new - total_base
net_pct  = net_rev / max(total_base, 1) * 100
canib_loss = abs(sum(
    r["cross_qty_delta"] * prod_map[pid]["price"]
    for pid, r in results.items() if r["cross_qty_delta"] < 0
))

# filter results by selected category
res_filtered = {pid: r for pid, r in results.items() if prod_map[pid]["category"] in sel_cats}

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
c1, c2 = st.columns([5, 1])
with c1:
    st.markdown("## MAPL+ Portfolio Simulator")
    st.markdown("<p style='margin-top:-10px;font-size:13px;color:#5a5a7a'>Detect cannibalization & simulate pricing impact · Nabati product portfolio</p>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='margin-top:22px;text-align:right'><span class='badge b-info'>{active_n} aktif</span></div>", unsafe_allow_html=True)
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
    m4.metric("Cannib. Loss Est.",  f"Rp {canib_loss/1e3:.1f}K")

    # ── Table ──
    st.markdown("<p class='sec-label'>Per-Product Revenue Impact</p>", unsafe_allow_html=True)
    df_show = pd.DataFrame([{
        "Product":    r["name"],
        "Brand":      r["brand"],
        "Category":   r["category"],
        "Discount":   f"{r['discount']*100:.0f}%",
        "Base Sales": int(r["base_qty"]),
        "Sim Sales":  int(r["new_qty"]),
        "Qty Δ%":     f"{r['qty_delta_pct']:+.1f}%",
        "Rev Δ":      f"Rp {r['rev_delta']/1e3:+.0f}K",
    } for r in res_filtered.values()])
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    # ── Waterfall ──
    st.markdown("<p class='sec-label'>Revenue Delta per Product</p>", unsafe_allow_html=True)
    names  = [r["name"] for r in res_filtered.values()]
    deltas = [r["rev_delta"] for r in res_filtered.values()]
    bcolors = [BRAND_COLOR.get(r["brand"],"#818cf8") for r in res_filtered.values()]
    border  = ["#34d399" if d >= 0 else "#f87171" for d in deltas]

    fig1 = go.Figure(go.Bar(
        x=names, y=deltas,
        marker=dict(color=bcolors, line=dict(color=border, width=2)),
        text=[f"Rp {d/1e3:+.0f}K" for d in deltas],
        textposition="outside",
        textfont=dict(size=10, color="#8888a8"),
    ))
    fig1.add_hline(y=0, line_color="#2a2a3a", line_width=1)
    fig1.update_layout(
        **PLOT, height=340, showlegend=False,
        yaxis=dict(showgrid=True, gridcolor="#1a1a24", zeroline=False),
        xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=10)),
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ── Own vs Cross ──
    st.markdown("<p class='sec-label'>Own-Price Uplift vs Cross-Price Cannibalization (Qty)</p>", unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name="Own-price uplift",
        x=names,
        y=[r["own_qty_delta"]   for r in res_filtered.values()],
        marker_color="#818cf8",
    ))
    fig2.add_trace(go.Bar(
        name="Cross-price loss (cannibalization)",
        x=names,
        y=[r["cross_qty_delta"] for r in res_filtered.values()],
        marker_color="#f87171",
    ))
    fig2.update_layout(
        **PLOT, barmode="relative", height=320,
        yaxis=dict(showgrid=True, gridcolor="#1a1a24", zeroline=True, zerolinecolor="#2a2a3a"),
        xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=10)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Revenue by Brand (pie) ──
    st.markdown("<p class='sec-label'>Simulated Revenue Split by Brand</p>", unsafe_allow_html=True)
    brand_rev = {}
    for r in res_filtered.values():
        brand_rev[r["brand"]] = brand_rev.get(r["brand"], 0) + r["new_rev"]

    fig_pie = go.Figure(go.Pie(
        labels=list(brand_rev.keys()),
        values=list(brand_rev.values()),
        marker=dict(colors=[BRAND_COLOR.get(b,"#818cf8") for b in brand_rev.keys()],
                    line=dict(color="#0c0c10", width=2)),
        textfont=dict(size=12, color="#eeeef5"),
        hole=0.5,
    ))
    fig_pie.update_layout(**PLOT, height=300, showlegend=True,
                          legend=dict(font=dict(color="#8888a8")))
    st.plotly_chart(fig_pie, use_container_width=True)


# ─────────────────────────────────────────────
# TAB 2 — CANNIBALIZATION MAP
# ─────────────────────────────────────────────
with tab2:
    # filter prod_ids by selected category
    filt_ids = [pid for pid in prod_ids if prod_map[pid]["category"] in sel_cats]
    filt_names = [prod_map[pid]["name"] for pid in filt_ids]
    n = len(filt_ids)

    st.markdown("<p class='sec-label'>Cross-Price Elasticity Heatmap</p>", unsafe_allow_html=True)
    st.caption("Baris = promoter (SKU yang dipromosi). Kolom = victim (SKU yang terdampak). Merah = kanibalisasi tinggi.")

    if n == 0:
        st.info("Pilih minimal satu kategori dari sidebar.")
    else:
        matrix = np.full((n, n), np.nan)
        for i, pid_i in enumerate(filt_ids):
            for j, pid_j in enumerate(filt_ids):
                if i != j:
                    v = cross_elast.get((pid_i, pid_j), np.nan)
                    matrix[i][j] = v

        text_ann = []
        for i in range(n):
            row_t = []
            for j in range(n):
                v = matrix[i][j]
                row_t.append(f"{v:.2f}" if not np.isnan(v) else "")
            text_ann.append(row_t)

        # mask NaN as 0 for display
        matrix_disp = np.where(np.isnan(matrix), 0, matrix)

        fig3 = go.Figure(go.Heatmap(
            z=matrix_disp,
            x=filt_names, y=filt_names,
            zmin=-1, zmax=0,
            colorscale=[
                [0.0, "#7f1d1d"],
                [0.4, "#dc2626"],
                [0.7, "#1e1e2e"],
                [1.0, "#1e1e2e"],
            ],
            text=text_ann,
            texttemplate="%{text}",
            textfont=dict(size=10, color="#eeeef5"),
            hovertemplate="Promoter: %{y}<br>Victim: %{x}<br>ε = %{z:.2f}<extra></extra>",
            showscale=True,
            colorbar=dict(
                title=dict(text="Cross-ε", font=dict(color="#8888a8")),
                tickfont=dict(color="#8888a8"), thickness=12,
            ),
            xgap=2, ygap=2,
        ))
        fig3.update_layout(
            **PLOT,
            height=max(380, n * 28),
            margin=dict(t=20, b=100, l=180, r=20),
            xaxis=dict(tickangle=-35, tickfont=dict(size=10), side="bottom"),
            yaxis=dict(tickfont=dict(size=10), autorange="reversed"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── High-risk pairs ──
    st.markdown("<p class='sec-label'>High-Risk Product Pairs</p>", unsafe_allow_html=True)
    pairs = sorted(
        [(pid_i, pid_j, e)
         for (pid_i, pid_j), e in cross_elast.items()
         if e < 0
         and prod_map[pid_i]["category"] in sel_cats
         and prod_map[pid_j]["category"] in sel_cats],
        key=lambda x: x[2]
    )
    if not pairs:
        st.info("Tidak ada pasangan risiko pada kategori yang dipilih.")
    else:
        header = st.columns([3, 3, 1.5, 1.2, 1])
        header[0].markdown("<span style='font-size:10px;color:#5a5a7a;text-transform:uppercase;letter-spacing:.08em'>Promoter</span>", unsafe_allow_html=True)
        header[1].markdown("<span style='font-size:10px;color:#5a5a7a;text-transform:uppercase;letter-spacing:.08em'>Victim</span>", unsafe_allow_html=True)
        header[2].markdown("<span style='font-size:10px;color:#5a5a7a;text-transform:uppercase;letter-spacing:.08em'>ε</span>", unsafe_allow_html=True)
        header[3].markdown("<span style='font-size:10px;color:#5a5a7a;text-transform:uppercase;letter-spacing:.08em'>Risk</span>", unsafe_allow_html=True)
        header[4].markdown("<span style='font-size:10px;color:#5a5a7a;text-transform:uppercase;letter-spacing:.08em'>Same Brand</span>", unsafe_allow_html=True)

        for pid_i, pid_j, e in pairs[:20]:
            lvl, cls = badge(e)
            same_brand = prod_map[pid_i]["brand"] == prod_map[pid_j]["brand"]
            ca,cb,cc,cd,ce = st.columns([3,3,1.5,1.2,1])
            ca.markdown(f"<span style='font-size:12px;color:#eeeef5'>{prod_names[pid_i]}</span>", unsafe_allow_html=True)
            cb.markdown(f"<span style='font-size:12px;color:#f87171'>→ {prod_names[pid_j]}</span>", unsafe_allow_html=True)
            cc.markdown(f"<span style='font-size:12px;color:#8888a8;font-family:DM Mono,monospace'>{e:.2f}</span>", unsafe_allow_html=True)
            cd.markdown(f"<span class='badge {cls}'>{lvl}</span>", unsafe_allow_html=True)
            ce.markdown(f"<span style='font-size:12px;color:#{'34d399' if same_brand else '818cf8'}'>{'✓' if same_brand else '↔'}</span>", unsafe_allow_html=True)

    # ── Network-style concurrent promo risk ──
    st.markdown("<p class='sec-label'>Concurrent Promo Risk — Active SKUs</p>", unsafe_allow_html=True)
    active_pids = [pid for pid, d in discounts.items() if d > 0]
    if not active_pids:
        st.info("Aktifkan diskon di sidebar untuk melihat concurrent promo risk.")
    else:
        risk_rows = []
        for pid_a in active_pids:
            for pid_b in prod_ids:
                if pid_b == pid_a: continue
                e = cross_elast.get((pid_a, pid_b), 0.0)
                if e < -0.15:
                    est_loss = abs(prod_map[pid_b]["base_sales"] * e * discounts[pid_a] * prod_map[pid_b]["price"])
                    lvl, cls = badge(e)
                    risk_rows.append({
                        "Promoter": prod_names[pid_a],
                        "Victim":   prod_names[pid_b],
                        "ε":        e,
                        "Risk":     lvl,
                        "Est. Loss": f"Rp {est_loss/1e3:.0f}K",
                        "_cls":     cls,
                    })

        if not risk_rows:
            st.markdown("<span style='color:#34d399;font-size:13px'>✓ Tidak ada cannibalization signifikan dari SKU aktif.</span>", unsafe_allow_html=True)
        else:
            risk_rows.sort(key=lambda x: x["ε"])
            for row in risk_rows:
                ca,cb,cc,cd,ce = st.columns([3,3,1.5,1.2,1.5])
                ca.markdown(f"<span style='font-size:12px;color:#eeeef5'>{row['Promoter']}</span>", unsafe_allow_html=True)
                cb.markdown(f"<span style='font-size:12px;color:#f87171'>→ {row['Victim']}</span>", unsafe_allow_html=True)
                cc.markdown(f"<span style='font-size:12px;font-family:DM Mono,monospace;color:#8888a8'>{row['ε']:.2f}</span>", unsafe_allow_html=True)
                cls_val = row["_cls"]
                cd.markdown(f"<span class='badge {cls_val}'>{row['Risk']}</span>", unsafe_allow_html=True)
                ce.markdown(f"<span style='font-size:12px;color:#f87171'>{row['Est. Loss']}</span>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 3 — AI INSIGHTS
# ─────────────────────────────────────────────
with tab3:
    st.markdown("<p class='sec-label'>Portfolio Intelligence Report</p>", unsafe_allow_html=True)

    active_promos = [(pid, d) for pid, d in discounts.items() if d > 0]

    if not active_promos:
        st.info("Aktifkan minimal satu diskon dari sidebar untuk melihat insight.")
    else:
        lines = []
        sign  = "naik" if net_pct >= 0 else "turun"
        lines.append(f"📊 Net portfolio revenue <b>{sign} {abs(net_pct):.1f}%</b> (Rp {net_rev/1e3:+.0f}K) dari skenario ini dengan tipe promo <b>{promo_type_global}</b>.")

        cannib_victims = [r for pid,r in results.items() if r["cross_qty_delta"] < -30]
        if cannib_victims:
            vnames = ", ".join(v["name"] for v in cannib_victims[:3])
            lines.append(f"🔴 Terdeteksi <b>cannibalization</b> pada: {vnames}.")

        worst = min(results.values(), key=lambda r: r["rev_delta"])
        if worst["rev_delta"] < 0:
            lines.append(f"📉 Produk paling terdampak: <b>{worst['name']}</b> (Rp {worst['rev_delta']/1e3:.0f}K revenue lost).")

        best = max(results.values(), key=lambda r: r["rev_delta"])
        if best["rev_delta"] > 0:
            lines.append(f"📈 Uplift terbesar: <b>{best['name']}</b> (+Rp {best['rev_delta']/1e3:.0f}K).")

        cat_active: dict = {}
        for pid, d in active_promos:
            cat = prod_map[pid]["category"]
            cat_active.setdefault(cat, []).append(prod_map[pid]["name"])
        for cat, ns in cat_active.items():
            if len(ns) > 1:
                lines.append(f"⚠️ <b>{ns[0]}</b> dan <b>{ns[1]}</b> dipromosikan bersamaan di kategori <b>{cat}</b> — risiko kanibalisasi tinggi.")

        if promo_type_global == "Promo Bundling":
            lines.append("💡 Promo Bundling cenderung menarik volume tinggi tapi margin tipis — pastikan bundle partner tidak saling kanibal.")
        elif promo_type_global == "Promo Seasonal High":
            lines.append("💡 Promo Seasonal biasanya menaikkan seluruh kategori — waspadai SKU yang justru turun saat seasonal, itu sinyal kuat kanibalisasi.")

        st.markdown(f"""
        <div class='ai-card'>
            <div class='ai-card-title'>🤖 AI Portfolio Report — {promo_type_global}</div>
            <div class='ai-card-body'>{'<br><br>'.join(lines)}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p class='sec-label' style='margin-top:28px'>Risk per Active SKU</p>", unsafe_allow_html=True)
        for pid, d in active_promos:
            p = prod_map[pid]
            victims = sorted(
                [(cross_elast.get((pid, oid), 0.0), oid)
                 for oid in prod_ids if oid != pid and cross_elast.get((pid, oid), 0.0) < 0]
            )
            with st.expander(f"🎯 {p['name']} — {d*100:.0f}% · {promo_type_global}", expanded=len(active_promos) <= 3):
                if victims:
                    for e_val, oid in victims:
                        lvl, cls = badge(e_val)
                        est = abs(prod_map[oid]["base_sales"] * e_val * d * prod_map[oid]["price"])
                        c1,c2,c3,c4 = st.columns([3,1.5,2,1.5])
                        c1.markdown(f"<span style='font-size:12px;color:#eeeef5'>{prod_names[oid]}</span>", unsafe_allow_html=True)
                        c2.markdown(f"<span class='badge {cls}'>{lvl}</span>", unsafe_allow_html=True)
                        c3.markdown(f"<span style='font-size:12px;color:#f87171'>~Rp {est:,.0f} hilang</span>", unsafe_allow_html=True)
                        c4.markdown(f"<span style='font-size:12px;color:#8888a8;font-family:DM Mono,monospace'>ε={e_val:.2f}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:#34d399;font-size:12px'>✓ Tidak ada cannibalization terdeteksi</span>", unsafe_allow_html=True)

    # ── Upgrade note ──
    st.markdown("---")
    st.markdown("<p class='sec-label'>Upgrade ke Claude API</p>", unsafe_allow_html=True)
    st.code("""# .streamlit/secrets.toml → ANTHROPIC_API_KEY = "sk-ant-..."
import anthropic
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
msg = client.messages.create(
    model="claude-sonnet-4-20250514", max_tokens=600,
    messages=[{"role":"user","content": f"Pricing analyst Nabati. Beri rekomendasi: {summary}"}]
)
st.write(msg.content[0].text)""", language="python")
