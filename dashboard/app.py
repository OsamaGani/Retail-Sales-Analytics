
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ENTERPRISE LIGHT THEME CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --page-bg: #F4F7FB;
    --surface: #FFFFFF;
    --navy: #172B4D;
    --muted: #718096;
    --border: #E5EAF1;
    --accent: #2563EB;
    --accent-soft: #EFF6FF;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--page-bg);
    color: var(--navy);
}

header[data-testid="stHeader"] {
    background: var(--page-bg);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.8rem;
    padding-bottom: 2.5rem;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    background: var(--surface);
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] .stMarkdown {
    color: #334155 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--navy) !important;
    letter-spacing: -0.4px;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}

/* MULTIPAGE NAVIGATION */

[data-testid="stSidebarNav"] {
    padding-top: 0.5rem;
}

[data-testid="stSidebarNav"] a {
    border-radius: 9px;
    margin: 3px 8px;
    padding: 9px 12px;
    transition: background 0.2s ease, color 0.2s ease;
}

[data-testid="stSidebarNav"] a p {
    font-weight: 600;
    color: #475569 !important;
    font-size: 13px;
}

[data-testid="stSidebarNav"] a:hover {
    background: var(--accent-soft);
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: #EAF1FF;
    border-left: 3px solid var(--accent);
}

[data-testid="stSidebarNav"] a[aria-current="page"] p {
    color: #1D4ED8 !important;
    font-weight: 700;
}

/* SIDEBAR INPUTS */

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"] {
    color: var(--navy) !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: #EAF1FF;
}

/* DASHBOARD HEADER */

.dashboard-header {
    background: linear-gradient(115deg, #FFFFFF 0%, #F8FAFF 100%);
    padding: 27px 30px;
    border-radius: 16px;
    border: 1px solid var(--border);
    border-top: 4px solid var(--accent);
    margin-bottom: 22px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.035);
}

.dashboard-title {
    color: var(--navy);
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.8px;
    margin: 0;
}

.dashboard-subtitle {
    color: var(--muted);
    font-size: 13px;
    margin-top: 8px;
    line-height: 1.6;
}

/* SECTION HEADINGS */

.section-title {
    color: var(--navy);
    font-size: 19px;
    font-weight: 750;
    letter-spacing: -0.3px;
    margin-top: 24px;
    margin-bottom: 14px;
}

/* CUSTOM KPI CARDS */

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 21px 19px;
    min-height: 136px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.035);
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.07);
}

.metric-label {
    color: var(--muted);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.8px;
}

.metric-value {
    color: var(--navy);
    font-size: clamp(17px, 1.7vw, 25px);
    font-weight: 800;
    margin-top: 14px;
    white-space: nowrap;
    line-height: 1.3;
}

.metric-description {
    color: #8492A6;
    font-size: 11px;
    margin-top: 8px;
}

/* STREAMLIT METRIC WIDGETS */

[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 16px 17px;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.025);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: var(--muted) !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: var(--navy) !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    font-weight: 600;
}

/* CHARTS */

div[data-testid="stPlotlyChart"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 8px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.025);
}

/* TABLES */

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 11px;
    overflow: hidden;
}

/* FORM CONTROLS */

[data-baseweb="select"] > div,
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div {
    border-radius: 8px;
    border-color: var(--border);
}

/* BUTTONS */

.stButton button,
.stDownloadButton button {
    border-radius: 9px;
    font-weight: 650;
    min-height: 40px;
    transition: all 0.2s ease;
}

.stDownloadButton button {
    background: var(--accent);
    color: #FFFFFF;
    border: 1px solid var(--accent);
}

.stDownloadButton button:hover {
    background: #1D4ED8;
    color: #FFFFFF;
    border-color: #1D4ED8;
}

/* DIVIDERS */

hr {
    border-color: var(--border);
}

/* CAPTIONS AND FOOTER */

