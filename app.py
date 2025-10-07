import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# --------------------------
# Page Config
# --------------------------
st.set_page_config(page_title="COVID Dashboard", layout="wide")
st.title(" COVID-19 Dashboard ")

# --------------------------
# Load Data from JSON URL
# --------------------------
json_url = "https://disease.sh/v3/covid-19/historical/all?lastdays=all"  
response = requests.get(json_url)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
else:
    st.error("❌ Failed to fetch JSON data!")

# --------------------------
# Handle Date Column / Index
# --------------------------
# Agar first column index me aa gaya hai
df.index = pd.to_datetime(df.index, format="%m/%d/%y", errors='coerce')
df.reset_index(inplace=True)
df.rename(columns={'index': 'Date'}, inplace=True)
# --------------------------
# Compute Recovery & Mortality Rates
# --------------------------
df['recovery_rate'] = (df['recovered'] / df['cases'] * 100).round(2)
df['mortality_rate'] = (df['deaths'] / df['cases'] * 100).round(2)

# --------------------------
# Sidebar Filters
# --------------------------
st.sidebar.header("Filters")
start_date = st.sidebar.date_input(
    "Start Date",
    value=df['Date'].min(),               # default = earliest date
    min_value=df['Date'].min(),           # cannot go before first date
    max_value=df['Date'].max()            # cannot go after last date
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df['Date'].max(),               # default = latest date
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)
metrics = st.sidebar.multiselect(
    "Select Metrics to Display",
    ['cases','deaths','recovered','recovery_rate','mortality_rate'],
    default=['cases','deaths','recovered']
)

# Filter Data
mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
df_filtered = df.loc[mask]

# --------------------------
# Display Total & Daily Metrics
# --------------------------
st.subheader("Key COVID-19 Metrics")

# Filter data first
df_date_filtered = df_filtered.copy()

# Calculate daily numbers
df_date_filtered['daily_cases'] = df_date_filtered['cases'].diff().fillna(0)
df_date_filtered['daily_deaths'] = df_date_filtered['deaths'].diff().fillna(0)
df_date_filtered['daily_recovered'] = df_date_filtered['recovered'].diff().fillna(0)

# Get latest totals and daily numbers
total_cases = int(df_date_filtered['cases'].iloc[-1])
total_deaths = int(df_date_filtered['deaths'].iloc[-1])
total_recovered = int(df_date_filtered['recovered'].iloc[-1])

daily_cases = int(df_date_filtered['daily_cases'].iloc[-1])
daily_deaths = int(df_date_filtered['daily_deaths'].iloc[-1])
daily_recovered = int(df_date_filtered['daily_recovered'].iloc[-1])

# Display metrics in columns
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Cases", value=f"{total_cases:,}", delta=f"+{daily_cases:,} today")
col2.metric(label="Total Deaths", value=f"{total_deaths:,}", delta=f"+{daily_deaths:,} today")
col3.metric(label="Total Recovered", value=f"{total_recovered:,}", delta=f"+{daily_recovered:,} today")



# --------------------------
# Line Chart with Twin Axis
# --------------------------
st.subheader("COVID Trends Over Time")
fig, ax1 = plt.subplots(figsize=(12,6))

# Left axis: Cases / Deaths / Recovered
if 'cases' in metrics:
    ax1.plot(df_filtered['Date'], df_filtered['cases'], label='Cases', color='orange')
if 'deaths' in metrics:
    ax1.plot(df_filtered['Date'], df_filtered['deaths'], label='Deaths', color='red')
if 'recovered' in metrics:
    ax1.plot(df_filtered['Date'], df_filtered['recovered'], label='Recovered', color='green')

ax1.set_xlabel("Date")
ax1.set_ylabel("Count")
ax1.tick_params(axis='y')
ax1.grid(True)

# Right axis: Recovery & Mortality Rates
ax2 = ax1.twinx()
if 'recovery_rate' in metrics:
    ax2.plot(df_filtered['Date'], df_filtered['recovery_rate'], label='Recovery Rate (%)', color='lime')
if 'mortality_rate' in metrics:
    ax2.plot(df_filtered['Date'], df_filtered['mortality_rate'], label='Mortality Rate (%)', color='darkred')

ax2.set_ylabel("Percentage")
ax2.tick_params(axis='y')
fig.tight_layout()
st.pyplot(fig)
