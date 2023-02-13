import argparse
import json
import os
from datetime import datetime, timedelta
import functions

D__M__Y = "%d.%m.%Y"

parser = argparse.ArgumentParser(
    prog='fetchWeatherByDate',
    description='Fetches Weather by Date into a json file from OWM',
    epilog='Text at the bottom of help')

parser.add_argument('-k', '--key', default=os.getenv('OWM_KEY'), dest='api_key')
parser.add_argument('-d', '--directory', default="out", dest='out_dir')
parser.add_argument('-s', '--start', default="01.10.2022", type=str)
parser.add_argument('-e', '--end', default="05.10.2022", type=str)
parser.add_argument('-n', '--name', default="Odense,DK", type=str)
parser.add_argument('-i', '--index', default="0", type=str)
parser.add_argument('-t', '--tense', default="history", type=str)  # history/future

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)

    functions.create_dir(args.out_dir)

    location = functions.get_location_by_name(args.api_key, args.name, args.index)

    if args.tense == 'history':
        dates = functions.to_interval(functions.parse_date(args.start), functions.parse_date(args.end))
        for date in dates:
            file_name = f'{args.out_dir}/{functions.to_date_string(date)}-{args.name}-hist.json'

            if functions.exists(file_name):
                print(f'Already downloaded: {functions.to_date_string(date)}')
                continue

            print(f"Downloading: {functions.to_date_string(date)} ...")

            end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
            json_str = functions.fetch_historical_data(args.api_key, functions.to_unix(date),
                                                       functions.to_unix(end_of_day), location)

            f = open(file_name, 'w')
            f.write(json_str)
            f.close()
    else:
        future_data = functions.fetch_future_data(args.api_key, location)
        future_data_json = json.loads(future_data)['list']

        # get start date
        start = functions.to_python(future_data_json[0]['dt'])
        # end date
        end = start + timedelta(days=3)

        hours_in_forecast_days = [24 - start.hour, 24, 24, end.hour]

        dates = functions.to_interval(start, end)
        counter = 1  # used hours from json
        for i, date in enumerate(dates):
            file_name = f'{args.out_dir}/{functions.to_date_string(date)}-{args.name}-fut.json'

            if functions.exists(file_name):
                print(f'Already downloaded: {functions.to_date_string(date)}')
                continue

            print(f"Downloading: {functions.to_date_string(date)} ...")

            with open(file_name, 'a') as f:
                f.write('[')
                for j in range(hours_in_forecast_days[i]):
                    f.write(json.dumps(future_data_json[counter]))  # write data for one hour
                    if j != hours_in_forecast_days[i] - 1:
                        f.write(',')  # add comma between hours
                    counter += 1
                f.write(']')
