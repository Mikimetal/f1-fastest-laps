import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

# ========================================
# Helper functions
# ========================================
def time_to_timedelta(time_str):
    if time_str == "N/A" or pd.isna(time_str):
        return None
    try:
        minutes, seconds = time_str.split(":")
        total_seconds = int(minutes) * 60 + float(seconds)
        return timedelta(seconds=total_seconds)
    except Exception:
        return None

def timedelta_to_str(td):
    if pd.isna(td) or td is None:
        return "N/A"
    total_seconds = td.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:06.3f}"

# ========================================
# Page config
# ========================================
st.set_page_config(page_title="F1 Fastest Laps Explorer", page_icon="🏎️", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("verstappen_fastest_laps.csv")

# ========================================
# Top header with logo + title
# ========================================
header_col1, header_col2 = st.columns([1, 8])
with header_col1:
    try:
        st.image("f1_logo.png", width=80, caption="Formula 1 Logo")
    except Exception:
        st.write("F1 Logo")
with header_col2:
    st.markdown("<h1 style='text-align: left;'>F1 Fastest Laps Explorer</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Filters")
    df = load_data()
    years = df["Year"].sort_values().unique()
    selected_year = st.selectbox("Select Year", years)

## ========================================
# Process data for grouped bar chart (Race vs Qualifying)
## ========================================
filtered_df = df[(df["Year"] == selected_year) & (df["Session Type"].isin(["Race", "Qualifying"]))].copy()
filtered_df["Lap Duration"] = filtered_df["Fastest Lap Time"].apply(time_to_timedelta)

# Pivot so each location has Race and Qualifying lap times
pivot_df = filtered_df.pivot_table(
    index=["Race Location", "Date"],
    columns="Session Type",
    values="Lap Duration",
    aggfunc="min"
).reset_index()

# Only keep rows with at least one valid lap
pivot_df = pivot_df.dropna(subset=["Race", "Qualifying"], how="all")

# Sort by date (most recent first)
pivot_df = pivot_df.sort_values(by="Date", ascending=False)

# Format lap times for display
pivot_df["Race Lap Str"] = pivot_df["Race"].apply(timedelta_to_str)
pivot_df["Qualifying Lap Str"] = pivot_df["Qualifying"].apply(timedelta_to_str)

# Handle empty DataFrame
if pivot_df.empty:
    st.warning("No data available for Race or Qualifying sessions in the selected year.")
    st.stop()

## ========================================
# Stats under title
## ========================================
stats_col1, stats_col2 = st.columns(2)
stats_col1.metric(label="Total Races", value=pivot_df.shape[0])
best_race_lap = pivot_df["Race"].min()
best_race_lap_str = timedelta_to_str(best_race_lap)
stats_col2.metric(label="Best Race Lap", value=best_race_lap_str)

## ========================================
# Grouped Bar Chart: Race vs Qualifying
## ========================================
st.markdown(
    "<h2 style='color:#1E41FF; text-align:center;'>Race vs Qualifying Fastest Laps</h2>",
    unsafe_allow_html=True
)

chart_df = pivot_df.copy()

# Melt for grouped bar chart (parallel bars)
chart_melted = chart_df.melt(
    id_vars=["Race Location", "Date"],
    value_vars=["Race", "Qualifying"],
    var_name="Session",
    value_name="Lap Duration"
)

chart_melted["Lap Duration Str"] = chart_melted["Lap Duration"].apply(timedelta_to_str)

fig = px.bar(
    chart_melted,
    y="Race Location",
    x="Lap Duration",
    color="Session",
    orientation="h",
    text="Lap Duration Str",
    barmode="group",
    color_discrete_map={"Race": "#1E41FF", "Qualifying": "#FF1E41"}
)

fig.update_layout(
    xaxis_tickangle=0,
    yaxis_title="Race Location",
    xaxis_title="Lap Time (seconds)",
    title_x=0.5,
    margin=dict(l=20, r=20, t=20, b=20),
    legend_title_text="Session Type"
)

st.plotly_chart(fig, use_container_width=True)
