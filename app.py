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

# ========================================
# Top header with logo + title
# ========================================
header_col1, header_col2 = st.columns([1, 8])
with header_col1:
    st.image("f1_logo.png", width=80)
with header_col2:
    st.markdown("<h1 style='text-align: left;'>F1 Fastest Laps Explorer</h1>", unsafe_allow_html=True)

# ========================================
# Sidebar filters
# ========================================
with st.sidebar:
    st.header("Filters")
    df = pd.read_csv("verstappen_fastest_laps.csv")
    years = df["Year"].sort_values().unique()
    selected_year = st.selectbox("Select Year", years)

    session_types = df["Session Type"].unique()
    selected_session = st.selectbox("Select Session Type", session_types)

# ========================================
# Process data
# ========================================
filtered_df = df[(df["Year"] == selected_year) & (df["Session Type"] == selected_session)].copy()
filtered_df["Lap Duration"] = filtered_df["Fastest Lap Time"].apply(time_to_timedelta)
filtered_df_sorted = filtered_df.sort_values(by="Lap Duration", ascending=False)

# ========================================
# Stats under title
# ========================================
stats_col1, stats_col2 = st.columns(2)
stats_col1.metric(label="Total Races", value=filtered_df.shape[0])
best_lap = filtered_df["Lap Duration"].min()
best_lap_str = timedelta_to_str(best_lap)
stats_col2.metric(label="Best Lap", value=best_lap_str)

# ========================================
# Chart
# ========================================
st.markdown(
    "<h2 style='color:#1E41FF; text-align:center;'>Verstappen's Fastest Laps</h2>",
    unsafe_allow_html=True
)

filtered_df_sorted["Lap Duration Str"] = filtered_df_sorted["Lap Duration"].apply(timedelta_to_str)

fig = px.bar(
    filtered_df_sorted,
    y="Race Location",
    x=filtered_df_sorted["Lap Duration"].dt.total_seconds(),
    color_discrete_sequence=["#1E41FF"],
    orientation='h',
    text="Lap Duration Str"
)

fig.update_layout(
    xaxis_tickangle=0,
    yaxis_title="Race Location",
    xaxis_title="Fastest Lap Time (seconds)",
    title_x=0.5,
    margin=dict(l=20, r=20, t=20, b=20)  # Reduce margins to avoid scrolling
)

st.plotly_chart(fig, use_container_width=True)
