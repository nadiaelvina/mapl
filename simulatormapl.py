import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="MAPL+ | Portfolio Pricing Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e0e0e0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
}
[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

/* ── Header brand ── */
.brand-header {
    padding: 1.5rem 0 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.5rem;
}
.brand-title {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ff4e4e, #ff8c42);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
    margin: 0;
}
.brand-subtitle {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.4);
    font-weight: 400;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── KPI Cards ── */
.kpi-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, border-color 0.2s;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(255,78,78,0.3);
}
.kpi-label {
    font-size: 0.7rem;
    font-weight: 500;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}
.kpi-delta-neg {
    font-size: 0.8rem;
    font-weight: 500;
    color: #ff4e4e;
}
.kpi-delta-pos {
    font-size: 0.8rem;
    font-weight: 500;
    color: #4caf50;
}
.kpi-delta-neutral {
    font-size: 0.8rem;
    font-weight: 500;
    color: rgba(255,255,255,0.4);
}

/* ── Section headers ── */
.section-header {
    font-size: 0.7rem;
    font-weight: 600;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 1.5rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.08);
}

/* ── Chart containers ── */
.chart-container {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1rem;
}

/* ── AI Recommendation card ── */
.rec-card {
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-top: 0.5rem;
    border-left: 4px solid;
}
.rec-card-green {
    background: rgba(76,175,80,0.08);
    border-color: #4caf50;
}
.rec-card-yellow {
    background: rgba(255,193,7,0.08);
    border-color: #ffc107;
}
.rec-card-red {
    background: rgba(255,78,78,0.08);
    border-color: #ff4e4e;
}
.rec-verdict {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
    color: #ffffff;
}
.rec-detail {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.6);
    line-height: 1.7;
}
.rec-detail b {
    color: rgba(255,255,255,0.9);
}

/* ── Disclaimer ── */
.disclaimer {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.35);
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin: 0.5rem 0 1rem 0;
    border-left: 3px solid rgba(255,140,66,0.4);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.07);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: rgba(255,255,255,0.5) !important;
    font-weight: 500;
    font-size: 0.85rem;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,78,78,0.15) !important;
    color: #ff4e4e !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #ff4e4e, #ff8c42) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: opacity 0.2s, transform 0.2s !important;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* ── Selectbox & Slider ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: white !important;
}
.stSlider [data-baseweb="slider"] {
    margin-top: 0.3rem;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.07);
}

/* ── Multiselect ── */
[data-testid="stMultiSelect"] span {
    background: rgba(255,78,78,0.15) !important;
    color: #ff8c42 !important;
    border-radius: 6px !important;
}

