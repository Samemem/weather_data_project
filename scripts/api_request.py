### Import libraries
import requests
import csv
import io
import pandas as pd
import json
from datetime import datetime
import math

from modules.api_module import *
from modules.stations_module import *

### Stations

stations_url = 'https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson'
stations_json = get_stations(stations_url)
active_stations = get_active_stations(stations_json)


### API requests

# WARNING : personal token, keep private
token = get_api_key('data/private_api_key.json', 'IP2')


all_data = get_all_stations_data('https://www.infoclimat.fr/opendata/',
                                'csv',
                                active_stations,
                                '2025-12-01',
                                '2025-12-07',
                                token,
                                verbose = True)

save_df_as_csv('data/weather_data_12_01-12_07.csv',all_data)