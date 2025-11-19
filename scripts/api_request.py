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
with open('data/private_api_key.txt','r') as file:
    for line in file:
        token = line
        break


all_data = get_all_stations_data('https://www.infoclimat.fr/opendata/',
                                'csv',
                                active_stations,
                                '2025-10-06',
                                '2025-10-06',
                                token,
                                verbose = True)

save_df_as_csv('../data/today_data.csv',all_data)