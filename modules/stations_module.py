from datetime import datetime
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
    stations_response = requests.get(url)
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