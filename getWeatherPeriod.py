import argparse
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

D__M__Y = "%d.%m.%Y"

parser = argparse.ArgumentParser(
    prog='fetchWeatherByDate',
    description='Fetches Weather by Date into a json file from OWM',
    epilog='Text at the bottom of help')

parser.add_argument('-k', '--key', default=os.getenv('API_OWM'), dest='api_key')
parser.add_argument('-d', '--directory', default="out", dest='out_dir')
parser.add_argument('-s', '--start', default="01.10.2022", type=str)
parser.add_argument('-e', '--end', default="05.10.2022", type=str)
parser.add_argument('-n', '--name', default="Odense,DK", type=str)
parser.add_argument('-i', '--index', default="0", type=str)
parser.add_argument('-t', '--tense', default="history", type=str)  # history/future


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


def fetch_future_data(key, loc):
    """
    Download json data for 4 days into the future
    :param loc: location with lat and lon as tuple
    :param key: api key
    :return:
    """
    base_url = 'https://pro.openweathermap.org/data/2.5/forecast/hourly?'
    arguments = dict(appid=key, units='metric', lat=loc[0], lon=loc[1])
    request_url = base_url + urllib.parse.urlencode(arguments)

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


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)

    create_dir(args.out_dir)
    
    location = get_location_by_name(args.api_key, args.name, args.index)

    if args.tense == 'history':
        dates = to_interval(parse_date(args.start), parse_date(args.end))
        for date in dates:
            file_name = f'{args.out_dir}/{to_date_string(date)}-{args.name}-hist.json'

            if exists(file_name):
                print(f'Already downloaded: {to_date_string(date)}')
                continue

            print(f"Downloading: {to_date_string(date)} ...")

            end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
            json_str = fetch_historical_data(args.api_key, to_unix(date), to_unix(end_of_day), location)

            f = open(file_name, 'w')
            f.write(json_str)
            f.close()
    else:
        future_data = fetch_future_data(args.api_key, location)
        future_data_json = json.loads(future_data)['list']

        # get start date
        start = to_python(future_data_json[0]['dt'])
        # end date
        end = start + timedelta(days=3)

        hours_in_forecast_days = [24 - start.hour, 24, 24, end.hour]

        dates = to_interval(start, end)
        counter = 1  # used hours from json
        for i, date in enumerate(dates):
            file_name = f'{args.out_dir}/{to_date_string(date)}-{args.name}-fut.json'

            print(start.strftime("%m/%d/%Y, %H:%M:%S"), end.strftime("%m/%d/%Y, %H:%M:%S"), date.strftime("%m/%d/%Y, %H:%M:%S"))

            if exists(file_name):
                print(f'Already downloaded: {to_date_string(date)}')
                continue

            print(f"Downloading: {to_date_string(date)} ...")

            with open(file_name, 'a') as f:
                f.write('[')
                for j in range(hours_in_forecast_days[i]):
                    f.write(json.dumps(future_data_json[counter]))  # write data for one hour
                    if j != hours_in_forecast_days[i] - 1:
                        f.write(',')  # add comma between hours
                    counter += 1
                f.write(']')

