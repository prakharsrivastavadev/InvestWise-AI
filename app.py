import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_data,
    calculate_summary,
    category_summary,
    search_investments,
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="InvestWise AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
<style>

.main{
    padding-top:1rem;
}

.stMetric{
    border-radius:10px;
    padding:10px;
}

footer{
    visibility:hidden;
}

</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📈 InvestWise AI")

st.caption(
    "AI-powered Investment Analytics Dashboard"
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Upload Investment Dataset")

st.sidebar.info(
"""
Required CSV columns:

• Date
• Investment
• Category
• Amount
• Return
• Status
"""
)

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV",
    type=["csv"],
)

# --------------------------------------------------
# Wait for Upload
# --------------------------------------------------

if uploaded_file is None:

    st.info(
        "Upload a CSV file to begin."
    )

    st.stop()

# --------------------------------------------------
# Safe Data Loading
# --------------------------------------------------

try:

    df = load_data(uploaded_file)

except Exception as e:

    st.error(
        "Unable to load dataset."
    )

    st.exception(e)

    st.stop()

# --------------------------------------------------
# Empty Dataset Check
# --------------------------------------------------

if df.empty:

    st.warning(
        "Dataset contains no valid records."
    )

    st.stop()
  # --------------------------------------------------
# Investment Summary
# --------------------------------------------------

try:

    summary = calculate_summary(df)

except Exception as e:

    st.error(
        "Unable to calculate investment summary."
    )

    st.exception(e)

    st.stop()

st.subheader("📊 Investment Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Investment",
        f"₹{summary['Total Investment']:,.2f}",
    )

with col2:

    st.metric(
        "Total Return",
        f"₹{summary['Total Return']:,.2f}",
    )

with col3:

    st.metric(
        "Profit / Loss",
        f"₹{summary['Profit']:,.2f}",
    )

with col4:

    st.metric(
        "ROI",
        f"{summary['ROI']:.2f}%",
    )

st.divider()

# --------------------------------------------------
# Category Summary
# --------------------------------------------------

try:

    categories_df = category_summary(df)

except Exception as e:

    st.error(
        "Unable to generate category summary."
    )

    st.exception(e)

    categories_df = pd.DataFrame(
        columns=[
            "Category",
            "Amount",
            "Return",
        ]
    )

st.subheader("📂 Category Summary")

