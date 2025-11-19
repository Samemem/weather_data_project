import geopandas as gpd
import pandas as pd
import requests


stations_url = 'https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson'
stations_json = get_stations('https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson')


normalized_stations = pd.json_normalize(stations_json['features'])


stations = gpd.read_file('stations_xhr.json', driver = 'GeoJSON')
stations.to_csv('data/stations.csv', index=0)