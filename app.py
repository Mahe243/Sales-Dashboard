"""
Sales Dashboard - Streamlit + Plotly
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------
# STYLING
# -----------------------------------------------------------------------
st.markdown(
    """
    <style>
        .kpi-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            text-align: center;
        }
        .kpi-label {
            font-size: 14px;
            color: #6b7280;
            font-weight: 500;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            color: #111827;
        }
        div.block-container {
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Date"])
    df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
    df["Year"] = df["Date"].dt.year
    return df


DATA_PATH = "data/sales_data.csv"

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"Could not find `{DATA_PATH}`. Run `python generate_data.py` first "
        "to create the sample dataset, or place your own CSV at that path "
        "with columns: Date, Region, Category, Product, Quantity, Sales, Profit."
    )
    st.stop()

# -----------------------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------------------
st.sidebar.title("🔍 Filters")

min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

regions = st.sidebar.multiselect(
    "Region", options=sorted(df["Region"].unique()), default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Category", options=sorted(df["Category"].unique()), default=sorted(df["Category"].unique())
)

products = st.sidebar.multiselect(
    "Product (optional)", options=sorted(df["Product"].unique()), default=[]
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit + Plotly")

# -----------------------------------------------------------------------
# APPLY FILTERS
# -----------------------------------------------------------------------
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
else:
    start, end = min_date, max_date

mask = (
    (df["Date"] >= pd.to_datetime(start))
    & (df["Date"] <= pd.to_datetime(end))
    & (df["Region"].isin(regions))
    & (df["Category"].isin(categories))
)

if products:
    mask &= df["Product"].isin(products)

filtered = df[mask]

if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your selection.")
    st.stop()

# -----------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------
st.title("📊 Sales Performance Dashboard")
st.caption(f"Showing data from **{start}** to **{end}** · {len(filtered):,} records")

# -----------------------------------------------------------------------
# KPIs
# -----------------------------------------------------------------------
total_revenue = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_orders = len(filtered)
avg_order_value = total_revenue / total_orders if total_orders else 0
profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0

k1, k2, k3, k4, k5 = st.columns(5)

kpis = [
    (k1, "💰 Total Revenue", f"${total_revenue:,.0f}"),
    (k2, "📈 Total Profit", f"${total_profit:,.0f}"),
    (k3, "🧾 Total Orders", f"{total_orders:,}"),
    (k4, "🛒 Avg Order Value", f"${avg_order_value:,.2f}"),
    (k5, "📊 Profit Margin", f"{profit_margin:.1f}%"),
]

for col, label, value in kpis:
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# -----------------------------------------------------------------------
# ROW 1: Sales by Region | Sales by Category
# -----------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Sales by Region")
    region_data = filtered.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_region = px.bar(
        region_data,
        x="Region",
        y="Sales",
        color="Region",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_region.update_layout(showlegend=False, yaxis_title="Sales ($)", xaxis_title="")
    st.plotly_chart(fig_region, use_container_width=True)

with c2:
    st.subheader("Sales by Category")
    category_data = filtered.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_category = px.pie(
        category_data,
        names="Category",
        values="Sales",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig_category.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_category, use_container_width=True)

# -----------------------------------------------------------------------
# ROW 2: Monthly Trend
# -----------------------------------------------------------------------
st.subheader("Monthly Revenue & Profit Trend")
monthly = filtered.groupby("Month", as_index=False)[["Sales", "Profit"]].sum().sort_values("Month")

fig_trend = go.Figure()
fig_trend.add_trace(
    go.Scatter(
        x=monthly["Month"], y=monthly["Sales"], mode="lines+markers", name="Revenue",
        line=dict(color="#3B82F6", width=3),
    )
)
fig_trend.add_trace(
    go.Scatter(
        x=monthly["Month"], y=monthly["Profit"], mode="lines+markers", name="Profit",
        line=dict(color="#10B981", width=3),
    )
)
fig_trend.update_layout(
    xaxis_title="Month",
    yaxis_title="Amount ($)",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------------------------------------------------
# ROW 3: Top Products
# -----------------------------------------------------------------------
st.subheader("Top 10 Products by Revenue")
top_products = (
    filtered.groupby("Product", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_top = px.bar(
    top_products.sort_values("Sales"),
    x="Sales",
    y="Product",
    orientation="h",
    text_auto=".2s",
    color="Sales",
    color_continuous_scale="Blues",
)
fig_top.update_layout(coloraxis_showscale=False, xaxis_title="Sales ($)", yaxis_title="")
st.plotly_chart(fig_top, use_container_width=True)

with st.expander("View Top Products Data Table"):
    st.dataframe(
        top_products.style.format({"Sales": "${:,.2f}", "Profit": "${:,.2f}", "Quantity": "{:,}"}),
        use_container_width=True,
    )

# -----------------------------------------------------------------------
# ROW 4: Region x Category Heatmap
# -----------------------------------------------------------------------
st.subheader("Region vs Category Sales Heatmap")
pivot = filtered.pivot_table(index="Region", columns="Category", values="Sales", aggfunc="sum", fill_value=0)
fig_heat = px.imshow(
    pivot,
    text_auto=".2s",
    color_continuous_scale="YlGnBu",
    aspect="auto",
)
fig_heat.update_layout(xaxis_title="Category", yaxis_title="Region")
st.plotly_chart(fig_heat, use_container_width=True)

# -----------------------------------------------------------------------
# RAW DATA
# -----------------------------------------------------------------------
with st.expander("🔎 View Filtered Raw Data"):
    st.dataframe(filtered.sort_values("Date", ascending=False), use_container_width=True)
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", data=csv, file_name="filtered_sales.csv", mime="text/csv")
