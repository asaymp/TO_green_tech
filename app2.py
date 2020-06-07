import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

data_url = "https://raw.githubusercontent.com/asaymp/TO_green_tech/master/full_data.csv"

st.title("Sloar water heaters and green roofs in Toronto")
st.markdown("This application is a Streamlit dashboard that can be used to locate commercial and residential solar heaters and green roofs in Toronto. Data is from the City of Toronto's open data portal.")

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(data_url)
    data.dropna(subset=['latitude', 'longitude'], inplace=True)
    return data

data = load_data()

#map of completed projects - solar heaters or green roofs
closed_projects = data[data['status']=='Closed']
st.header("Where are the green building technologies in Toronto?")
techtype = st.selectbox("Technology Type", ('Solar Water Heater', 'Green Roof'))
st.map(closed_projects.query("green_tech == @techtype")[["latitude","longitude"]].dropna(how="any"))#have to be latitude and longitude columns if we want to make a map

#barchart top neighbourhoods by number of solar heaters/green roofs
st.subheader("Top five neighbourhoods by number of installations") #
data['neighbourhood'] = data['location'].apply(lambda x: x.split(",")[4].strip())

if techtype == 'Solar Water Heater':
    nb_series = data['neighbourhood'][data['green_tech']=='Solar Water Heater']
else:
    nb_series = data['neighbourhood'][data['green_tech']=='Green Roof']

chart_data = nb_series.value_counts().rename_axis('neighbourhood').reset_index(name='count').sort_values(by='count', ascending=False).head(5)

fig = px.bar(chart_data, x='neighbourhood', y='count', hover_data=['count'], height=400)
st.write(fig)


#linechart by completed projects over time solar heaters/green roofs




#figure out how to pull the data through the City of Toronto's APIs
#attribution to Open Street Map's geolocator feature
#attribution to Deck
#attribution to Streamlit
#add City of Toronto Open Data License