# 🏎️ F1 Fastest Laps Explorer

A data product dashboard built with [Streamlit](https://streamlit.io) and powered by [OpenF1 API](https://openf1.org).  
Explore the fastest laps in Formula 1 from 2023 to 2025 with interactive rankings, race results, and driver histories.

[👉 View Live App on Streamlit Community Cloud](https://f1-fastest-laps-5qwayvvftwubdpkpm8qcoj.streamlit.app/)

---

## 🎯 Features

- **Ranking Tab:** See a horizontal bar chart ranking drivers by the number of fastest laps, with filters for year, session name, and session type.
- **Races Tab:** View a table of the fastest driver for each race, filtered by year.
- **Driver Log Tab:** Explore the history of fastest laps for any driver, with full filtering.
- Clean, responsive UI with F1 branding and logo.
- Lap times stored as durations (`timedelta`) for accurate sorting & metrics.
- Human-readable lap times shown in **minutes:seconds.milliseconds**.
- Fully responsive: optimized for desktop and mobile.
- Clean separation of production app (`app.py`) and development scripts (`scripts/` folder).

---

## 🗂️ Folder Structure

├── app.py # Main Streamlit application  
├── verstappen_fastest_laps.csv # Dataset for the app  
├── all_drivers_fastest_laps.csv # Fastest laps for all drivers  
├── f1_logo.png # F1 logo for branding  
├── requirements.txt # Project dependencies  
├── .gitignore # Exclude unnecessary files from repo  
├── README.md # Project overview & instructions  
└── scripts/ # Helper scripts used during data preparation

---

## 🛠️ Scripts Folder

The `scripts/` folder contains development scripts used during data collection and preparation:
- `verstappen_fastest_laps.py`: prepares Verstappen lap dataset
- `drivers_data.py`: prepares fastest laps for all drivers
- Other scripts for exploring and fetching OpenF1 data

👉 These are **not required to run the live app**, but are included for reproducibility.

---

## 🚀 How to Run Locally

1️⃣ Clone this repository:
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/f1-fastest-laps.git
cd f1-fastest-laps
```

2️⃣ Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

4️⃣ Launch the app:
```bash
streamlit run app.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501)

---

## 👨‍💻 Author

Built by **Miguel Mego**  
[LinkedIn](https://www.linkedin.com/in/miguelmego/) | [GitHub](https://github.com/Mikimetal)

---

## 💡 Acknowledgements

- [Streamlit](https://streamlit.io)
- [OpenF1 API](https://openf1.org)
- Formula 1 / Red Bull Racing