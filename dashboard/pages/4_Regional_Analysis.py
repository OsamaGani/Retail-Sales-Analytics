
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Regional Analysis | Retail Analytics",
    page_icon="🌎",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "cleaned_sales.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    for col in ["Sales", "Profit", "Quantity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load sales data: {e}")
    st.stop()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --navy: #172554;
        --blue: #2563eb;
        --text: #1e293b;
        --muted: #64748b;
        --border: #e2e8f0;
        --surface: #ffffff;
        --page: #f5f7fb;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--page);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(245, 247, 251, 0.92);
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--navy);
        font-weight: 700;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #334155;
        font-weight: 500;
    }

    .main-title {
        font-size: 2.15rem;
        line-height: 1.2;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: var(--navy);
        margin: 0 0 7px 0;
    }

    .sub-title {
        color: var(--muted);
        font-size: 0.96rem;
        line-height: 1.6;
        margin-bottom: 1.6rem;
    }

    h2, h3 {
        color: var(--navy) !important;
        font-weight: 700 !important;
        letter-spacing: -0.25px;
    }

    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
        min-height: 112px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--navy) !important;
        font-size: 1.55rem !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        font-weight: 600;
    }

    [data-testid="stPlotlyChart"],
    [data-testid="stDataFrame"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 8px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
    }

    /* Improve Plotly chart text visibility */
    [data-testid="stPlotlyChart"] .js-plotly-plot svg text {
        font-family: Arial, sans-serif !important;
        text-rendering: geometricPrecision;
        -webkit-font-smoothing: antialiased;
    }

    [data-testid="stPlotlyChart"] .xtick text,
    [data-testid="stPlotlyChart"] .ytick text {
        fill: #334155 !important;
        font-size: 12px !important;
    }

    [data-testid="stPlotlyChart"] .gtitle {
        fill: #172554 !important;
        font-weight: 700 !important;
    }

    [data-testid="stDownloadButton"] button {
        background: var(--blue);
        color: #ffffff;
        border: 1px solid var(--blue);
        border-radius: 9px;
        padding: 0.55rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    [data-testid="stDownloadButton"] button:hover {
        background: #1d4ed8;
        border-color: #1d4ed8;
        color: #ffffff;
    }

    div[data-baseweb="select"] > div {
        border-radius: 9px;
        border-color: #cbd5e1;
    }

    hr {
        border-color: var(--border);
        margin-top: 1.4rem;
        margin-bottom: 1.4rem;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1500px;
    }

    @media (max-width: 768px) {
        .main-title {
            font-size: 1.7rem;
        }

        .sub-title {
            font-size: 0.88rem;
        }

        [data-testid="stMetric"] {
            padding: 13px;
        }
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CHART STYLING
# --------------------------------------------------

def style_chart(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(
            family="Arial, sans-serif",
            size=13,
            color="#334155"
        ),
        title=dict(
            font=dict(
                family="Arial, sans-serif",
                size=18,
                color="#172554"
            ),
            x=0.02,
            xanchor="left"
        ),
        margin=dict(
            l=25,
            r=25,
            t=65,
            b=25
        ),
        legend=dict(
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="#334155"
            ),
            title_font=dict(
                size=13,
                color="#172554"
            )
        )
    )

    fig.update_xaxes(
        showline=True,
        linecolor="#e2e8f0",
        tickfont=dict(
            family="Arial, sans-serif",
            size=12,
            color="#334155"
        ),
        title_font=dict(
            family="Arial, sans-serif",
            size=13,
            color="#172554"
        ),
        gridcolor="#eef2f7",
        zerolinecolor="#e2e8f0"
    )

    fig.update_yaxes(
        showline=True,
        linecolor="#e2e8f0",
        tickfont=dict(
            family="Arial, sans-serif",
            size=12,
            color="#334155"
        ),
        title_font=dict(
            family="Arial, sans-serif",
            size=13,
            color="#172554"
        ),
        gridcolor="#eef2f7",
        zerolinecolor="#e2e8f0"
    )

    return fig


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("🌎 Regional Analysis")
st.sidebar.markdown("---")

regions = st.sidebar.multiselect(
    "Select Region",
    sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

states = st.sidebar.multiselect(
    "Select State",
    sorted(df["State"].dropna().unique()),
    default=sorted(df["State"].dropna().unique())
)

segments = st.sidebar.multiselect(
    "Customer Segment",
    sorted(df["Segment"].dropna().unique()),
    default=sorted(df["Segment"].dropna().unique())
)


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if regions:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(regions)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if states:
    filtered_df = filtered_df[
        filtered_df["State"].isin(states)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if segments:
    filtered_df = filtered_df[
        filtered_df["Segment"].isin(segments)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">Regional Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Explore sales, profit and customer performance across different regions and states.</div>',
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning("No regional data found for the selected filters.")
    st.stop()


# --------------------------------------------------
# REGIONAL KPIs
# --------------------------------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_states = filtered_df["State"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("States Covered", f"{total_states:,}")

st.markdown("---")


# --------------------------------------------------
# REGION PERFORMANCE
# --------------------------------------------------

st.subheader("📊 Region-wise Performance")

region_summary = (
    filtered_df.groupby("Region", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique")
    )
)

col1, col2 = st.columns(2)

with col1:
    fig_region_sales = px.bar(
        region_summary.sort_values("Sales"),
        x="Sales",
        y="Region",
        orientation="h",
        color="Sales",
        title="Revenue by Region",
        labels={
            "Sales": "Revenue ($)",
            "Region": "Region"
        }
    )

    fig_region_sales = style_chart(fig_region_sales)

    fig_region_sales.update_layout(
        coloraxis_colorbar=dict(
            title="Revenue",
            tickfont=dict(size=12, color="#334155")
        )
    )

    fig_region_sales.update_xaxes(showgrid=True)
    fig_region_sales.update_yaxes(showgrid=False)

    st.plotly_chart(fig_region_sales, width="stretch")

with col2:
    fig_region_profit = px.bar(
        region_summary.sort_values("Profit"),
        x="Profit",
        y="Region",
        orientation="h",
        color="Profit",
        title="Profit by Region",
        labels={
            "Profit": "Profit ($)",
            "Region": "Region"
        }
    )

    fig_region_profit = style_chart(fig_region_profit)

    fig_region_profit.update_layout(
        coloraxis_colorbar=dict(
            title="Profit",
            tickfont=dict(size=12, color="#334155")
        )
    )

    fig_region_profit.update_xaxes(showgrid=True)
    fig_region_profit.update_yaxes(showgrid=False)

    st.plotly_chart(fig_region_profit, width="stretch")


# --------------------------------------------------
# REGIONAL REVENUE SHARE
# --------------------------------------------------

st.subheader("🌎 Regional Revenue Contribution")

fig_region_pie = px.pie(
    region_summary,
    names="Region",
    values="Sales",
    hole=0.45,
    title="Revenue Share by Region"
)

fig_region_pie = style_chart(fig_region_pie)

fig_region_pie.update_layout(
    legend_title_text=""
)

fig_region_pie.update_traces(
    textfont=dict(
        family="Arial, sans-serif",
        size=13,
        color="#ffffff"
    )
)

st.plotly_chart(fig_region_pie, width="stretch")


# --------------------------------------------------
# STATE-WISE SALES
# --------------------------------------------------

st.subheader("📍 State-wise Sales Performance")

state_summary = (
    filtered_df.groupby("State", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .sort_values("Sales", ascending=False)
)

top_states = state_summary.head(15)

fig_states = px.bar(
    top_states.sort_values("Sales"),
    x="Sales",
    y="State",
    orientation="h",
    color="Sales",
    title="Top 15 States by Revenue",
    labels={
        "Sales": "Revenue ($)",
        "State": "State"
    }
)

fig_states = style_chart(fig_states)

fig_states.update_layout(
    coloraxis_colorbar=dict(
        title="Revenue",
        tickfont=dict(size=12, color="#334155")
    )
)

fig_states.update_xaxes(showgrid=True)
fig_states.update_yaxes(showgrid=False)

st.plotly_chart(fig_states, width="stretch")


# --------------------------------------------------
# STATE-WISE PROFIT
# --------------------------------------------------

st.subheader("💰 State-wise Profit Analysis")

top_profit_states = (
    state_summary.sort_values("Profit", ascending=False)
    .head(15)
)

fig_state_profit = px.bar(
    top_profit_states.sort_values("Profit"),
    x="Profit",
    y="State",
    orientation="h",
    color="Profit",
    title="Top 15 States by Profit",
    labels={
        "Profit": "Profit ($)",
        "State": "State"
    }
)

fig_state_profit = style_chart(fig_state_profit)

fig_state_profit.update_layout(
    coloraxis_colorbar=dict(
        title="Profit",
        tickfont=dict(size=12, color="#334155")
    )
)

fig_state_profit.update_xaxes(showgrid=True)
fig_state_profit.update_yaxes(showgrid=False)

st.plotly_chart(fig_state_profit, width="stretch")


# --------------------------------------------------
# REGIONAL CATEGORY ANALYSIS
# --------------------------------------------------

st.subheader("🛍️ Category Performance Across Regions")

region_category = (
    filtered_df.groupby(
        ["Region", "Category"],
        as_index=False
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

fig_region_category = px.bar(
    region_category,
    x="Region",
    y="Sales",
    color="Category",
    barmode="group",
    title="Category-wise Revenue Across Regions",
    labels={
        "Sales": "Revenue ($)",
        "Region": "Region",
        "Category": "Category"
    }
)

fig_region_category = style_chart(fig_region_category)

fig_region_category.update_layout(
    legend_title_text=""
)

fig_region_category.update_xaxes(showgrid=False)
fig_region_category.update_yaxes(showgrid=True)

st.plotly_chart(fig_region_category, width="stretch")


# --------------------------------------------------
# REGIONAL SEGMENT ANALYSIS
# --------------------------------------------------

st.subheader("👥 Customer Segment Across Regions")

region_segment = (
    filtered_df.groupby(
        ["Region", "Segment"],
        as_index=False
    )["Sales"]
    .sum()
)

fig_segment = px.bar(
    region_segment,
    x="Region",
    y="Sales",
    color="Segment",
    barmode="stack",
    title="Customer Segment Revenue by Region",
    labels={
        "Sales": "Revenue ($)",
        "Region": "Region",
        "Segment": "Customer Segment"
    }
)

fig_segment = style_chart(fig_segment)

fig_segment.update_layout(
    legend_title_text=""
)

fig_segment.update_xaxes(showgrid=False)
fig_segment.update_yaxes(showgrid=True)

st.plotly_chart(fig_segment, width="stretch")


# --------------------------------------------------
# COMPLETE REGIONAL TABLE
# --------------------------------------------------

st.subheader("📋 Regional Performance Summary")

st.dataframe(
    region_summary.round(2),
    width="stretch",
    hide_index=True
)


# --------------------------------------------------
# STATE PERFORMANCE TABLE
# --------------------------------------------------

st.subheader("📌 Complete State Performance")

st.dataframe(
    state_summary.round(2),
    width="stretch",
    hide_index=True
)


# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

csv_data = state_summary.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Regional Report",
    data=csv_data,
    file_name="regional_analysis_report.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption("Retail Sales Analytics & Business Intelligence System")
