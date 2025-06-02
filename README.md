# 🏎️ F1 Fastest Laps Explorer

A data product dashboard built with [Streamlit](https://streamlit.io) and powered by [OpenF1 API](https://openf1.org).  
This project allows you to explore Max Verstappen's fastest laps across all F1 races between 2023 and 2025 in a clean, interactive, and responsive dashboard.

[👉 View Live App on Streamlit Community Cloud](https://f1-fastest-laps-5qwayvvftwubdpkpm8qcoj.streamlit.app/)

![F1_Fastest_Laps_Explorer](https://github.com/Mikimetal/f1-fastest-laps/blob/main/streamlit_app.png?raw=true)

---

## 🎯 Features

- Filters by Year and Session Type (Race, Practice, Qualifying)
- Horizontal bar chart showing Verstappen's fastest lap times
- Lap times stored as durations (`timedelta`) for accurate sorting & metrics
- Human-readable lap times shown in **minutes:seconds.milliseconds**
- Key Stats panel showing **Total Races** and **Best Lap**
- Red Bull Racing official blue color bars
- Formula 1 branding with logo and professional layout
- Fully responsive: optimized for desktop and mobile
- Clean separation of production app (`app.py`) and development scripts (`scripts/` folder)

---

## 🗂️ Folder Structure

├── app.py # Main Streamlit application
├── verstappen_fastest_laps.csv # Dataset for the app
├── f1_logo.png # F1 logo for branding
├── requirements.txt # Project dependencies
├── .gitignore # Exclude unnecessary files from repo
├── README.md # Project overview & instructions
└── scripts/ # Helper scripts used during data preparation

---

## 🛠️ Scripts Folder

The `scripts/` folder contains development scripts used during data collection and preparation:
- `fetch_lap_data.py`: example script to collect lap data from OpenF1
- `explore_sessions.py`: test script to explore OpenF1 session data
- `verstappen_fastest_laps.py`: script to prepare Verstappen lap dataset

👉 These are **not required to run the live app**, but are included for reproducibility.

---

## 🚀 How to Run Locally

1️⃣ Clone this repository:
git clone https://github.com/YOUR_GITHUB_USERNAME/f1-fastest-laps.git
cd f1-fastest-laps

2️⃣ Create a virtual environment:
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3️⃣ Install dependencies:
pip install -r requirements.txt

4️⃣ Launch the app:
streamlit run app.py

The app will open in your browser at [http://localhost:8501](http://localhost:8501)


---

## 👨‍💻 Author

Built by **Miguel Mego**  
[LinkedIn](https://www.linkedin.com/in/miguelmego/) | [GitHub](https://github.com/Mikimetal)

---

## 💡 Acknowledgements

- [Streamlit](https://streamlit.io)
- [OpenF1 API](https://openf1.org)
- Formula 1 / Red Bull Racing branding
