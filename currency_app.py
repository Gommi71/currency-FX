import streamlit as st
import requests
import pandas as pd
import datetime
import plotly.express as px

st.title("Currency Exchange Rate Viewer")

amount = st.number_input("Enter amount", min_value=0.0, value=100.0)
currency_options = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY']
base_currency = st.selectbox("Select base currency", currency_options)
target_currency = st.selectbox("Select target currency", currency_options)
time_range = st.selectbox("Select time range", ['7 days', '1 month', '3 months', '6 months', '1 year'])

range_days = {
    '7 days': 7,
    '1 month': 30,
    '3 months': 90,
    '6 months': 180,
    '1 year': 365
}

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=range_days[time_range])

url = f"https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&base={base_currency}&symbols={target_currency}"
response = requests.get(url)
data = response.json()

latest_url = f"https://api.exchangerate.host/latest?base={base_currency}&symbols={target_currency}"
latest_response = requests.get(latest_url)
latest_data = latest_response.json()
current_rate = latest_data['rates'][target_currency]
converted_amount = amount * current_rate

st.subheader("Current Exchange Rate")
st.write(f"{amount} {base_currency} = {converted_amount:.2f} {target_currency} (Rate: {current_rate:.4f})")

if data['success']:
    rates = data['rates']
    dates = []
    values = []
    for date in sorted(rates.keys()):
        dates.append(date)
        values.append(rates[date][target_currency])
    
    df = pd.DataFrame({'Date': dates, 'Exchange Rate': values})
    fig = px.line(df, x='Date', y='Exchange Rate', title=f'{base_currency} to {target_currency} Exchange Rate Over Time')
    st.plotly_chart(fig)
else:
    st.error("Failed to fetch historical exchange rate data.")
