
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Advanced Analytics | Retail Analytics",
    page_icon="🚀",
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

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    for col in ["Sales", "Profit", "Quantity", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(
        subset=["Order Date", "Sales", "Profit"]
    )

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load data: {e}")
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

    h1, h2, h3 {
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

    [data-testid="stMetric"] * {
        color: var(--navy) !important;
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
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🚀 Advanced Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Advanced business intelligence, growth metrics, '
    'customer value and sales forecasting.'
    '</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("🚀 Advanced Analytics")
st.sidebar.markdown("---")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = df[
        (df["Order Date"].dt.date >= start_date) &
        (df["Order Date"].dt.date <= end_date)
    ].copy()

else:
    filtered_df = df.copy()

if filtered_df.empty:
    st.warning("No data available for selected dates.")
    st.stop()

# --------------------------------------------------
# BASIC METRICS
# --------------------------------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales else 0
)

total_orders = filtered_df["Order ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${total_sales:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)

col4.metric(
    "Total Orders",
    f"{total_orders:,}"
)

st.markdown("---")

# ==================================================
# 1. YEAR OVER YEAR GROWTH
# ==================================================

st.subheader("📈 1. Year-over-Year (YoY) Growth")

yearly = (
    filtered_df.groupby(
        filtered_df["Order Date"].dt.year
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_index()
)

yearly.index.name = "Year"

yearly["YoY Growth (%)"] = (
    yearly["Sales"].pct_change() * 100
)

yearly["Profit Growth (%)"] = (
    yearly["Profit"].pct_change() * 100
)

if len(yearly) >= 2:

    latest_yoy = yearly["YoY Growth (%)"].iloc[-1]

    col1, col2 = st.columns(2)

    col1.metric(
        "Latest YoY Revenue Growth",
        f"{latest_yoy:.2f}%",
        delta=f"{latest_yoy:.2f}%"
    )

    col2.metric(
        "Latest Year Revenue",
        f"${yearly['Sales'].iloc[-1]:,.2f}"
    )

else:
    st.info(
        "At least two years of data are required "
        "to calculate YoY growth."
    )

fig_yoy = px.bar(
    yearly.reset_index(),
    x="Year",
    y="Sales",
    title="Yearly Revenue Growth",
    color="Sales",
    labels={
        "Sales": "Revenue ($)",
        "Year": "Year"
    }
)

fig_yoy.update_layout(
    template="plotly_white",
    title_font_color="#172554",
    font_color="#334155"
)

st.plotly_chart(
    fig_yoy,
    width="stretch"
)

st.dataframe(
    yearly.round(2),
    width="stretch"
)

# ==================================================
# 2. MONTH OVER MONTH GROWTH
# ==================================================

st.markdown("---")

st.subheader("📅 2. Month-over-Month (MoM) Growth")

monthly = (
    filtered_df.set_index("Order Date")
    .resample("MS")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

monthly["MoM Growth (%)"] = (
    monthly["Sales"].pct_change() * 100
)

monthly["Profit Growth (%)"] = (
    monthly["Profit"].pct_change() * 100
)

monthly = monthly.reset_index()

if len(monthly) >= 2:

    latest_mom = monthly["MoM Growth (%)"].iloc[-1]

    st.metric(
        "Latest MoM Revenue Growth",
        f"{latest_mom:.2f}%",
        delta=f"{latest_mom:.2f}%"
    )

else:
    st.info(
        "At least two months of data are required "
        "for MoM growth."
    )

fig_mom = px.line(
    monthly,
    x="Order Date",
    y="MoM Growth (%)",
    markers=True,
    title="Monthly Revenue Growth Percentage"
)

fig_mom.add_hline(
    y=0,
    line_dash="dash"
)

fig_mom.update_layout(
    template="plotly_white",
    title_font_color="#172554",
    font_color="#334155"
)

st.plotly_chart(
    fig_mom,
    width="stretch"
)

st.dataframe(
    monthly.round(2),
    width="stretch",
    hide_index=True
)

# ==================================================
# 3. PROFIT MARGIN ANALYSIS
# ==================================================

st.markdown("---")

st.subheader("💰 3. Profit Margin Analysis")

category_margin = (
    filtered_df.groupby("Category", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

category_margin["Profit Margin (%)"] = np.where(
    category_margin["Sales"] != 0,
    category_margin["Profit"] /
    category_margin["Sales"] * 100,
    0
)

region_margin = (
    filtered_df.groupby("Region", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

region_margin["Profit Margin (%)"] = np.where(
    region_margin["Sales"] != 0,
    region_margin["Profit"] /
    region_margin["Sales"] * 100,
    0
)

col1, col2 = st.columns(2)

with col1:

    fig_category_margin = px.bar(
        category_margin,
        x="Category",
        y="Profit Margin (%)",
        color="Profit Margin (%)",
        title="Profit Margin by Category"
    )

    fig_category_margin.update_layout(
        template="plotly_white",
        font_color="#334155"
    )

    st.plotly_chart(
        fig_category_margin,
        width="stretch"
    )

with col2:

    fig_region_margin = px.bar(
        region_margin,
        x="Region",
        y="Profit Margin (%)",
        color="Profit Margin (%)",
        title="Profit Margin by Region"
    )

    fig_region_margin.update_layout(
        template="plotly_white",
        font_color="#334155"
    )

    st.plotly_chart(
        fig_region_margin,
        width="stretch"
    )

st.subheader("Category Profit Margin Details")

st.dataframe(
    category_margin.round(2),
    width="stretch",
    hide_index=True
)

st.subheader("Regional Profit Margin Details")

st.dataframe(
    region_margin.round(2),
    width="stretch",
    hide_index=True
)

# ==================================================
# 4. RFM CUSTOMER SEGMENTATION
# ==================================================

st.markdown("---")

st.subheader("👥 4. RFM Customer Segmentation")

st.caption(
    "RFM means Recency, Frequency and Monetary value. "
    "It segments customers based on their purchasing behavior."
)

reference_date = (
    filtered_df["Order Date"].max() +
    pd.Timedelta(days=1)
)

rfm = (
    filtered_df.groupby(
        ["Customer ID", "Customer Name"],
        as_index=False
    )
    .agg(
        Recency=(
            "Order Date",
            lambda x: (reference_date - x.max()).days
        ),
        Frequency=("Order ID", "nunique"),
        Monetary=("Sales", "sum")
    )
)

if len(rfm) >= 5:

    rfm["R_Score"] = pd.qcut(
        rfm["Recency"].rank(method="first"),
        5,
        labels=[5, 4, 3, 2, 1]
    ).astype(int)

    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)

    rfm["M_Score"] = pd.qcut(
        rfm["Monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)

    rfm["RFM Score"] = (
        rfm["R_Score"].astype(str) +
        rfm["F_Score"].astype(str) +
        rfm["M_Score"].astype(str)
    )

    rfm["Segment"] = np.select(
        [
            (rfm["R_Score"] >= 4) &
            (rfm["F_Score"] >= 4),

            (rfm["R_Score"] >= 3) &
            (rfm["M_Score"] >= 4),

            (rfm["R_Score"] <= 2) &
            (rfm["F_Score"] >= 3),

            (rfm["R_Score"] <= 2) &
            (rfm["F_Score"] <= 2)
        ],
        [
            "Loyal Customers",
            "High Value Customers",
            "At Risk Customers",
            "Lost / Inactive Customers"
        ],
        default="Regular Customers"
    )

    segment_summary = (
        rfm.groupby("Segment", as_index=False)
        .agg(
            Customers=("Customer ID", "count"),
            Revenue=("Monetary", "sum"),
            Average_Recency=("Recency", "mean")
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_rfm = px.pie(
            segment_summary,
            names="Segment",
            values="Customers",
            hole=0.45,
            title="Customer Distribution by Segment"
        )

        fig_rfm.update_layout(
            template="plotly_white",
            font_color="#334155"
        )

        st.plotly_chart(
            fig_rfm,
            width="stretch"
        )

    with col2:

        fig_rfm_revenue = px.bar(
            segment_summary,
            x="Segment",
            y="Revenue",
            color="Segment",
            title="Revenue by Customer Segment"
        )

        fig_rfm_revenue.update_layout(
            template="plotly_white",
            font_color="#334155"
        )

        st.plotly_chart(
            fig_rfm_revenue,
            width="stretch"
        )

    st.subheader("Customer RFM Details")

    st.dataframe(
        rfm.sort_values(
            "Monetary",
            ascending=False
        ).round(2),
        width="stretch",
        hide_index=True
    )

    st.download_button(
        label="⬇️ Download RFM Customer Report",
        data=rfm.to_csv(index=False).encode("utf-8"),
        file_name="rfm_customer_analysis.csv",
        mime="text/csv"
    )

else:

    st.info(
        "At least five customers are required "
        "for RFM segmentation."
    )

# ==================================================
# 5. SALES FORECASTING
# ==================================================

st.markdown("---")

st.subheader("🔮 5. Sales Forecasting")

st.caption(
    "A simple linear trend forecast based on historical "
    "monthly revenue. This is an exploratory estimate, "
    "not a guaranteed prediction."
)

forecast_data = (
    filtered_df.set_index("Order Date")
    .resample("MS")["Sales"]
    .sum()
    .reset_index()
)

forecast_data = forecast_data[
    forecast_data["Sales"] > 0
].copy()

if len(forecast_data) >= 3:

    forecast_data["Month_Index"] = np.arange(
        len(forecast_data)
    )

    x = forecast_data["Month_Index"].to_numpy()
    y = forecast_data["Sales"].to_numpy()

    slope, intercept = np.polyfit(
        x,
        y,
        1
    )

    forecast_months = 3

    future_x = np.arange(
        len(forecast_data),
        len(forecast_data) + forecast_months
    )

    future_sales = (
        slope * future_x + intercept
    )

    future_sales = np.maximum(
        future_sales,
        0
    )

    future_dates = pd.date_range(
        start=(
            forecast_data["Order Date"].max() +
            pd.offsets.MonthBegin(1)
        ),
        periods=forecast_months,
        freq="MS"
    )

    forecast_df = pd.DataFrame({
        "Order Date": future_dates,
        "Sales": future_sales,
        "Type": "Forecast"
    })

    historical_df = forecast_data[
        ["Order Date", "Sales"]
    ].copy()

    historical_df["Type"] = "Historical"

    combined = pd.concat(
        [historical_df, forecast_df],
        ignore_index=True
    )

    fig_forecast = px.line(
        combined,
        x="Order Date",
        y="Sales",
        color="Type",
        markers=True,
        title="Historical Sales and Next 3 Months Forecast"
    )

    fig_forecast.update_layout(
        template="plotly_white",
        font_color="#334155"
    )

    st.plotly_chart(
        fig_forecast,
        width="stretch"
    )

    st.subheader("Next 3 Months Sales Forecast")

    st.dataframe(
        forecast_df.round(2),
        width="stretch",
        hide_index=True
    )

    st.download_button(
        label="⬇️ Download Sales Forecast",
        data=forecast_df.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="sales_forecast.csv",
        mime="text/csv"
    )

else:

    st.info(
        "At least three months of sales data "
        "are required for forecasting."
    )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Retail Sales Analytics & Business Intelligence System | Advanced Analytics"
)
