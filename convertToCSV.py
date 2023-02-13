import argparse
import csv
import json

import functions

parser = argparse.ArgumentParser(
    prog='convertToCSV',
    description='Reads data from JSON and appends relevant data from it into a CSV file',
    epilog='Text at the bottom of help')

parser.add_argument('-d', '--directory', default="out", dest='in_dir')
parser.add_argument('-o', '--out', default="weather_dk_predictions_20230213_140001.csv", type=str)
parser.add_argument('-t', '--tense', default="history", type=str)  # history, future

params_header = ['location', 'date', 'temp', 'wind', 'gust', 'clouds', 'weatherId', 'weatherGroup', 'rain', 'snow']

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)

    count = 0
    with open(args.out, 'w', encoding='UTF8', newline='') as weather_dest:
        writer = csv.writer(weather_dest, lineterminator="\n")

        writer.writerow(params_header)  # write header

        for weather_data_str in functions.list_weather_data_files(args.in_dir, args.tense):
            print(weather_data_str)
            weather_data_json = functions.load_weather_json(weather_data_str,
                                                            args.tense)  # load contents from json file

            if args.tense == 'accu':
                params = functions.get_params_accu(weather_data_json, weather_data_str)
                for hour_params in params:
                    writer.writerow(hour_params)  # write data for every hour of the day
                    count = count + 1

            else:
                for hour in range(len(weather_data_json)):
                    params = functions.get_params(weather_data_json[hour],
                                                  weather_data_str)  # get relevant data from json
                    writer.writerow(params)  # write data for every hour of the day
                    count = count + 1

    print(f"Written {count} records.")
