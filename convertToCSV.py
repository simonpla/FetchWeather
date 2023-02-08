import argparse
import csv
import glob
import json

parser = argparse.ArgumentParser(
    prog='convertToCSV',
    description='Reads data from JSON and appends relevant data from it into a CSV file',
    epilog='Text at the bottom of help')

parser.add_argument('-d', '--directory', default="out", dest='in_dir')
parser.add_argument('-o', '--out', default="training.csv", type=str)

params_header = ['location', 'date', 'temp', 'wind', 'gust', 'clouds', 'weatherId', 'weatherGroup', 'rain', 'snow']


def list_weather_data_files(data_dir):
    """
    Reads all json file names from given dir into list
    :return:
    """
    weather_data = []
    for json_file_weather in glob.glob(f'{data_dir}/*.json'):
        weather_data.append(json_file_weather)
    return weather_data


def load_weather_json(file):
    """
    Reads json file and loads it using json lib
    :param file: file location
    :return:
    """
    f = open(file, 'r')
    contents = f.read()
    f.close()
    return json.loads(contents)['list']


def get_params(hour_data, ):
    """
    Filters out the relevant data, optionally assigns -1 to missing parameters
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
        weather_data_str.split('-')[1].replace(',', ' ') or -1,  # location name, replace comma with space
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


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)

    count = 0
    with open(args.out, 'w', encoding='UTF8', newline='') as weather_dest:
        writer = csv.writer(weather_dest)

        writer.writerow(params_header)  # write header

        for weather_data_str in list_weather_data_files(args.in_dir):
            weather_data_json = load_weather_json(weather_data_str)  # load contents from json file

            for hour in range(len(weather_data_json)):
                params = get_params(weather_data_json[hour])  # get relevant data from json
                writer.writerow(params)  # write data for every hour of the day
                count = count + 1

    print (f"Written {count} records.")