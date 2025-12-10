import geopandas as gpd
import pandas as pd
import requests

from modules.stations_module import *

# Get stations
stations_url = 'https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson'
stations_json = get_stations('https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson')


# Direct json extraction
normalized_stations = pd.json_normalize(stations_json['features'])
normalized_stations.to_csv('data/normalized_stations.csv', index=0)


# Stations processing with geopandas
process_stations('stations_xhr.json','data/stations.csv')