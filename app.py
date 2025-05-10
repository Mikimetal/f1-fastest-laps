import streamlit as st
import pandas as pd
import plotly.express as px

# ========================================
# Page config for cleaner title & layout
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

# Filter dataset
filtered_df = df[(df["Year"] == selected_year) & (df["Session Type"] == selected_session)]

# Sort by lap time (fastest laps first)
filtered_df = filtered_df.sort_values(by="Fastest Lap Time", ascending=False)

# ========================================
# Metrics section
# ========================================
st.write("### Key Stats")
col1, col2 = st.columns(2)
col1.metric(label="Total Races", value=filtered_df.shape[0])
col2.metric(label="Best Lap", value=f"{filtered_df['Fastest Lap Time'].min():.3f} sec")

# ========================================
# Chart
# ========================================
st.markdown(
    "<h2 style='color:#1E41FF; text-align:center;'>Verstappen's Fastest Laps</h2>",
    unsafe_allow_html=True
)

fig = px.bar(
    filtered_df,
    y="Race Location",
    x="Fastest Lap Time",
    color_discrete_sequence=["#1E41FF"],   # Red Bull blue
    orientation='h'
)

fig.update_layout(
    xaxis_tickangle=0,   # horizontal x-axis labels
    yaxis_title="Race Location",
    xaxis_title="Fastest Lap Time (seconds)",
    title_x=0.5          # center the chart title
)

st.plotly_chart(fig, use_container_width=True)
