from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Sales Analysis | Retail Analytics",
    page_icon="📈",
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
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Month Year"] = df["Order Date"].dt.to_period("M").astype(str)

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
        --blue-light: #eff6ff;
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
        color: var(--navy) !important;
        font-weight: 700;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #334155 !important;
        font-weight: 500;
    }

    .main-title {
        font-size: 2.15rem;
        line-height: 1.2;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: var(--navy) !important;
        margin: 0 0 7px 0;
    }

    .sub-title {
        color: var(--muted) !important;
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
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 18px 20px !important;
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

    /* ---------------------------------------------
       PLOTLY CHART TEXT VISIBILITY FIX
       --------------------------------------------- */

    .js-plotly-plot,
    .js-plotly-plot .plot-container,
    .js-plotly-plot .svg-container {
        opacity: 1 !important;
    }

    .js-plotly-plot .plotly text {
        fill: #334155 !important;
        opacity: 1 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .js-plotly-plot .plotly .gtitle {
        fill: #172554 !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }

    .js-plotly-plot .plotly .xtitle,
    .js-plotly-plot .plotly .ytitle {
        fill: #334155 !important;
        opacity: 1 !important;
    }

    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text,
    .js-plotly-plot .plotly .legend text {
        fill: #334155 !important;
        opacity: 1 !important;
    }

    .js-plotly-plot .modebar-btn path {
        fill: #64748b !important;
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

    div[data-baseweb="select"] > div,
    [data-testid="stDateInput"] input {
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
            padding: 13px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("📈 Sales Analysis")
st.sidebar.markdown("---")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

categories = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

segments = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df["Segment"].dropna().unique()),
    default=sorted(df["Segment"].dropna().unique())
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date) &
        (filtered_df["Order Date"].dt.date <= end_date)
    ]

if categories:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(categories)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if regions:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(regions)
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
    '<div class="main-title">Sales Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Detailed analysis of revenue, profit, orders and sales trends.</div>',
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning("No sales data found for the selected filters.")
    st.stop()

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales else 0
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Quantity Sold", f"{total_quantity:,}")
col5.metric("Profit Margin", f"{profit_margin:.2f}%")

st.markdown("---")

# --------------------------------------------------
# MONTHLY SALES TREND
# --------------------------------------------------

st.subheader("📅 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby("Month Year", as_index=False)["Sales"]
    .sum()
    .sort_values("Month Year")
)

fig_monthly = px.line(
    monthly_sales,
    x="Month Year",
    y="Sales",
    markers=True,
    title="Monthly Revenue Trend",
    labels={
        "Month Year": "Month",
        "Sales": "Revenue ($)"
    }
)

fig_monthly.update_layout(
    template="plotly_white",
    hovermode="x unified",
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        family="Inter, sans-serif",
        color="#334155",
        size=13
    ),
    title=dict(
        font=dict(size=17, color="#172554")
    ),
    margin=dict(l=20, r=20, t=55, b=20),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

fig_monthly.update_xaxes(
    showgrid=False,
    linecolor="#e2e8f0",
    tickfont=dict(color="#334155", size=12),
    title_font=dict(color="#334155")
)

fig_monthly.update_yaxes(
    gridcolor="#eef2f7",
    zerolinecolor="#e2e8f0",
    tickfont=dict(color="#334155", size=12),
    title_font=dict(color="#334155")
)

st.plotly_chart(fig_monthly, width="stretch")

# --------------------------------------------------
# MONTHLY PROFIT ANALYSIS
# --------------------------------------------------

st.subheader("💰 Monthly Profit Analysis")

monthly_profit = (
    filtered_df.groupby("Month Year", as_index=False)["Profit"]
    .sum()
    .sort_values("Month Year")
)

fig_profit = px.bar(
    monthly_profit,
    x="Month Year",
    y="Profit",
    title="Monthly Profit",
    labels={
        "Month Year": "Month",
        "Profit": "Profit ($)"
    }
)

fig_profit.update_layout(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        family="Inter, sans-serif",
        color="#334155",
        size=13
    ),
    title=dict(font=dict(size=17, color="#172554")),
    margin=dict(l=20, r=20, t=55, b=20)
)

fig_profit.update_xaxes(
    showgrid=False,
    linecolor="#e2e8f0",
    tickfont=dict(color="#334155", size=12),
    title_font=dict(color="#334155")
)

fig_profit.update_yaxes(
    gridcolor="#eef2f7",
    zerolinecolor="#e2e8f0",
    tickfont=dict(color="#334155", size=12),
    title_font=dict(color="#334155")
)

st.plotly_chart(fig_profit, width="stretch")

# --------------------------------------------------
# YEARLY SALES ANALYSIS
# --------------------------------------------------

st.subheader("📊 Yearly Sales Performance")

yearly_sales = (
    filtered_df.groupby("Year", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

yearly_sales["Year"] = yearly_sales["Year"].astype(str)

fig_yearly = px.bar(
    yearly_sales,
    x="Year",
    y=["Sales", "Profit"],
    barmode="group",
    title="Yearly Revenue vs Profit"
)

fig_yearly.update_layout(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        family="Inter, sans-serif",
        color="#334155",
        size=13
    ),
    title=dict(font=dict(size=17, color="#172554")),
    margin=dict(l=20, r=20, t=55, b=20),
    legend_title_text=""
)

fig_yearly.update_xaxes(
    showgrid=False,
    linecolor="#e2e8f0",
    tickfont=dict(color="#334155", size=12)
)

fig_yearly.update_yaxes(
    gridcolor="#eef2f7",
    zerolinecolor="#e2e8f0",
    tickfont=dict(color="#334155", size=12)
)

st.plotly_chart(fig_yearly, width="stretch")

# --------------------------------------------------
# CATEGORY SALES ANALYSIS
# --------------------------------------------------

st.subheader("🛍️ Category-wise Sales")

category_sales = (
    filtered_df.groupby("Category", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

col1, col2 = st.columns(2)

with col1:
    fig_category = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=0.45,
        title="Revenue Share by Category"
    )

    fig_category.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        font=dict(
            family="Inter, sans-serif",
            color="#334155",
            size=13
        ),
        title=dict(font=dict(size=17, color="#172554")),
        margin=dict(l=15, r=15, t=55, b=15),
        legend_title_text=""
    )

    st.plotly_chart(fig_category, width="stretch")

with col2:
    fig_category_profit = px.bar(
        category_sales,
        x="Category",
        y="Profit",
        title="Category-wise Profit",
        color="Category"
    )

    fig_category_profit.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Inter, sans-serif",
            color="#334155",
            size=13
        ),
        title=dict(font=dict(size=17, color="#172554")),
        margin=dict(l=15, r=15, t=55, b=15),
        showlegend=False
    )

    fig_category_profit.update_xaxes(
        showgrid=False,
        linecolor="#e2e8f0",
        tickfont=dict(color="#334155", size=12)
    )

    fig_category_profit.update_yaxes(
        gridcolor="#eef2f7",
        tickfont=dict(color="#334155", size=12)
    )

    st.plotly_chart(fig_category_profit, width="stretch")

