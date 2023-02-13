from datetime import datetime
import functions
import argparse
import os

parser = argparse.ArgumentParser(
    prog='fetchWeatherByDate',
    description='Fetches Weather by Date into a json file from OWM',
    epilog='Text at the bottom of help')

parser.add_argument('-k', '--key', default=os.getenv('ACC_KEY'), dest='api_key')
parser.add_argument('-d', '--directory', default="out", dest='out_dir')
parser.add_argument('-n', '--name', default="Odense,DK", type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)

    functions.create_dir(args.out_dir)

    location = args.name.split(',')
    if args.name == 'Odense,DK':
        city_code = '126312'
    elif args.name == 'Svendborg,DK':
        city_code = '126179'
    else:
        city_code = functions.get_city_code(args.api_key, location[1], location[0])

    print(city_code)

    file_name = f'{args.out_dir}/{functions.to_date_string(datetime.today())}-{args.name}-accu.json'

    if functions.exists(file_name):
        print(f'Already downloaded: {functions.to_date_string(datetime.today())}')
    else:
        print(f"Downloading: {functions.to_date_string(datetime.today())} ...")

        with open(file_name, 'a') as f:
            f.write(functions.fetch_future_accu(args.api_key, city_code))
