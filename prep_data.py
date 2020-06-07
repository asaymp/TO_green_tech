import pandas as pd
import requests
import io
import os, ssl
from geopy.geocoders import Nominatim


class GreenTOData():

    def __init__(self):

        self.heaters_url = ('https://raw.githubusercontent.com/asaymp/TO_green_tech/master/Solar%20Hot%20Water%20Heater%20Data.csv')
        self.rooves_url = ('https://raw.githubusercontent.com/asaymp/TO_green_tech/master/Building%20Permits%20-%20Green%20Roofs%20Data.csv')

    def prep_data(self):
        heater_download = requests.Session().get(self.heaters_url).content
        heater_data = pd.read_csv(io.StringIO(heater_download.decode('utf-8')))
        heater_data['green_tech'] = 'Solar Water Heater'
        roof_download = requests.Session().get(self.rooves_url).content
        roof_data = pd.read_csv(io.StringIO(roof_download.decode('utf-8')))
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
        data['address'] = data['street_num'] + ' ' + data['street_name'] + ' ' + data['street_type'] + ' ' + data['street_direction'] + ' Toronto, Canada'

        geolocator = Nominatim(user_agent='**********')

        def getLocation(cell):
            try:
                return geolocator.geocode(cell)
            except:
                return None

        location = data.address.apply(getLocation)
        data['location'] = location

        def getLat(cell):
            try:
                return cell.latitude
            except:
                return None

        def getLon(cell):
            try:
                return cell.longitude
            except:
                return None

        latitude = data.location.apply(getLat)
        data['latitude'] = latitude
        longitude = data.location.apply(getLon)
        data['longitude'] = longitude

        return data

if __name__ == '__main__':
    gtd = GreenTOData()
    gtd.prep_data()