/* ── Metric override ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: rgba(255,255,255,0.4) !important;
}
[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Plotly dark theme config ──────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='rgba(255,255,255,0.7)', size=11),
    xaxis=dict(gridcolor='rgba(255,255,255,0.06)', linecolor='rgba(255,255,255,0.1)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.06)', linecolor='rgba(255,255,255,0.1)'),
    legend=dict(bgcolor='rgba(255,255,255,0.04)',
                bordercolor='rgba(255,255,255,0.08)',
                borderwidth=1, font_size=10),
    margin=dict(l=10, r=10, t=40, b=10),
)

COLORS = {
    'primary':   '#ff4e4e',
    'secondary': '#ff8c42',
    'blue':      '#4fc3f7',
    'green':     '#4caf50',
    'purple':    '#9c27b0',
    'text_dim':  'rgba(255,255,255,0.4)',
}

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    sku_overview    = pd.read_csv('sku_overview.csv')
    price_lookup_df = pd.read_csv('price_lookup.csv')
    matrix_df       = pd.read_csv('cannibalization_matrix.csv', index_col=0)
    elast_df        = pd.read_csv('elasticity_per_sku.csv')
    forecast_df     = pd.read_csv('base_forecast.csv')

    sku_meta = (sku_overview[['SKU_ID','SKU','Brand','SKU_Category']]
                .drop_duplicates().reset_index(drop=True))
    elast_lookup = dict(zip(elast_df['SKU_ID'], elast_df['FinalElasticity']))
    price_lookup = dict(zip(price_lookup_df['SKU_ID'], price_lookup_df['NormalPrice']))

    return sku_overview, sku_meta, matrix_df, elast_lookup, price_lookup, forecast_df

sku_overview, sku_meta, matrix_df, elast_lookup, price_lookup, forecast_df = load_data()

# ── Simulator engine ──────────────────────────────────────────────────────────
def simulate_portfolio_impact(sku_a_id, discount_pct, branch, weeks=4):
    skus      = sku_meta['SKU_ID'].tolist()
    sku_name  = dict(zip(sku_meta['SKU_ID'], sku_meta['SKU']))
    sku_cat   = dict(zip(sku_meta['SKU_ID'], sku_meta['SKU_Category']))
    sku_brand = dict(zip(sku_meta['SKU_ID'], sku_meta['Brand']))
    elast_a      = elast_lookup.get(sku_a_id, -1.0)
    uplift_pct_a = elast_a * (-discount_pct)

    rows = []
    for week in range(1, weeks + 1):
        def get_base(sku_id):
            val = forecast_df[
                (forecast_df['SKU_ID']==sku_id) &
                (forecast_df['Branch']==branch) &
                (forecast_df['ForecastWeek']==week)
            ]['BaseForecast']
            return val.values[0] if len(val) > 0 else 0

        base_qty_a   = get_base(sku_a_id)
        uplift_qty_a = base_qty_a * uplift_pct_a

        for sku_b_id in skus:
            base_qty_b     = get_base(sku_b_id)
            normal_price_b = price_lookup.get(sku_b_id, 0)

            if sku_b_id == sku_a_id:
                adj_qty     = base_qty_b * (1 + uplift_pct_a)
                delta_qty   = adj_qty - base_qty_b
                disc_price  = normal_price_b * (1 - discount_pct)
                base_rev    = base_qty_b * normal_price_b
                adj_rev     = adj_qty * disc_price
                effect_type = 'Promo Uplift'
                coef        = 0.0
            else:
                coef = float(matrix_df.loc[sku_a_id, sku_b_id]) if (
                    sku_a_id in matrix_df.index and
                    sku_b_id in matrix_df.columns) else 0.0
                loss_qty_b  = uplift_qty_a * coef
                adj_qty     = max(base_qty_b - loss_qty_b, 0)
                delta_qty   = adj_qty - base_qty_b
                base_rev    = base_qty_b * normal_price_b
                adj_rev     = adj_qty * normal_price_b
                effect_type = 'Cannibalization' if coef > 0 else 'No Effect'

            rows.append({
                'Week': week, 'SKU_ID': sku_b_id,
                'SKU': sku_name.get(sku_b_id,''),
                'Brand': sku_brand.get(sku_b_id,''),
                'Category': sku_cat.get(sku_b_id,''),
                'BaseQty': round(base_qty_b, 1),
                'AdjustedQty': round(adj_qty, 1),
                'DeltaQty': round(delta_qty, 1),
                'BaseRevenue': round(base_rev, 0),
                'AdjustedRevenue': round(adj_rev, 0),
                'DeltaRevenue': round(adj_rev - base_rev, 0),
                'EffectType': effect_type,
                'CannibCoef': coef,
            })

    weekly_df = pd.DataFrame(rows)
    summary   = (weekly_df.groupby(['SKU_ID','SKU','Brand','Category','EffectType'])
                          .agg(
                              TotalBaseQty  = ('BaseQty','sum'),
                              TotalAdjQty   = ('AdjustedQty','sum'),
                              TotalDeltaQty = ('DeltaQty','sum'),
                              TotalBaseRev  = ('BaseRevenue','sum'),
                              TotalAdjRev   = ('AdjustedRevenue','sum'),
                              TotalDeltaRev = ('DeltaRevenue','sum'),
                          ).reset_index())

    port_base      = summary['TotalBaseRev'].sum()
    port_adj       = summary['TotalAdjRev'].sum()
    port_delta     = port_adj - port_base
    port_delta_pct = port_delta / port_base * 100 if port_base > 0 else 0

    return weekly_df, summary, port_base, port_adj, port_delta, port_delta_pct

# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
        <div class='brand-header'>
            <div class='brand-title'>MAPL+</div>
            <div class='brand-subtitle'>Portfolio Pricing Intelligence</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Simulation Parameters</div>",
                unsafe_allow_html=True)

    sku_options       = dict(zip(sku_meta['SKU'], sku_meta['SKU_ID']))
    selected_sku_name = st.selectbox("SKU Target (Aggressor)",
                                      options=list(sku_options.keys()))
    selected_sku_id   = sku_options[selected_sku_name]

    selected_branch = st.selectbox("Branch",
                                    ['Jakarta','Surabaya','Bandung','Semarang'])

    discount_pct = st.slider("Discount Level (%)",
                              min_value=5, max_value=50, value=20, step=5) / 100

    # Info SKU yang dipilih
    sku_info = sku_meta[sku_meta['SKU_ID'] == selected_sku_id].iloc[0]
    elast_val = elast_lookup.get(selected_sku_id, -1.0)

    st.markdown("<div class='section-header'>SKU Info</div>",
                unsafe_allow_html=True)
    st.markdown(f"""
        <div style='font-size:0.78rem; color:rgba(255,255,255,0.5); line-height:2'>
            <b style='color:rgba(255,255,255,0.85)'>Brand:</b> {sku_info['Brand']}<br>
            <b style='color:rgba(255,255,255,0.85)'>Category:</b> {sku_info['SKU_Category']}<br>
            <b style='color:rgba(255,255,255,0.85)'>Elasticity:</b> {elast_val:.3f}<br>
            <b style='color:rgba(255,255,255,0.85)'>Normal Price:</b> Rp {price_lookup.get(selected_sku_id,0):,.0f}<br>
            <b style='color:rgba(255,255,255,0.85)'>Discounted Price:</b> Rp {price_lookup.get(selected_sku_id,0)*(1-discount_pct):,.0f}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Run Simulation", use_container_width=True)

    st.markdown("<div class='section-header'>About</div>",
                unsafe_allow_html=True)
    st.markdown("""
        <div style='font-size:0.72rem; color:rgba(255,255,255,0.3); line-height:1.8'>
            MAPL+ extends MAPL with portfolio-aware<br>
            pricing intelligence using:<br>
            • Own-price elasticity (OLS log-log)<br>
            • Cannibalization detection (DiD)<br>
            • Demand forecasting (Linear Trend)<br>
            <br>
            <i>Nabati Group · Capstone 2025</i>
        </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <div style='padding: 0.5rem 0 1rem 0'>
        <h2 style='color:white; font-weight:700; font-size:1.4rem; margin:0'>
            Portfolio Impact Simulator
        </h2>
        <p style='color:rgba(255,255,255,0.35); font-size:0.82rem; margin:4px 0 0 0'>
            Simulate price promotion effects across the entire product portfolio · 4-week horizon
        </p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "  🎯  What-If Simulator  ",
    "  🔥  Cannibalization Heatmap  ",
    "  📋  SKU Overview  "
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — SIMULATOR
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    if not run_btn:
        # Empty state
        st.markdown("""
            <div style='
                text-align:center;
                padding: 5rem 2rem;
                color: rgba(255,255,255,0.2);
            '>
                <div style='font-size:3rem; margin-bottom:1rem'>📊</div>
                <div style='font-size:1rem; font-weight:500; margin-bottom:0.5rem;
                            color:rgba(255,255,255,0.35)'>
                    Configure your simulation in the sidebar
                </div>
                <div style='font-size:0.8rem'>
                    Select a SKU, branch, and discount level, then click Run Simulation
                </div>
            </div>
        """, unsafe_allow_html=True)

    else:
        with st.spinner("Running portfolio simulation..."):
            weekly_df, summary, port_base, port_adj, port_delta, port_delta_pct = \
                simulate_portfolio_impact(selected_sku_id, discount_pct, selected_branch)

        sku_row     = summary[summary['SKU_ID'] == selected_sku_id].iloc[0]
        cannib_rows = summary[summary['EffectType'] == 'Cannibalization']
        uplift_show = elast_val * (-discount_pct) * 100

        # ── KPI Cards ──────────────────────────────────────────────────────
        st.markdown("<div class='section-header'>Portfolio Impact Summary</div>",
                    unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)

        delta_color  = "kpi-delta-neg" if port_delta < 0 else "kpi-delta-pos"
        delta_arrow  = "↓" if port_delta < 0 else "↑"
        net_qty      = summary['TotalDeltaQty'].sum()
        net_color    = "kpi-delta-neg" if net_qty < 0 else "kpi-delta-pos"

        with c1:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Portfolio ΔRevenue</div>
                    <div class='kpi-value'>Rp {abs(port_delta)/1e6:.1f}M</div>
                    <div class='{delta_color}'>{delta_arrow} {abs(port_delta_pct):.1f}% vs baseline</div>
                </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Volume Uplift (Target SKU)</div>
                    <div class='kpi-value'>+{sku_row['TotalDeltaQty']:,.0f}</div>
                    <div class='kpi-delta-pos'>↑ {uplift_show:.1f}% demand increase</div>
                </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>SKUs Cannibalized</div>
                    <div class='kpi-value'>{len(cannib_rows)}</div>
                    <div class='kpi-delta-neg'>↓ {abs(cannib_rows['TotalDeltaQty'].sum()):,.0f} units lost</div>
                </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Net Portfolio Volume</div>
                    <div class='kpi-value'>{net_qty:+,.0f}</div>
                    <div class='{net_color}'>{'↓' if net_qty < 0 else '↑'} net unit change</div>
                </div>
            """, unsafe_allow_html=True)

        # Disclaimer
        st.markdown(f"""
            <div class='disclaimer'>
                ℹ️ Revenue SKU target dapat negatif meski volume naik —
                karena harga jual turun dari Rp {price_lookup.get(selected_sku_id,0):,.0f}
                menjadi Rp {price_lookup.get(selected_sku_id,0)*(1-discount_pct):,.0f}
                (price-volume tradeoff). Portfolio ΔRevenue sudah memperhitungkan hal ini.
            </div>
        """, unsafe_allow_html=True)

        # ── Charts ─────────────────────────────────────────────────────────
        st.markdown("<div class='section-header'>Revenue & Volume Analysis</div>",
                    unsafe_allow_html=True)

        col_left, col_right = st.columns(2)

        # Chart 1: Revenue impact
        with col_left:
            affected = summary[summary['EffectType'] != 'No Effect'].copy()
            affected = affected.sort_values('TotalDeltaRev')

            fig_bar = go.Figure(go.Bar(
                x=affected['TotalDeltaRev'],
                y=affected['SKU'],
                orientation='h',
                marker=dict(
                    color=['#4fc3f7' if e == 'Promo Uplift' else '#ff4e4e'
                           for e in affected['EffectType']],
                    opacity=0.85,
                    line=dict(width=0),
                ),
                hovertemplate='<b>%{y}</b><br>ΔRevenue: Rp %{x:,.0f}<extra></extra>',
            ))
            fig_bar.update_layout(
                **PLOT_LAYOUT,
                title=dict(text='Revenue Impact per SKU (4 Weeks)',
                          font=dict(size=12, color='rgba(255,255,255,0.7)')),
                height=420,
                margin=dict(l=200, r=80, t=40, b=20),
                yaxis=dict(tickfont_size=9,
                           gridcolor='rgba(255,255,255,0.04)',
                           linecolor='rgba(255,255,255,0.08)'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.04)',
                           linecolor='rgba(255,255,255,0.08)'),
            )
            fig_bar.add_vline(x=0, line_color='rgba(255,255,255,0.15)',
                              line_width=1)
            st.plotly_chart(fig_bar, use_container_width=True)

        # Chart 2: Weekly projection
        with col_right:
            top_cannib = (cannib_rows.nsmallest(3, 'TotalDeltaRev')['SKU_ID'].tolist()
                          + [selected_sku_id])
            top_cannib = list(dict.fromkeys(top_cannib))

            fig_line = go.Figure()
            palette = ['#ff4e4e','#4fc3f7','#ff8c42','#9c27b0','#4caf50']

            for i, sku_id in enumerate(top_cannib):
                sub       = weekly_df[weekly_df['SKU_ID'] == sku_id]
                sku_label = sku_meta[sku_meta['SKU_ID']==sku_id]['SKU'].values[0]
                is_target = sku_id == selected_sku_id
                color     = palette[i % len(palette)]

                # Base (dotted)
                fig_line.add_trace(go.Scatter(
                    x=sub['Week'], y=sub['BaseQty'],
                    mode='lines',
                    line=dict(dash='dot', color=color, width=1),
                    opacity=0.3, showlegend=False,
                ))
                # Adjusted (solid)
                fig_line.add_trace(go.Scatter(
                    x=sub['Week'], y=sub['AdjustedQty'],
                    mode='lines+markers',
                    name=sku_label[:22] + (' 🎯' if is_target else ''),
                    line=dict(color=color,
                              width=2.5 if is_target else 1.5,
                              dash='solid' if is_target else 'dash'),
                    marker=dict(size=7 if is_target else 4,
                                symbol='circle',
                                line=dict(width=2 if is_target else 0,
                                          color='white')),
                ))

            fig_line.update_layout(
                **PLOT_LAYOUT,
                title=dict(text='Projected Weekly Qty — Adjusted vs Baseline',
                          font=dict(size=12, color='rgba(255,255,255,0.7)')),
                height=420,
                xaxis=dict(tickvals=[1,2,3,4],
                           title='Week',
                           gridcolor='rgba(255,255,255,0.04)'),
                yaxis=dict(title='Weekly Qty',
                           gridcolor='rgba(255,255,255,0.04)'),
                legend=dict(orientation='h', yanchor='bottom',
                            y=-0.3, xanchor='left', x=0,
                            font_size=9),
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # ── Detail Table ────────────────────────────────────────────────────
        st.markdown("<div class='section-header'>SKU-Level Detail</div>",
                    unsafe_allow_html=True)

        display = summary[['SKU','Brand','Category','EffectType',
                            'TotalBaseQty','TotalDeltaQty',
                            'TotalBaseRev','TotalDeltaRev']].copy()
        display.columns = ['SKU','Brand','Category','Effect',
                            'Base Qty','Δ Qty','Base Rev (Rp)','Δ Rev (Rp)']
        display = display.sort_values('Δ Rev (Rp)')

        def color_delta(val):
            if val < 0:   return 'color: #ff4e4e'
            elif val > 0: return 'color: #4caf50'
            return 'color: rgba(255,255,255,0.3)'

        st.dataframe(
            display.style
                   .map(color_delta, subset=['Δ Qty','Δ Rev (Rp)'])
                   .format({'Base Qty':'{:,.0f}','Δ Qty':'{:+,.0f}',
                            'Base Rev (Rp)':'{:,.0f}','Δ Rev (Rp)':'{:+,.0f}'}),
            use_container_width=True, height=380
        )

        # ── AI Recommendation ───────────────────────────────────────────────
        st.markdown("<div class='section-header'>AI Recommendation</div>",
                    unsafe_allow_html=True)

        worst = summary[summary['EffectType']=='Cannibalization'].nsmallest(1,'TotalDeltaRev')
        wv_name = worst['SKU'].values[0] if len(worst) > 0 else '-'
        wv_rev  = worst['TotalDeltaRev'].values[0] if len(worst) > 0 else 0

        if port_delta_pct > 0:
            card_class = 'rec-card-green'
            icon       = '✅'
            verdict    = 'Promo ini menguntungkan portfolio secara keseluruhan.'
            rec        = 'Lanjutkan promo dengan monitoring mingguan terhadap SKU yang terdampak.'
        elif port_delta_pct > -3:
            card_class = 'rec-card-yellow'
            icon       = '⚠️'
            verdict    = 'Promo ini memberikan dampak negatif ringan ke portfolio.'
            rec        = f'Pertimbangkan menurunkan discount ke {int(discount_pct*100)-5}% untuk meminimalkan cannibalization.'
        else:
            card_class = 'rec-card-red'
            icon       = '🔴'
            verdict    = 'Promo ini berisiko tinggi — cannibalization melebihi uplift revenue.'
            rec        = 'Tidak disarankan tanpa adjustment. Evaluasi ulang discount level atau batasi ke branch tertentu.'

        st.markdown(f"""
            <div class='rec-card {card_class}'>
                <div class='rec-verdict'>{icon} {verdict}</div>
                <div class='rec-detail'>
                    <b>Portfolio Impact:</b> Rp {port_delta:,.0f} ({port_delta_pct:.1f}%) selama 4 minggu<br>
                    <b>SKU paling terdampak:</b> {wv_name} (Rp {wv_rev:,.0f})<br>
                    <b>Elasticity SKU target:</b> {elast_val:.3f}
                    → volume uplift {uplift_show:.1f}% dengan diskon {discount_pct*100:.0f}%<br>
                    <b>Rekomendasi:</b> {rec}
                </div>
            </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — CANNIBALIZATION HEATMAP
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
        <div style='padding: 0.5rem 0 1rem 0'>
            <h3 style='color:white; font-weight:600; font-size:1.1rem; margin:0'>
                Cannibalization Coefficient Matrix
            </h3>
            <p style='color:rgba(255,255,255,0.35); font-size:0.8rem; margin:4px 0 0 0'>
                Estimated via Difference-in-Differences · Van Heerde et al. (2004)
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        filter_brand = st.multiselect(
            "Filter Brand",
            options=sku_meta['Brand'].unique(),
            default=sku_meta['Brand'].unique().tolist()
        )
    with col_f2:
        show_zeros = st.checkbox("Show zero cells", value=False)

    filtered_skus = sku_meta[sku_meta['Brand'].isin(filter_brand)]['SKU_ID'].tolist()
    sku_labels    = sku_meta[sku_meta['Brand'].isin(filter_brand)]['SKU'].str[:22].tolist()

    mat = matrix_df.loc[filtered_skus, filtered_skus].copy()
    mat.index   = sku_labels
    mat.columns = sku_labels

    text_mat = np.where(
        mat.values > 0,
        np.round(mat.values, 3).astype(str),
        '·' if show_zeros else ''
    )

    fig_heat = go.Figure(go.Heatmap(
        z=mat.values,
        x=mat.columns.tolist(),
        y=mat.index.tolist(),
        colorscale=[[0,'rgba(0,0,0,0)'],
                    [0.01,'rgba(255,78,78,0.1)'],
                    [0.5,'rgba(255,78,78,0.5)'],
                    [1,'rgba(255,78,78,0.95)']],
        zmin=0, zmax=0.25,
        text=text_mat,
        texttemplate='%{text}',
        textfont=dict(size=8, color='rgba(255,255,255,0.8)'),
        colorbar=dict(
            title=dict(text='Coef', font=dict(color='rgba(255,255,255,0.5)', size=10)),
            tickfont=dict(color='rgba(255,255,255,0.5)', size=9),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(255,255,255,0.1)',
        ),
        hovertemplate='<b>%{y}</b> → <b>%{x}</b><br>Coef: %{z:.3f}<extra></extra>',
    ))
    fig_heat.update_layout(
        **PLOT_LAYOUT,
        height=580,
        xaxis=dict(tickfont_size=8, side='bottom'),
        yaxis=dict(tickfont_size=8, autorange='reversed'),
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""
        <div style='font-size:0.78rem; color:rgba(255,255,255,0.35);
                    background:rgba(255,255,255,0.03); border-radius:8px;
                    padding:0.7rem 1rem; border-left:3px solid rgba(255,78,78,0.3)'>
            <b style='color:rgba(255,255,255,0.6)'>Cara baca:</b>
            Baris = SKU aggressor (yang diberi promo) · Kolom = SKU victim ·
            Nilai 0.19 artinya ketika aggressor promo, demand victim
            rata-rata 19% di bawah baseline ekspektasinya ·
            Sel kosong = tidak ada bukti cannibalization signifikan (p ≥ 0.05)
        </div>
    """, unsafe_allow_html=True)

    # Top pairs
    st.markdown("<div class='section-header'>Top Cannibalization Pairs</div>",
                unsafe_allow_html=True)
    pairs = []
    for a, row in mat.iterrows():
        for b, val in row.items():
            if val > 0:
                pairs.append({'Aggressor SKU': a, 'Victim SKU': b,
                               'Coefficient': val})
    if pairs:
        pairs_df = (pd.DataFrame(pairs)
                      .sort_values('Coefficient', ascending=False)
                      .reset_index(drop=True))
        st.dataframe(
            pairs_df.style.format({'Coefficient': '{:.3f}'}),
            use_container_width=True, height=280
        )

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — SKU OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
        <div style='padding: 0.5rem 0 1rem 0'>
            <h3 style='color:white; font-weight:600; font-size:1.1rem; margin:0'>
                SKU Performance Overview
            </h3>
            <p style='color:rgba(255,255,255,0.35); font-size:0.8rem; margin:4px 0 0 0'>
                Historical performance · May–September 2025
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_f, _ = st.columns([1, 3])
    with col_f:
        branch_filter = st.selectbox(
            "Branch", ['All','Jakarta','Surabaya','Bandung','Semarang'])

    if branch_filter == 'All':
        df_view = (sku_overview.groupby(['SKU_ID','SKU','Brand','SKU_Category'])
                               .agg(TotalQty=('TotalQty','sum'),
                                    TotalRevenue=('TotalRevenue','sum'),
                                    TotalTx=('TotalTx','sum'),
                                    AvgDiscount=('AvgDiscount','mean'))
                               .reset_index())
    else:
        df_view = (sku_overview[sku_overview['Brand'].isin(
                       sku_overview['Brand'].unique())]  # all brands
                               if branch_filter == 'All' else
                   sku_overview[sku_overview['Branch']==branch_filter]
                               .groupby(['SKU_ID','SKU','Brand','SKU_Category'])
                               .agg(TotalQty=('TotalQty','sum'),
                                    TotalRevenue=('TotalRevenue','sum'),
                                    TotalTx=('TotalTx','sum'),
                                    AvgDiscount=('AvgDiscount','mean'))
                               .reset_index())

    if branch_filter != 'All':
        pass  # already filtered above
    
    sku_summary = df_view.sort_values('TotalRevenue', ascending=False)
    sku_summary['AvgDiscount'] = (sku_summary['AvgDiscount'] * 100).round(1)

    brand_colors = {'Richeese':'#ff4e4e','Richoco':'#ff8c42','Nextar':'#4fc3f7'}

    col_a, col_b = st.columns(2)
    with col_a:
        fig_rev = px.bar(sku_summary, x='TotalRevenue', y='SKU',
                         color='Brand', orientation='h',
                         color_discrete_map=brand_colors,
                         title='Total Revenue per SKU')
        fig_rev.update_layout(**PLOT_LAYOUT, height=520,
                              yaxis={'categoryorder':'total ascending',
                                     'tickfont':{'size':9}})
        st.plotly_chart(fig_rev, use_container_width=True)

    with col_b:
        fig_qty = px.bar(sku_summary, x='TotalQty', y='SKU',
                         color='Brand', orientation='h',
                         color_discrete_map=brand_colors,
                         title='Total Volume per SKU')
        fig_qty.update_layout(**PLOT_LAYOUT, height=520,
                              yaxis={'categoryorder':'total ascending',
                                     'tickfont':{'size':9}})
        st.plotly_chart(fig_qty, use_container_width=True)

    st.dataframe(
        sku_summary[['SKU','Brand','SKU_Category','TotalQty',
                     'TotalRevenue','TotalTx','AvgDiscount']]
                  .rename(columns={'SKU_Category':'Category',
                                   'TotalQty':'Total Qty',
                                   'TotalRevenue':'Revenue (Rp)',
                                   'TotalTx':'Transactions',
                                   'AvgDiscount':'Avg Disc %'})
                  .style.format({'Total Qty':'{:,.0f}',
                                 'Revenue (Rp)':'{:,.0f}',
                                 'Transactions':'{:,.0f}',
                                 'Avg Disc %':'{:.1f}%'}),
        use_container_width=True
    )
