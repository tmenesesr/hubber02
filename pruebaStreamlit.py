import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pickups in NYC by Oscar")

DATE_COLUMN = "date/time"
DATA_URL = (
    "http://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # st.write(data.columns)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    # data["date/time"] = pd.to_datetime(data["Date/Time"])
    # data["date/time"] = pd.to_datetime(data["date/time"])
    return data


# Create a text element and let the reader know the data is loading.
# st.write(st.cache.__sizeof__)
data_load_state = st.text("Loading data...")
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)

# Notify the reader that the data was successfully loaded.
# data_load_state.text("Loading data...done!")
data_load_state.text("Done! (using st.cache_data)")

# st.subheader("Raw data")
# st.write(data)
# st.write(data.columns)

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

# st.button("Rerun")

st.subheader("Number of pickups by hour")
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

st.subheader("Map of all pickups")
st.map(data)

# hour_to_filter = 17
hour_to_filter = st.slider("hour", 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)
