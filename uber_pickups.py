import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('Uber pickups in NYC')

st.markdown('[Follow the tutorial here](https://docs.streamlit.io/get-started/tutorials/create-an-app)')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data with st.text()'):
    st.subheader('Raw data')
    st.text('with st.text()')
    st.write(data)
    
if st.checkbox('Show raw data with st.dataframe'):
    st.subheader('Raw data')
    st.text('with st.dataframe()')
    st.dataframe(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

st.subheader('Linechart of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.line_chart(hist_values)


# Plot data on a map
st.subheader('Map of all pickups')
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
