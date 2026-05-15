# app/dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
from analytics.bottlenecks import compute_bottlenecks, what_if_simulation
import sys

sys.path.append("..")

from analytics.bottlenecks import compute_bottlenecks


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="BMW Process Analytics",
    layout="wide"
)

st.title("🚗 BMW Order-to-Delivery Process Mining Dashboard")


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/event_log.csv", parse_dates=["timestamp"])
    return df


df = load_data()


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Filters")

# Date range filter
min_date = df["timestamp"].min()
max_date = df["timestamp"].max()

date_range = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date]
)

model_filter = st.sidebar.multiselect(
    "Model Type",
    df["model_type"].unique(),
    default=list(df["model_type"].unique())
)

shift_filter = st.sidebar.multiselect(
    "Shift",
    df["shift"].unique(),
    default=list(df["shift"].unique())
)


# Apply filters
filtered = df[
    (df["model_type"].isin(model_filter)) &
    (df["shift"].isin(shift_filter))
]


# =========================================================
# PAGE NAVIGATION
# =========================================================

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Bottlenecks", "AI Insights", "Process Map", "What-If Optimizer"]
)


# =========================================================
# PAGE 1 — OVERVIEW
# =========================================================

if page == "Overview":

    st.header("📊 Overview KPIs")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Orders", filtered["case_id"].nunique())

    col2.metric("Avg Duration (h)", f"{filtered['duration_h'].mean():.1f}")

    col3.metric("Total Events", len(filtered))

    st.divider()

    st.write("Sample Data")
    st.dataframe(filtered.head(20))


# =========================================================
# PAGE 2 — BOTTLENECKS
# =========================================================

elif page == "Bottlenecks":

    st.header("🐌 Bottleneck Analysis")

    avg, shares, insights = compute_bottlenecks()

    chart_df = avg.reset_index()
    chart_df.columns = ["activity", "avg_duration"]

    fig = px.bar(
        chart_df,
        x="activity",
        y="avg_duration",
        title="Average Duration per Activity"
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================================================
# PAGE 3 — AI INSIGHTS
# =========================================================

elif page == "AI Insights":

    st.header("🧠 AI Insights Engine")

    avg, shares, insights = compute_bottlenecks()

    for insight in insights:
        st.info("💡 " + insight)


# =========================================================
# PAGE 4 — PROCESS MAP
# =========================================================

elif page == "Process Map":

    st.header("🗺️ Discovered Process Map")

    st.image(
        "data/process_map.png",
        use_container_width=True
    )

# =========================================================
# PAGE 5 — WHAT-IF OPTIMIZER
# =========================================================

elif page == "What-If Optimizer":

    st.header("⚙️ What-If Optimization Simulator")

    st.write("Simulate process improvements in real time.")

    # Slider: night shift improvement
    night_improve = st.slider(
        "Night Shift Improvement (%)",
        0, 50, 0
    ) / 100

    # Supplier toggle
    drop_s103 = st.checkbox("Remove Supplier S103 (simulate fixing delays)")

    drop_supplier = "S103" if drop_s103 else None

    # Baseline
    baseline = what_if_simulation()

    # Improved scenario
    improved = what_if_simulation(
        night_shift_improvement=night_improve,
        drop_supplier=drop_supplier
    )

    # Display comparison
    col1, col2 = st.columns(2)

    col1.metric("Baseline Avg Lead Time (h)", baseline)
    col2.metric("Improved Avg Lead Time (h)", improved)

    st.success(f"Improvement: {round(baseline - improved, 2)} hours saved per order")