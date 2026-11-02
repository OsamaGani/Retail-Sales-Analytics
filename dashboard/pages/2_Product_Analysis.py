from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Product Analysis | Retail Analytics",
    page_icon="📦",
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

    numeric_columns = ["Sales", "Profit", "Quantity", "Discount"]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load sales data: {e}")
    st.stop()


# --------------------------------------------------
# COMMON PLOTLY CHART STYLING
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
                size=12,
                color="#334155"
            ),
            title_font=dict(
                color="#172554"
            )
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#eef2f7",
        linecolor="#cbd5e1",
        tickfont=dict(
            size=12,
            color="#334155"
        ),
        title_font=dict(
            size=13,
            color="#172554"
        ),
        automargin=True
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#eef2f7",
        linecolor="#cbd5e1",
        tickfont=dict(
            size=12,
            color="#334155"
        ),
        title_font=dict(
            size=13,
            color="#172554"
        ),
        automargin=True
    )

    return fig


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

    /* PLOTLY TEXT VISIBILITY FIX */

    .js-plotly-plot .plotly text {
        fill: #334155 !important;
        opacity: 1 !important;
        font-family: Arial, sans-serif !important;
    }

    .js-plotly-plot .plotly .gtitle {
        fill: #172554 !important;
        font-weight: 700 !important;
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
            padding: 13px !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("📦 Product Analysis")
st.sidebar.markdown("---")

categories = st.sidebar.multiselect(
    "Select Category",
    sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

subcategories = st.sidebar.multiselect(
    "Select Sub-Category",
    sorted(df["Sub-Category"].dropna().unique()),
    default=sorted(df["Sub-Category"].dropna().unique())
)


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if categories:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(categories)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if subcategories:
    filtered_df = filtered_df[
        filtered_df["Sub-Category"].isin(subcategories)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">Product Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Understand product performance, revenue contribution and profitability.</div>',
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning("No product data found for the selected filters.")
    st.stop()


# --------------------------------------------------
# PRODUCT KPIs
# --------------------------------------------------

total_products = filtered_df["Product Name"].nunique()
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Unique Products", f"{total_products:,}")
col2.metric("Total Revenue", f"${total_sales:,.2f}")
col3.metric("Total Profit", f"${total_profit:,.2f}")
col4.metric("Units Sold", f"{total_quantity:,.0f}")

st.markdown("---")


# --------------------------------------------------
# PRODUCT PERFORMANCE
# --------------------------------------------------

product_summary = (
    filtered_df.groupby("Product Name", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique")
    )
)


# --------------------------------------------------
# TOP 10 PRODUCTS BY SALES
# --------------------------------------------------

st.subheader("🏆 Top 10 Products by Revenue")

top_products = product_summary.nlargest(10, "Sales")

fig_top = px.bar(
    top_products.sort_values("Sales"),
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    title="Top 10 Revenue Generating Products",
    labels={
        "Sales": "Revenue ($)",
        "Product Name": "Product"
    }
)

fig_top = style_chart(fig_top)
fig_top.update_layout(yaxis_title="")

st.plotly_chart(fig_top, width="stretch")


# --------------------------------------------------
# TOP 10 PRODUCTS BY QUANTITY
# --------------------------------------------------

st.subheader("📊 Top 10 Products by Quantity Sold")

top_quantity = product_summary.nlargest(10, "Quantity")

fig_quantity = px.bar(
    top_quantity.sort_values("Quantity"),
    x="Quantity",
    y="Product Name",
    orientation="h",
    color="Quantity",
    title="Most Purchased Products"
)

fig_quantity = style_chart(fig_quantity)

st.plotly_chart(fig_quantity, width="stretch")


# --------------------------------------------------
# PROFIT ANALYSIS
# --------------------------------------------------

st.subheader("💰 Product Profitability Analysis")

top_profit = product_summary.nlargest(10, "Profit")

fig_profit = px.bar(
    top_profit.sort_values("Profit"),
    x="Profit",
    y="Product Name",
    orientation="h",
    color="Profit",
    title="Top 10 Most Profitable Products"
)

fig_profit = style_chart(fig_profit)

st.plotly_chart(fig_profit, width="stretch")


# --------------------------------------------------
# LOSS-MAKING PRODUCTS
# --------------------------------------------------

st.subheader("⚠️ Loss-Making Products")

loss_products = (
    product_summary[product_summary["Profit"] < 0]
    .sort_values("Profit")
    .head(10)
)

if not loss_products.empty:

    fig_loss = px.bar(
        loss_products.sort_values("Profit", ascending=False),
        x="Profit",
        y="Product Name",
        orientation="h",
        color="Profit",
        title="Top 10 Products with Highest Loss"
    )

    fig_loss = style_chart(fig_loss)

    st.plotly_chart(fig_loss, width="stretch")

    st.dataframe(
        loss_products.round(2),
        width="stretch",
        hide_index=True
    )

else:
    st.success("No loss-making products found.")


# --------------------------------------------------
# CATEGORY PERFORMANCE
# --------------------------------------------------

st.subheader("🛍️ Category-wise Product Performance")

category_summary = (
    filtered_df.groupby("Category", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
)

col1, col2 = st.columns(2)

with col1:

    fig_category_sales = px.pie(
        category_summary,
        names="Category",
        values="Sales",
        hole=0.45,
        title="Revenue by Category"
    )

    fig_category_sales = style_chart(fig_category_sales)

    st.plotly_chart(fig_category_sales, width="stretch")


with col2:

    fig_category_profit = px.bar(
        category_summary,
        x="Category",
        y="Profit",
        color="Category",
        title="Profit by Category"
    )

    fig_category_profit = style_chart(fig_category_profit)
    fig_category_profit.update_layout(showlegend=False)

    st.plotly_chart(fig_category_profit, width="stretch")


# --------------------------------------------------
# SUB-CATEGORY PERFORMANCE
# --------------------------------------------------

st.subheader("📌 Sub-Category Performance")

subcategory_summary = (
    filtered_df.groupby("Sub-Category", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values("Sales", ascending=False)
)

fig_subcategory = px.bar(
    subcategory_summary,
    x="Sub-Category",
    y="Sales",
    color="Profit",
    title="Sub-Category Revenue and Profit"
)

fig_subcategory = style_chart(fig_subcategory)

st.plotly_chart(fig_subcategory, width="stretch")


# --------------------------------------------------
# COMPLETE PRODUCT TABLE
# --------------------------------------------------

st.subheader("📋 Complete Product Performance")

product_summary = product_summary.sort_values(
    "Sales",
    ascending=False
)

st.dataframe(
    product_summary.round(2),
    width="stretch",
    hide_index=True
)


# --------------------------------------------------
# DOWNLOAD PRODUCT REPORT
# --------------------------------------------------

csv_data = product_summary.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Product Report",
    data=csv_data,
    file_name="product_analysis_report.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption("Retail Sales Analytics & Business Intelligence System")