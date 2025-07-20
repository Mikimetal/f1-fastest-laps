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
def load_verstappen_data():
    return pd.read_csv("verstappen_fastest_laps.csv")

@st.cache_data
def load_all_drivers_data():
    return pd.read_csv("all_drivers_fastest_laps.csv")

# ========================================
# Top header with logo + title
# ========================================
header_col1, header_col2 = st.columns([1, 8])
with header_col1:
    try:
        st.image("f1_logo.png", width=80)
    except Exception:
        st.write("")
with header_col2:
    st.markdown("<h1 style='text-align: left;'>F1 Fastest Laps Explorer</h1>", unsafe_allow_html=True)

verstappen_df = load_verstappen_data()
all_drivers_df = load_all_drivers_data()

## ========================================
# Tabs: Ranking, Races, Driver Log
## ========================================
tab1, tab2, tab3 = st.tabs(["Ranking", "Races", "Driver Log"])
with tab2:
    # Filter for fastest drivers per race (session name and type = 'Race')
    races_df = all_drivers_df[(all_drivers_df["Session Name"] == "Race") & (all_drivers_df["Session Type"] == "Race")].copy()
    # Year filter
    years = sorted(races_df["Year"].unique())
    selected_year = st.selectbox("Year", years, index=len(years)-1, key="race_year")
    filtered_races_df = races_df[races_df["Year"] == selected_year].copy()
    st.markdown("### Fastest Drivers Per Race")
    # Display a table of fastest drivers per race
    display_races_df = filtered_races_df[["Driver Name", "Race Location", "Date", "Fastest Lap Time"]].copy()
    display_races_df = display_races_df.rename(columns={
        "Driver Name": "Driver",
        "Race Location": "Race",
        "Date": "Date",
        "Fastest Lap Time": "Fastest Lap Time"
    })
    st.dataframe(display_races_df, use_container_width=True)

with tab1:
    ranking_df = all_drivers_df.copy()

    # --- Horizontal filters ---
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        selected_year_ranking = st.selectbox("Year", sorted(ranking_df["Year"].unique()), index=len(ranking_df["Year"].unique())-1, key="ranking_year")
    with filter_col2:
        session_names_ranking = ranking_df[ranking_df["Year"] == selected_year_ranking]["Session Name"].unique()
        selected_session_name_ranking = st.selectbox("Session Name", ["All"] + list(session_names_ranking), key="ranking_session_name")
    with filter_col3:
        session_types_ranking = ranking_df[ranking_df["Year"] == selected_year_ranking]["Session Type"].unique()
        selected_session_type_ranking = st.selectbox("Session Type", ["All"] + list(session_types_ranking), key="ranking_session_type")

    # --- Apply filters ---
    ranking_df = ranking_df[ranking_df["Year"] == selected_year_ranking]
    if selected_session_name_ranking != "All":
        ranking_df = ranking_df[ranking_df["Session Name"] == selected_session_name_ranking]
    if selected_session_type_ranking != "All":
        ranking_df = ranking_df[ranking_df["Session Type"] == selected_session_type_ranking]

    # --- Count fastest laps per driver ---
    driver_counts = ranking_df["Driver Name"].value_counts().reset_index()
    driver_counts.columns = ["Driver", "Fastest Lap Count"]

    # --- Horizontal bar chart ---
    fig = px.bar(
        driver_counts,
        y="Driver",
        x="Fastest Lap Count",
        orientation="h",
        color="Driver",
        color_discrete_sequence=px.colors.qualitative.Safe,
        text="Fastest Lap Count",
    )
    fig.update_layout(
        xaxis_title="Number of Fastest Laps",
        yaxis_title="Driver",
        title_x=0.5,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    log_df = all_drivers_df.copy()
    # --- Horizontal filters ---
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    with filter_col1:
        selected_year_log = st.selectbox("Year", sorted(log_df["Year"].unique()), index=len(log_df["Year"].unique())-1, key="log_year")
    with filter_col2:
        driver_names_log = log_df[log_df["Year"] == selected_year_log]["Driver Name"].unique()
        selected_driver_log = st.selectbox("Driver", ["All"] + list(driver_names_log), key="log_driver")
    with filter_col3:
        session_names_log = log_df[log_df["Year"] == selected_year_log]["Session Name"].unique()
        selected_session_name_log = st.selectbox("Session Name", ["All"] + list(session_names_log), key="log_session_name")
    with filter_col4:
        session_types_log = log_df[log_df["Year"] == selected_year_log]["Session Type"].unique()
        selected_session_type_log = st.selectbox("Session Type", ["All"] + list(session_types_log), key="log_session_type")

    # --- Apply filters ---
    log_df = log_df[log_df["Year"] == selected_year_log]
    if selected_driver_log != "All":
        log_df = log_df[log_df["Driver Name"] == selected_driver_log]
    if selected_session_name_log != "All":
        log_df = log_df[log_df["Session Name"] == selected_session_name_log]
    if selected_session_type_log != "All":
        log_df = log_df[log_df["Session Type"] == selected_session_type_log]

    # --- Display log table ---
    display_log_df = log_df[["Driver Name", "Race Location", "Date", "Session Name", "Session Type", "Fastest Lap Time"]].copy()
    display_log_df = display_log_df.rename(columns={
        "Driver Name": "Driver",
        "Race Location": "Race",
        "Date": "Date",
        "Session Name": "Session Name",
        "Session Type": "Session Type",
        "Fastest Lap Time": "Fastest Lap Time"
    })
    st.dataframe(display_log_df, use_container_width=True)
