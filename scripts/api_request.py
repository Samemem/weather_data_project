### Import libraries
import requests
import csv
import io
import pandas as pd
import json
from datetime import datetime
import math


### Stations

# with open('../stations_xhr.json') as f:
#     stations_json = json.load(f)

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

def get_active_stations(stations_json):
    """
    Returns all the stations that are active at the current day
    stations_json : str
        string with json structure conaining stations properties
    Returns
    -------
    list of str
    """
    today_date = datetime.today().strftime('%Y-%m-%d')
    features = stations_json['features']
    # Keep stations that are still active today
    active_stations = [feature['properties']['id'] for feature in features \
                       if feature['properties']['last_activity'][0:10] == today_date]
    return active_stations

stations_url = 'https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson'
stations_json = get_stations(stations_url)
active_stations = get_active_stations(stations_json)


### API requests

def get_api_response(base_url,
                     format, 
                     stations,
                     start,
                     end,
                     token):
    """
    Gets the InfoClimat API response according to the given parameters
    TODO : Create a function taking directly the dictionary of parameters
    Parameters
    ----------
    base_url : str
        base url of the API
    format : str
        whether csv or json
    stations : list of str
        list of the stations ID 
    start : str
        date of the beginning of data
    end : str
        date of the end of data
    token : str
        personal token for API access

    Returns
    -------
    return of requests.get
    """
    
    parameters = {'version' : '2',
                  'method' : 'get',
                  'format' : format,
                  'stations[]' : stations,
                  'start' : start,
                  'end' : end,
                  'token' : token}
    
    return requests.get(base_url, parameters)


### Response processing

def save_response_as_csv(file_name, response):
    with open(file_name, 'w') as file:
        for line in response.text:
            file.write(line)

# save_response_as_csv('api_resp_test.csv', response)

def get_data_from_response(response, format):
    """
    Gets the data corresponding to the given API response
    Parameters
    ----------
    response : str
        API response
    format : str
        csv or json

    Returns
    -------
    pandas DataFrame
    """
    
    if format == 'csv':
        text = response.text
        # Directly create a dataframe by skipping first 5 rows
        df = pd.read_csv(io.StringIO(text),
                         delimiter=';', 
                        #  skiprows=3+nb_stations,
                        comment='#',
                         usecols=range(0,26))
        
    elif format =='json':
        print('case not handled yet')
    
    return df


# WARNING : personal token, keep private
with open('private_api_key.txt','r') as file:
    for line in file:
        token = line
        break



# response = get_api_response('https://www.infoclimat.fr/opendata/',
#                             'csv',
#                             active_stations[0:400],
#                             '2025-10-06',
#                             '2025-10-06',
#                             token)
# print(response.text[0:1000])

# data = get_data_from_response(response, 'csv')

def get_all_stations_data(base_url,format, stations,start,end,token):
    """
    Limit for one day of data is 420 stations, we keep it at 400.
    This function automatically calls the api according to the number of days,
    then concatenates the data into a dataframe.
    """
    start_date = datetime.fromisoformat(start)
    end_date = datetime.fromisoformat(end)
    delta = end_date - start_date
    # Add 1 to the difference because of indexing
    days = delta.days + 1

    nb_stations = len(stations)
    nb_stations_by_request = 400 // days
    nb_requests = math.ceil(nb_stations / nb_stations_by_request)
    list_data = []

    for i in range(nb_requests):
        # call for [i*nb_stations_by_request:(i+1)*nb_stations_by_request]
        response = get_api_response(base_url,
                                    format,
                                    active_stations[i*nb_stations_by_request:(i+1)*nb_stations_by_request],
                                    start,
                                    end,
                                    token)

        data = get_data_from_response(response, format)

        # Remove first row corresponding to metadata
        data = data.drop(axis=0, index = 0)

        list_data.append(data)
    
    return pd.concat(list_data, axis = 0)

all_data = get_all_stations_data('https://www.infoclimat.fr/opendata/',
                                'csv',
                                active_stations,
                                '2025-10-06',
                                '2025-10-06',
                                token)


def save_df_as_csv(filepath,data):
    data.to_csv(filepath)

save_df_as_csv('today_data.csv',all_data)