.stCaption,
[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

.dashboard-footer {
    text-align: center;
    color: #8492A6;
    font-size: 12px;
    line-height: 1.8;
    padding: 22px 12px;
}

/* RESPONSIVE */

@media (max-width: 768px) {
    .dashboard-title {
        font-size: 23px;
    }

    .dashboard-header {
        padding: 19px;
    }

    .metric-card {
        padding: 15px;
        min-height: 120px;
    }

    .metric-value {
        font-size: 17px;
    }

    .section-title {
        font-size: 17px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. DATA LOADING
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "cleaned_sales.csv"


@st.cache_data
def load_data():

    df = pd.read_csv(
        DATA_PATH,
        encoding="utf-8"
    )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        errors="coerce"
    )

    numeric_columns = [
        "Sales",
        "Profit",
        "Quantity",
        "Discount"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.dropna(
        subset=["Order Date", "Sales", "Profit"]
    )

    return df


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "Cleaned dataset not found. "
        "Please run data_cleaning.py first."
    )

    st.stop()

except Exception as error:

    st.error(f"Dataset loading error: {error}")

    st.stop()


# ==========================================
# 4. SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 📊 Retail BI")

    st.caption("BUSINESS INTELLIGENCE PLATFORM")

    st.divider()

    st.markdown("### Dashboard Filters")

    min_date = df["Order Date"].min().date()

    max_date = df["Order Date"].max().date()

    date_range = st.date_input(
        "Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    category_options = sorted(
        df["Category"].dropna().unique().tolist()
    )

    selected_categories = st.multiselect(
        "Product Category",
        options=category_options,
        default=category_options
    )

    region_options = sorted(
        df["Region"].dropna().unique().tolist()
    )

    selected_regions = st.multiselect(
        "Region",
        options=region_options,
        default=region_options
    )

    segment_options = sorted(
        df["Segment"].dropna().unique().tolist()
    )

    selected_segments = st.multiselect(
        "Customer Segment",
        options=segment_options,
        default=segment_options
    )

    ship_options = sorted(
        df["Ship Mode"].dropna().unique().tolist()
    )

    selected_ship_modes = st.multiselect(
        "Shipping Mode",
        options=ship_options,
        default=ship_options
    )

    st.divider()

    st.caption("Retail Sales Analytics v1.0")

    st.caption("Powered by Python, Pandas & Plotly")


# ==========================================
# 5. DATE VALIDATION
# ==========================================

if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:

    st.warning("Please select both start and end dates.")

    st.stop()

start_date, end_date = date_range

if start_date > end_date:

    st.error("Start date cannot be after end date.")

    st.stop()


# ==========================================
# 6. FILTER DATA
# ==========================================

filtered_df = df[
    (df["Order Date"].dt.date >= start_date)
    &
    (df["Order Date"].dt.date <= end_date)
    &
    (df["Category"].isin(selected_categories))
    &
    (df["Region"].isin(selected_regions))
    &
    (df["Segment"].isin(selected_segments))
    &
    (df["Ship Mode"].isin(selected_ship_modes))
].copy()


# ==========================================
# 7. DASHBOARD HEADER
# ==========================================

st.markdown(
    '<div class="dashboard-header">'
    '<div class="dashboard-title">'
    'Retail Sales Analytics'
    '</div>'
    '<div class="dashboard-subtitle">'
    'Business Intelligence Dashboard | '
    'Sales Performance & Business Insights'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    f"Reporting Period: {start_date} to {end_date}"
)

st.divider()


# ==========================================
# 8. EMPTY DATA VALIDATION
# ==========================================

if filtered_df.empty:

    st.warning(
        "No records found for the selected filters. "
        "Please change your filters."
    )

    st.stop()


# ==========================================
# 9. KPI CALCULATIONS
# ==========================================

total_revenue = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_customers = filtered_df["Customer ID"].nunique()

total_quantity = filtered_df["Quantity"].sum()

profit_margin = (
    (total_profit / total_revenue) * 100
    if total_revenue != 0 else 0
)

average_order_value = (
    total_revenue / total_orders
    if total_orders != 0 else 0
)


# ==========================================
# 10. BUSINESS OVERVIEW
# ==========================================

st.markdown(
    '<div class="section-title">Business Overview</div>',
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL REVENUE</div>
            <div class="metric-value">${total_revenue:,.2f}</div>
            <div class="metric-description">
                Total sales generated
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL PROFIT</div>
            <div class="metric-value">${total_profit:,.2f}</div>
            <div class="metric-description">
                Total recorded profit
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL ORDERS</div>
            <div class="metric-value">{total_orders:,}</div>
            <div class="metric-description">
                Unique order IDs
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL CUSTOMERS</div>
            <div class="metric-value">{total_customers:,}</div>
            <div class="metric-description">
                Unique customers
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# 11. SECONDARY METRICS
# ==========================================

st.write("")

m1, m2, m3 = st.columns(3)

m1.metric(
    "Total Quantity Sold",
    f"{total_quantity:,}"
)

m2.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)

m3.metric(
    "Average Order Value",
    f"${average_order_value:,.2f}"
)


# ==========================================
# 12. MONTHLY SALES TREND
# ==========================================

st.markdown(
    '<div class="section-title">Sales Performance Trend</div>',
    unsafe_allow_html=True
)

monthly_data = (
    filtered_df
    .groupby(
        filtered_df["Order Date"].dt.to_period("M")
    )
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

monthly_data["Month"] = (
    monthly_data["Order Date"].astype(str)
)

fig_monthly = go.Figure()

fig_monthly.add_trace(
    go.Scatter(
        x=monthly_data["Month"],
        y=monthly_data["Revenue"],
        mode="lines+markers",
        name="Revenue",
        line=dict(width=3),
        marker=dict(size=7)
    )
)

fig_monthly.add_trace(
    go.Scatter(
        x=monthly_data["Month"],
        y=monthly_data["Profit"],
        mode="lines+markers",
        name="Profit",
        line=dict(width=2, dash="dot")
    )
)

fig_monthly.update_layout(
    title="Monthly Revenue & Profit",
    xaxis_title="Month",
    yaxis_title="Amount ($)",
    template="plotly_white",
    height=420,
    hovermode="x unified",
    legend=dict(
        orientation="h",
        y=1.12
    )
)

st.plotly_chart(
    fig_monthly,
    width="stretch"
)




# ==========================================
# 13. CATEGORY AND REGION ANALYSIS
# ==========================================

st.markdown(
    '<div class="section-title">'
    'Category & Regional Analysis'
    '</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

category_data = (
    filtered_df.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

region_data = (
    filtered_df.groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

with col1:

    fig_category = px.bar(
        category_data,
        x="Category",
        y="Sales",
        color="Category",
        title="Category-wise Revenue",
        text_auto=".3s",
        template="plotly_white"
    )

    fig_category.update_layout(
        height=400,
        showlegend=False
    )

    st.plotly_chart(
        fig_category,
        width="stretch"
    )


with col2:

    fig_region = px.bar(
        region_data,
        x="Region",
        y="Sales",
        color="Region",
        title="Region-wise Revenue",
        text_auto=".3s",
        template="plotly_white"
    )

    fig_region.update_layout(
        height=400,
        showlegend=False
    )

    st.plotly_chart(
        fig_region,
        width="stretch"
    )


# ==========================================
# 14. PROFITABILITY ANALYSIS
# ==========================================

st.markdown(
    '<div class="section-title">'
    'Profitability Analysis'
    '</div>',
    unsafe_allow_html=True
)

profit_col1, profit_col2 = st.columns(2)

with profit_col1:

    fig_profit = px.bar(
        category_data,
        x="Category",
        y="Profit",
        color="Profit",
        title="Category-wise Profit",
        text_auto=".3s",
        template="plotly_white"
    )

    fig_profit.update_layout(
        height=400
    )

    st.plotly_chart(
        fig_profit,
        width="stretch"
    )


with profit_col2:

    fig_scatter = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Category",
        size="Quantity",
        hover_data=[
            "Product Name",
            "Region"
        ],
        title="Sales vs Profit",
        template="plotly_white"
    )

    fig_scatter.update_layout(
        height=400
    )

    st.plotly_chart(
        fig_scatter,
        width="stretch"
    )


# ==========================================
# 15. PRODUCT PERFORMANCE
# ==========================================

st.markdown(
    '<div class="section-title">'
    'Product Performance'
    '</div>',
    unsafe_allow_html=True
)

product_data = (
    filtered_df.groupby("Product Name")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

top_products = (
    product_data
    .nlargest(10, "Revenue")
    .sort_values("Revenue")
)

fig_products = px.bar(
    top_products,
    x="Revenue",
    y="Product Name",
    orientation="h",
    color="Revenue",
    title="Top 10 Products by Revenue",
    text_auto=".3s",
    template="plotly_white"
)

fig_products.update_layout(
    height=550
)

st.plotly_chart(
    fig_products,
    width="stretch"
)


# ==========================================
# 16. CUSTOMER PERFORMANCE
# ==========================================

st.markdown(
    '<div class="section-title">'
    'Customer Performance'
    '</div>',
    unsafe_allow_html=True
)

customer_data = (
    filtered_df.groupby(
        ["Customer ID", "Customer Name"]
    )
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Orders=("Order ID", "nunique"),
        Total_Profit=("Profit", "sum")
    )
    .reset_index()
    .sort_values(
        "Total_Sales",
        ascending=False
    )
)

st.dataframe(
    customer_data.head(10),
    width="stretch",
    hide_index=True
)


# ==========================================
# 17. LOSS MAKING PRODUCTS
# ==========================================

st.markdown(
    '<div class="section-title">'
    'Loss-Making Products'
    '</div>',
    unsafe_allow_html=True
)

loss_products = (
    product_data[
        product_data["Profit"] < 0
    ]
    .sort_values("Profit")
    .head(10)
)

if not loss_products.empty:

    st.dataframe(
        loss_products,
        width="stretch",
        hide_index=True
    )

else:

    st.success(
        "No loss-making products in the selected filters."
    )


# ==========================================
# 18. DETAILED SALES RECORDS
# ==========================================

st.markdown(
    '<div class="section-title">'
    'Detailed Sales Records'
    '</div>',
    unsafe_allow_html=True
)

with st.expander("View filtered sales data"):

    st.caption(
        f"Showing {len(filtered_df):,} records"
    )

    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True
    )


# ==========================================
# 19. EXPORT FILTERED DATA
# ==========================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Sales Data",
    data=csv_data,
    file_name="retail_sales_report.csv",
    mime="text/csv",
    width="stretch"
)


# ==========================================
# 20. FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div class="dashboard-footer">
        <strong>Retail Sales Analytics</strong>
        <br>
        Business Intelligence Dashboard
        <br><br>
        Built with Python | NumPy | Pandas |
        Streamlit | Plotly
        <br>
        Version 1.0
    </div>
    """,
    unsafe_allow_html=True
)