# --------------------------------------------------
# REGION SALES ANALYSIS
# --------------------------------------------------

st.subheader("🌎 Region-wise Sales")

region_sales = (
    filtered_df.groupby("Region", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

col1, col2 = st.columns(2)

with col1:
    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Revenue by Region",
        color="Region"
    )

    fig_region.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Inter, sans-serif",
            color="#334155",
            size=13
        ),
        title=dict(font=dict(size=17, color="#172554")),
        margin=dict(l=15, r=15, t=55, b=15),
        showlegend=False
    )

    fig_region.update_xaxes(
        showgrid=False,
        linecolor="#e2e8f0",
        tickfont=dict(color="#334155", size=12)
    )

    fig_region.update_yaxes(
        gridcolor="#eef2f7",
        tickfont=dict(color="#334155", size=12)
    )

    st.plotly_chart(fig_region, width="stretch")

with col2:
    fig_region_profit = px.bar(
        region_sales,
        x="Region",
        y="Profit",
        title="Profit by Region",
        color="Region"
    )

    fig_region_profit.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Inter, sans-serif",
            color="#334155",
            size=13
        ),
        title=dict(font=dict(size=17, color="#172554")),
        margin=dict(l=15, r=15, t=55, b=15),
        showlegend=False
    )

    fig_region_profit.update_xaxes(
        showgrid=False,
        linecolor="#e2e8f0",
        tickfont=dict(color="#334155", size=12)
    )

    fig_region_profit.update_yaxes(
        gridcolor="#eef2f7",
        tickfont=dict(color="#334155", size=12)
    )

    st.plotly_chart(fig_region_profit, width="stretch")

# --------------------------------------------------
# SALES AND PROFIT TABLE
# --------------------------------------------------

st.subheader("📋 Sales Performance Summary")

summary = (
    filtered_df.groupby("Category", as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
)

summary["Profit_Margin"] = (
    summary["Total_Profit"] / summary["Total_Sales"] * 100
)

st.dataframe(
    summary.round(2),
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Sales Report",
    data=csv_data,
    file_name="sales_analysis_report.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption("Retail Sales Analytics & Business Intelligence System")