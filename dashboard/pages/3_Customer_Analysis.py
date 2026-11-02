
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Analysis | Retail Analytics",
    page_icon="👥",
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

    /* Improve Plotly SVG text readability */
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

st.sidebar.title("👥 Customer Analysis")
st.sidebar.markdown("---")

segments = st.sidebar.multiselect(
    "Customer Segment",
    sorted(df["Segment"].dropna().unique()),
    default=sorted(df["Segment"].dropna().unique())
)

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if segments:
    filtered_df = filtered_df[
        filtered_df["Segment"].isin(segments)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if regions:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(regions)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">Customer Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Analyze customer value, purchasing behavior and segment performance.</div>',
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning("No customer data found for the selected filters.")
    st.stop()

# --------------------------------------------------
# CUSTOMER SUMMARY
# --------------------------------------------------

customer_summary = (
    filtered_df.groupby(
        ["Customer ID", "Customer Name", "Segment"],
        as_index=False
    )
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order ID", "nunique"),
        Total_Quantity=("Quantity", "sum"),
        First_Order=("Order Date", "min"),
        Last_Order=("Order Date", "max")
    )
)

# --------------------------------------------------
# CUSTOMER KPIs
# --------------------------------------------------

total_customers = customer_summary["Customer ID"].nunique()
total_revenue = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
avg_customer_sales = (
    customer_summary["Total_Sales"].mean()
    if total_customers else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Total Profit", f"${total_profit:,.2f}")
col4.metric("Avg. Customer Revenue", f"${avg_customer_sales:,.2f}")

st.markdown("---")

# --------------------------------------------------
# TOP 10 CUSTOMERS
# --------------------------------------------------

st.subheader("🏆 Top 10 Customers by Revenue")

top_customers = customer_summary.nlargest(10, "Total_Sales")

fig_top_customers = px.bar(
    top_customers.sort_values("Total_Sales"),
    x="Total_Sales",
    y="Customer Name",
    orientation="h",
    color="Total_Sales",
    title="Top 10 Revenue Generating Customers",
    labels={
        "Total_Sales": "Revenue ($)",
        "Customer Name": "Customer"
    }
)

fig_top_customers = style_chart(fig_top_customers)

fig_top_customers.update_layout(
    coloraxis_colorbar=dict(
        title="Revenue",
        tickfont=dict(size=12, color="#334155")
    )
)

fig_top_customers.update_xaxes(showgrid=True)
fig_top_customers.update_yaxes(showgrid=False)

st.plotly_chart(fig_top_customers, width="stretch")

# --------------------------------------------------
# CUSTOMER SEGMENT ANALYSIS
# --------------------------------------------------

st.subheader("📊 Customer Segment Analysis")

segment_summary = (
    filtered_df.groupby("Segment", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
)

col1, col2 = st.columns(2)

with col1:
    fig_segment_sales = px.pie(
        segment_summary,
        names="Segment",
        values="Sales",
        hole=0.45,
        title="Revenue Share by Segment"
    )

    fig_segment_sales = style_chart(fig_segment_sales)

    fig_segment_sales.update_layout(
        legend_title_text=""
    )

    fig_segment_sales.update_traces(
        textfont=dict(
            family="Arial, sans-serif",
            size=13
        )
    )

    st.plotly_chart(fig_segment_sales, width="stretch")

with col2:
    fig_segment_profit = px.bar(
        segment_summary,
        x="Segment",
        y="Profit",
        color="Segment",
        title="Profit by Customer Segment"
    )

    fig_segment_profit = style_chart(fig_segment_profit)

    fig_segment_profit.update_layout(
        showlegend=False
    )

    fig_segment_profit.update_xaxes(showgrid=False)
    fig_segment_profit.update_yaxes(showgrid=True)

    st.plotly_chart(fig_segment_profit, width="stretch")

# --------------------------------------------------
# CUSTOMER ORDER ANALYSIS
# --------------------------------------------------

st.subheader("🛒 Customer Order Analysis")

col1, col2 = st.columns(2)

with col1:
    fig_orders = px.histogram(
        customer_summary,
        x="Total_Orders",
        nbins=20,
        title="Distribution of Orders per Customer",
        labels={
            "Total_Orders": "Number of Orders"
        }
    )

    fig_orders = style_chart(fig_orders)

    fig_orders.update_xaxes(showgrid=False)
    fig_orders.update_yaxes(showgrid=True)

    st.plotly_chart(fig_orders, width="stretch")

with col2:
    fig_customer_value = px.scatter(
        customer_summary,
        x="Total_Orders",
        y="Total_Sales",
        size="Total_Quantity",
        color="Segment",
        hover_name="Customer Name",
        title="Customer Revenue vs Order Frequency",
        labels={
            "Total_Orders": "Number of Orders",
            "Total_Sales": "Revenue ($)"
        }
    )

    fig_customer_value = style_chart(fig_customer_value)

    fig_customer_value.update_xaxes(showgrid=True)
    fig_customer_value.update_yaxes(showgrid=True)

    st.plotly_chart(fig_customer_value, width="stretch")

# --------------------------------------------------
# CUSTOMER PROFITABILITY
# --------------------------------------------------

st.subheader("💰 Customer Profitability")

top_profit_customers = customer_summary.nlargest(
    10, "Total_Profit"
)

fig_profit = px.bar(
    top_profit_customers.sort_values("Total_Profit"),
    x="Total_Profit",
    y="Customer Name",
    orientation="h",
    color="Total_Profit",
    title="Top 10 Most Profitable Customers"
)

fig_profit = style_chart(fig_profit)

fig_profit.update_xaxes(showgrid=True)
fig_profit.update_yaxes(showgrid=False)

st.plotly_chart(fig_profit, width="stretch")

# --------------------------------------------------
# CUSTOMER TABLE
# --------------------------------------------------

st.subheader("📋 Customer Performance Details")

display_df = customer_summary.sort_values(
    "Total_Sales",
    ascending=False
)

st.dataframe(
    display_df.round(2),
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

csv_data = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Customer Report",
    data=csv_data,
    file_name="customer_analysis_report.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption("Retail Sales Analytics & Business Intelligence System")
