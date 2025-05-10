import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("verstappen_fastest_laps.csv")

# Streamlit app
st.title("F1 Fastest Laps Explorer")
selected_year = st.selectbox("Select Year", df["Year"].unique())
filtered_df = df[df["Year"] == selected_year]

fig = px.bar(filtered_df, x="Race Location", y="Fastest Lap Time", color="Session Type")
st.plotly_chart(fig)