st.dataframe(
    categories_df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# --------------------------------------------------
# Investment Statistics
# --------------------------------------------------

st.subheader("📈 Investment Statistics")

left, right = st.columns(2)

with left:

    st.write(
        f"**Investments:** {df['Investment'].nunique()}"
    )

    st.write(
        f"**Categories:** {df['Category'].nunique()}"
    )

    st.write(
        f"**Statuses:** {df['Status'].nunique()}"
    )

with right:

    st.write(
        f"**First Investment:** "
        f"{df['Date'].min().date()}"
    )

    st.write(
        f"**Latest Investment:** "
        f"{df['Date'].max().date()}"
    )

    st.write(
        f"**Records:** {len(df)}"
    )

st.divider()
# --------------------------------------------------
# Investment Search
# --------------------------------------------------

st.subheader("🔍 Investment Search")

search_text = st.text_input(
    "Search Investment",
    placeholder="Example: Apple, SBI Fund, Bitcoin",
)

try:

    filtered_df = search_investments(
        df,
        search_text,
    ).reset_index(drop=True)

except Exception as e:

    st.error(
        "Unable to search investments."
    )

    st.exception(e)

    filtered_df = df.copy().reset_index(drop=True)

# --------------------------------------------------
# Investment Table
# --------------------------------------------------

investments_df = filtered_df.copy()

investments_df["Profit"] = (
    investments_df["Return"]
    - investments_df["Amount"]
)

st.write(
    f"Showing **{len(investments_df):,}** investment(s)."
)

if investments_df.empty:

    st.warning(
        "No matching investments found."
    )

else:

    st.dataframe(
        investments_df,
        use_container_width=True,
        hide_index=True,
    )

# --------------------------------------------------
# Download CSV
# --------------------------------------------------

try:

    csv = investments_df.to_csv(
        index=False,
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Investment CSV",
        data=csv,
        file_name="investments.csv",
        mime="text/csv",
    )

except Exception as e:

    st.error(
        "Unable to prepare CSV download."
    )

    st.exception(e)

st.divider()

# --------------------------------------------------
# Top Investments
# --------------------------------------------------

st.subheader("🏆 Top Investments")

if not investments_df.empty:

    top_investments = (
        investments_df.sort_values(
            by="Return",
            ascending=False,
        )
        .head(10)
    )

    st.dataframe(
        top_investments,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No investments available."
    )

st.divider()

# --------------------------------------------------
# Dataset Preview
# --------------------------------------------------

st.subheader("📄 Dataset Preview")

preview_rows = st.slider(
    "Rows to Preview",
    min_value=5,
    max_value=50,
    value=10,
)

st.dataframe(
    filtered_df.head(preview_rows),
    use_container_width=True,
    hide_index=True,
)

st.divider()
# --------------------------------------------------
# Investment Analytics
# --------------------------------------------------

st.subheader("📊 Investment Analytics")

# --------------------------------------------------
# Investment by Category
# --------------------------------------------------

try:

    if not categories_df.empty:

        fig = px.pie(
            categories_df,
            names="Category",
            values="Amount",
            hole=0.45,
            title="Investment by Category",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

except Exception as e:

    st.error(
        "Unable to generate category chart."
    )

    st.exception(e)

# --------------------------------------------------
# Investment vs Return
# --------------------------------------------------

try:

    if not categories_df.empty:

        fig = px.bar(
            categories_df,
            x="Category",
            y=[
                "Amount",
                "Return",
            ],
            barmode="group",
            title="Investment vs Return",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

except Exception as e:

    st.error(
        "Unable to generate comparison chart."
    )

    st.exception(e)

# --------------------------------------------------
# Profit by Investment
# --------------------------------------------------

try:

    profit_df = investments_df.copy()

    profit_df["Profit"] = (
        profit_df["Return"]
        - profit_df["Amount"]
    )

    fig = px.bar(
        profit_df,
        x="Investment",
        y="Profit",
        color="Status",
        title="Profit / Loss by Investment",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

except Exception as e:

    st.error(
        "Unable to generate profit chart."
    )

    st.exception(e)

# --------------------------------------------------
# Return Distribution
# --------------------------------------------------

try:

    fig = px.histogram(
        investments_df,
        x="Return",
        nbins=20,
        title="Return Distribution",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

except Exception as e:

    st.error(
        "Unable to generate return distribution."
    )

    st.exception(e)

# --------------------------------------------------
# Investment Timeline
# --------------------------------------------------

try:

    timeline_df = (
        filtered_df.copy()
        .sort_values("Date")
    )

    fig = px.line(
        timeline_df,
        x="Date",
        y="Return",
        color="Investment",
        markers=True,
        title="Investment Timeline",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

except Exception as e:

    st.error(
        "Unable to generate timeline."
    )

    st.exception(e)

st.divider()
# --------------------------------------------------
# Investment Insights
# --------------------------------------------------

st.subheader("📈 Investment Insights")

display_df = investments_df.reset_index(
    drop=True
)

if display_df.empty:

    st.info(
        "No investments available."
    )

else:

    selected_index = st.selectbox(
        "Select Investment",
        options=range(len(display_df)),
        format_func=lambda x:
            f"{display_df.iloc[x]['Investment']} | "
            f"₹{display_df.iloc[x]['Return']:,.2f}",
    )

    investment = display_df.iloc[selected_index]

    col1, col2 = st.columns(2)

    with col1:

        st.write("### Investment Details")

        st.write(
            f"**Investment:** {investment['Investment']}"
        )

        st.write(
            f"**Category:** {investment['Category']}"
        )

        st.write(
            f"**Status:** {investment['Status']}"
        )

        st.write(
            f"**Date:** {investment['Date'].date()}"
        )

    with col2:

        st.write("### Financial Details")

        st.write(
            f"**Amount:** ₹{investment['Amount']:,.2f}"
        )

        st.write(
            f"**Return:** ₹{investment['Return']:,.2f}"
        )

        st.write(
            f"**Profit:** ₹{investment['Profit']:,.2f}"
        )

        roi = 0.0

        if investment["Amount"] > 0:

            roi = (
                investment["Profit"]
                / investment["Amount"]
            ) * 100

        st.write(
            f"**ROI:** {roi:.2f}%"
        )

        average_return = (
            display_df["Return"].mean()
        )

        if investment["Return"] >= average_return * 2:

            st.success(
                "This is one of your highest-performing investments."
            )

        elif investment["Return"] >= average_return:

            st.info(
                "This investment is performing above average."
            )

        else:

            st.warning(
                "This investment is performing below average."
            )

st.divider()

# --------------------------------------------------
# Best Performing Investments
# --------------------------------------------------

st.subheader("🏆 Best Performing Investments")

ranking_df = display_df.sort_values(
    by="Profit",
    ascending=False,
)

st.dataframe(
    ranking_df,
    use_container_width=True,
    hide_index=True,
)

st.divider()
# --------------------------------------------------
# Dataset Health Report
# --------------------------------------------------

st.subheader("🩺 Dataset Health Report")

total_records = len(df)

missing_values = int(df.isna().sum().sum())

duplicate_rows = int(df.duplicated().sum())

health_score = max(
    0,
    100 - (
        missing_values
        + duplicate_rows
    ),
)

health_score = min(
    100,
    health_score,
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Records",
        total_records,
    )

    st.metric(
        "Missing Values",
        missing_values,
    )

with col2:

    st.metric(
        "Duplicate Rows",
        duplicate_rows,
    )

    st.metric(
        "Categories",
        df["Category"].nunique(),
    )

with col3:

    st.metric(
        "Investments",
        df["Investment"].nunique(),
    )

    st.metric(
        "Dataset Quality",
        f"{health_score}%",
    )

st.divider()

# --------------------------------------------------
# Investment Summary
# --------------------------------------------------

st.subheader("📋 Investment Summary")

summary_df = pd.DataFrame(
    {
        "Metric": [
            "Rows",
            "Columns",
            "Investments",
            "Categories",
            "Total Investment",
            "Total Return",
            "Profit",
            "ROI",
        ],
        "Value": [
            len(df),
            len(df.columns),
            df["Investment"].nunique(),
            df["Category"].nunique(),
            f"₹{summary['Total Investment']:,.2f}",
            f"₹{summary['Total Return']:,.2f}",
            f"₹{summary['Profit']:,.2f}",
            f"{summary['ROI']:.2f}%",
        ],
    }
)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    "InvestWise AI • Built with Streamlit, Pandas and Plotly"
)










