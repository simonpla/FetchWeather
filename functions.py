import urllib.parse
import urllib.request
from datetime import datetime, timedelta
import os
import json
import glob

D__M__Y = "%d.%m.%Y"


def parse_date(date_string):
    """
    Parses date string to date object
    :param date_string: format "%d.%m.%Y"
    :return: date object
    """
    return datetime.strptime(date_string, D__M__Y)


def to_interval(start_date, end_date):
    """
    Convert date range to closed interval
    :param start_date:
    :param end_date:
    :return:
    """
    if start_date <= end_date:
        return [start_date + timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]
    return []


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def to_unix(python_date):
    """
    Convert python date to unix time stamp
    :param python_date:
    :return:
    """
    return int(python_date.timestamp())


def to_python(unix_date):
    """
    Convert unix timestamp to python date
    :param unix_date:
    :return:
    """
    return datetime.fromtimestamp(int(unix_date))


def to_date_string(python_date):
    """
    Convert python date to human-readable date
    :param python_date:
    :return:
    """
    return python_date.strftime('%Y%m%d')


def fetch_historical_data(key, start, end, loc):
    """
    Download json data for single day
    :param loc: location with lat and lon as tuple
    :param end: end date in unix format
    :param start: start date in unix format
    :param key: api key
    :return:
    """
    base_url = 'https://history.openweathermap.org/data/2.5/history/city?'
    arguments = dict(appid=key, units='metric', lat=loc[0], lon=loc[1], type='hour', start=start, end=end)
    request_url = base_url + urllib.parse.urlencode(arguments)

    with urllib.request.urlopen(request_url) as request:
        return request.read().decode("utf8")


def fetch_future_data(key, loc, **kwargs):
    """
    Download json data for 4 days into the future
    :param loc: location with lat and lon as tuple
    :param key: api key
    :return:
    """
    base_url = 'https://pro.openweathermap.org/data/2.5/forecast/hourly?'
    arguments = dict(appid=key, units='metric', lat=loc[0], lon=loc[1])
    request_url = base_url + urllib.parse.urlencode(arguments)

    # use optionally provided url for accuweather
    if 'url' in kwargs:
        request_url = kwargs.get('url')

    with urllib.request.urlopen(request_url) as request:
        return request.read().decode("utf8")


def get_location_by_name(key, query, index):
    """
    Get location by given name
    :param index: which city from the list if names match
    :param key:
    :param query:
    :return: tuple with lat, lon
    """
    base_url = 'http://api.openweathermap.org/geo/1.0/direct?'
    arguments = dict(q=query, appid=key, limit='5')
    request_url = base_url + urllib.parse.urlencode(arguments)

    with urllib.request.urlopen(request_url) as request:
        # get data, load into json and use city from index
        city_loc = json.loads(request.read().decode("utf8"))[int(index)]
        return city_loc['lat'], city_loc['lon']


def exists(file):
    """
    checks whether file exists
    :param file:
    :return:
    """
    return os.path.exists(file) and os.path.isfile(file)


def list_weather_data_files(data_dir, tense):
    """
    Reads all json file names from given dir into list
    :return:
    """
    weather_data = []

    if tense == 'history':
        file_pattern = f'{data_dir}/*-hist.json'
    elif tense == 'accu':
        file_pattern = f'{data_dir}/*-accu.json'
    else:
        file_pattern = f'{data_dir}/*-fut.json'

    for json_file_weather in glob.glob(file_pattern):
        weather_data.append(json_file_weather)
    return weather_data


def load_weather_json(file, tense):
    """
    Reads json file and loads it using json lib
    :param tense: history or future
    :param file: file location
    :return:
    """
    f = open(file, 'r')
    contents = f.read()
    f.close()
    if tense == 'history':
        return json.loads(contents)['list']
    else:
        return json.loads(contents)


def get_params(hour_data, weather_str):
    """
    Filters out the relevant data, optionally assigns -1 to missing parameters
    :param weather_str:
    :param hour_data: which hour
    :return:
    """
    # optionally missing params
    if 'rain' in hour_data.keys():
        rain = hour_data['rain']['1h']
    else:
        rain = -1

    if 'snow' in hour_data.keys():
        snow = hour_data['snow']['1h']
    else:
        snow = -1

    return [
        weather_str.split('-')[1].replace(',', ' '),  # location name, replace comma with space
        hour_data['dt'],  # date in unix format
        hour_data['main']['temp'],  # temperature
        hour_data['wind']['speed'],  # wind speed
        hour_data['wind']['gust'],  # gust speed
        hour_data['clouds']['all'],  # cloudiness
        hour_data['weather'][0]['id'],  # weather condition id
        hour_data['weather'][0]['main'],  # weather description
        rain,  # rain in the last hour
        snow  # snow in the last hour
    ]


def get_params_accu(data, weather_str):
    """
    gets relevant parameters from the accuweather json file
    :param data: json data
    :param weather_str:
    :return:
    """
    day_data = []

    for hour in data:
        day_data.append([
            weather_str.split('-')[1].replace(',', ' '),
            hour['EpochDateTime'],  # date in unix format
            hour['Temperature']['Value'],  # temperature
            hour['Wind']['Speed']['Value'],  # wind speed
            hour['WindGust']['Speed']['Value'],  # gust speed
            hour['CloudCover'],  # cloudiness
            -1,  # not provided by accuweather
            hour['IconPhrase'],  # weather description
            hour['Rain']['Value'],  # rain in the last hour
            hour['Snow']['Value']  # snow in the last hour
        ])
    return day_data


def get_city_code(key, country, city):
    """
    get city code of specified city. because of limited calls, don't use if not necessary
    :param key: api key
    :param country:
    :param city:
    :return:
    """
    base_url = 'http://dataservice.accuweather.com/locations/v1/cities/' + country + '/search?'
    arguments = dict(apikey=key, details='true', metric='true', q=city)
    request_url = base_url + urllib.parse.urlencode(arguments)

    with urllib.request.urlopen(request_url) as search_address:
        data = json.loads(search_address.read().decode())
        location_key = data[0]['Key']
        return location_key


def fetch_future_accu(key, acc_city_code):
    """
    gets weather predictions from accuweather
    :param key: api key
    :param acc_city_code: accuweather city code
    :return:
    """
    base_url = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' + acc_city_code + '?'
    arguments = dict(apikey=key, language='en-us', details='true', metric='true')
    request_url = base_url + urllib.parse.urlencode(arguments)

    return fetch_future_data('', ('', ''), url=request_url)
