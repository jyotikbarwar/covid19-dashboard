# COVID-19 Dashboard

This is an interactive COVID-19 dashboard built using **Streamlit**, **Pandas**, **Matplotlib**, and **Requests**.  
It visualizes global COVID-19 data from **2020 to 2023** and allows users to explore trends, daily cases, deaths, and recoveries.

---

## Features

- Data fetched from [disease.sh](https://disease.sh/) API
- Total and daily numbers of Cases , Deaths , Recovered 
- Interactive date filter (2020-2023)
- Line charts with twin axis:
  - Counts (Cases, Deaths, Recovered) on left axis
  - Rates (Recovery %, Mortality %) on right axis
- User-friendly interface for easy exploration.

## Installation & Run Locally

1. **Clone the repository**
```bash
git clone <YOUR_REPO_URL>
cd <REPO_FOLDER>

python3 -m venv covid_env
source covid_env/bin/activate   # Mac/Linux
# OR
covid_env\Scripts\activate      # Windows
pip install -r requirements.txt
streamlit run app.py
