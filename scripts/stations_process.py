import geopandas as gpd
import pandas as pd
import requests

def get_stations(url):
    """
    Calls the api to automatically get all stations properties
    url : str
        api url
    Returns
    -------
    str with json structure
    """
    stations_response = requests.get(stations_url)
    return stations_response.json()

stations_url = 'https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson'
stations_json = get_stations('https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson')


normalized_stations = pd.json_normalize(stations_json['features'])



stations = gpd.read_file('stations_xhr.json', driver = 'GeoJSON')
stations.to_csv('/data/stations.csv', index=0)