import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import statsmodels.api as sm
import streamlit as st
from datetime import datetime

dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
death = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
rec = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

cases = dat[dat['Country/Region'] == 'Belgium'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
cases = cases.melt()
cases['Daily Cases'] = cases['value'].diff().fillna(0)
cases = cases[['variable','Daily Cases']]

deaths = death[death['Country/Region'] == 'Belgium'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
deaths = deaths.melt()
deaths['Daily Deaths'] = deaths['value'].diff().fillna(0)
deaths = deaths[['variable','Daily Deaths']]

recoveries = rec[rec['Country/Region'] == 'Belgium'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
recoveries = recoveries.melt()
recoveries['Daily Recoveries'] = recoveries['value'].diff().fillna(0)
recoveries = recoveries[['variable','Daily Recoveries']]

data = pd.merge(cases, deaths, on="variable")
data = pd.merge(data, recoveries, on="variable")
data['variable'] = pd.to_datetime(data['variable'])

data['Daily Cases'] = data['Daily Cases'].apply(lambda x: max(x, 0))
data['Daily Deaths'] = data['Daily Deaths'].apply(lambda x: max(x, 0))
data['Daily Recoveries'] = data['Daily Recoveries'].apply(lambda x: max(x, 0))
data = data.rename(columns = {'variable':'Date'})

st.title('Belgium: COVID-19 Cases and Outcomes')

option = st.selectbox(
   "What type of COVID data do you want to be displayed?",
   ("Daily Cases", "Daily Deaths", "Daily Recoveries"),
   index=None,
   placeholder="Select type of COVID data ..."
)

if option in ["Daily Cases", "Daily Deaths", "Daily Recoveries"]: 
   st.line_chart(data,x = 'Date', y =option) 
else: 
   st.line_chart(data,x = 'Date', y ='Daily Cases') 

timeline = st.slider(
    "Select the time range:",
    value=(datetime(2020, 1, 20), datetime(2023, 3, 9)))

date_range = pd.date_range(start=timeline[0], end=timeline[1], freq='D')
timeline = date_range.tolist()

chart_data = data[data['Date'].isin(timeline)]

if option in ["Daily Cases", "Daily Deaths", "Daily Recoveries"]: 
   st.line_chart(chart_data, x='Date', y=option) 
else: 
   st.line_chart(chart_data,x = 'Date', y ='Daily Cases') 