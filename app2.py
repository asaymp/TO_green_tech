import pandas as pd
import requests
import io
import streamlit as st

from geopy.geocoders import Nominatim


class GreenToronto():

    def __init__(self):

        self.heaters_url = ('https://raw.githubusercontent.com/asaymp/TO_green_tech/master/Solar%20Hot%20Water%20Heater%20Data.csv')
        self.rooves_url = ('https://raw.githubusercontent.com/asaymp/TO_green_tech/master/Building%20Permits%20-%20Green%20Roofs%20Data.csv')

        st.title("Sloar water heaters and green rooves in Toronto")
        st.markdown("This application is a Streamlit dashboard that can be used to locate commercial and residential solar heaters and green rooves in Toronto. Data is from the City of Toronto's open data portal.")

    @st.cache(persist=True)
    def load_data(self):
        heater_download = requests.Session().get(self.heaters_url).content
        heater_data = pd.read_csv(io.StringIO(heater_download.decode('utf-8')))
        heater_data['green_tech'] = 'Solar Water Heater'
        roof_download = requests.Session().get(self.rooves_url).content
        heater_data = pd.read_csv(io.StringIO(roof_download.decode('utf-8')))
        roof_data['green_tech'] = 'Green Roof'
        data = pd.concat([heater_data, roof_data], ignore_index=True)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data['heater_work'] = data['work']
        data.drop('work', axis=1, inplace=True)
        date_cols = ['application_date','completed_date','issued_date']
        for col in date_cols:
            data[col] = pd.to_datetime(data[col])
            data[col] = [date.date() for date in data[col]]
        data['address'] = data['street_num'] + ' ' + data['street_name'] + ' ' + data['street_type'] + data['street_direction'] + ' Toronto, Canada'
        #geolocator = Nominatim(user_agent='')
        #data['latitude'] = geolocator.geocode(data['address']).latitude
        #data['longitude'] = geolocator.geocode(data['address']).longitude
        #pd.to_csv('green_Toronto_full_data.csv')
        return data

if __name__ == '__main__':
    gt = GreenToronto()
    gt.load_data()
#figure out how to pull the data through the City of Toronto's APIs

#attribution to Open Street Map's geolocator feature
#attribution to Deck
#attribution to Streamlit
#add City of Toronto Open Data License