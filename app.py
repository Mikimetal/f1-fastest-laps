import streamlit as st
import pandas as pd
import plotly.express as px

# ========================================
# Helper function to convert time strings
# ========================================
def time_to_seconds(time_str):
    if time_str == "N/A" or pd.isna(time_str):
        return None
    try:
        minutes, seconds = time_str.split(":")
        return int(minutes) * 60 + float(seconds)
    except Exception:
        return None

# ========================================
# Page config
# ========================================
st.set_page_config(page_title="F1 Fastest Laps Explorer", page_icon="🏎️", layout="centered")

# ========================================
# Show F1 logo
# ========================================
st.image("f1_logo.png", width=200)

# ========================================
# Title
# ========================================
st.markdown("<h1 style='text-align: center;'>F1 Fastest Laps Explorer</h1>", unsafe_allow_html=True)

# ========================================
# Load data
# ========================================
df = pd.read_csv("verstappen_fastest_laps.csv")

# ========================================
# Filters
# ========================================
years = df["Year"].sort_values().unique()
selected_year = st.selectbox("Select Year", years)

session_types = df["Session Type"].unique()
selected_session = st.selectbox("Select Session Type", session_types)

filtered_df = df[(df["Year"] == selected_year) & (df["Session Type"] == selected_session)]

# ========================================
# Convert lap times to seconds for metric
# ========================================
filtered_df["Lap Seconds"] = filtered_df["Fastest Lap Time"].apply(time_to_seconds)

# Sort by lap time (fastest first)
filtered_df_sorted = filtered_df.sort_values(by="Lap Seconds", ascending=False)

# ========================================
# Metrics section
# ========================================
st.write("### Key Stats")
col1, col2 = st.columns(2)
col1.metric(label="Total Races", value=filtered_df.shape[0])
best_lap = filtered_df["Lap Seconds"].min()
best_lap_str = f"{best_lap:.3f} sec" if pd.notna(best_lap) else "N/A"
col2.metric(label="Best Lap", value=best_lap_str)

# ========================================
# Chart
# ========================================
st.markdown(
    "<h2 style='color:#1E41FF; text-align:center;'>Verstappen's Fastest Laps</h2>",
    unsafe_allow_html=True
)

fig = px.bar(
    filtered_df_sorted,
    y="Race Location",
    x="Lap Seconds",
    color_discrete_sequence=["#1E41FF"],
    orientation='h'
)

fig.update_layout(
    xaxis_tickangle=0,
    yaxis_title="Race Location",
    xaxis_title="Fastest Lap Time (seconds)",
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)
