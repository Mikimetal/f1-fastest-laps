import streamlit as st
import pandas as pd
import plotly.express as px

# Optional: Show F1 logo at top
st.image("f1_logo.png", width=200)

# Title
st.title("F1 Fastest Laps Explorer")

# Load data
df = pd.read_csv("verstappen_fastest_laps.csv")

# Filter by Year
years = df["Year"].unique()
selected_year = st.selectbox("Select Year", years)

# Filter by Session Type
session_types = df["Session Type"].unique()
selected_session = st.selectbox("Select Session Type", session_types)

# Apply filters
filtered_df = df[(df["Year"] == selected_year) & (df["Session Type"] == selected_session)]

# Plot horizontal bar chart
fig = px.bar(
    filtered_df,
    y="Race Location",
    x="Fastest Lap Time",
    color_discrete_sequence=["#1E41FF"],
    orientation='h'
)

fig.update_layout(title_text="Verstappen's Fastest Laps")

# Show chart
st.plotly_chart(fig)
