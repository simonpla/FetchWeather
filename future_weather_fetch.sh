#!/bin/bash

python=/usr/bin/python3

# delete old predictions
rm -f ~/FetchWeather/out/*fut*

date

locations=("Odense,DK" "Svendborg,DK")
for location in "${locations[@]}"; do
	$python ~/FetchWeather/getWeatherPeriod.py -n "$location" --key "$OWM_KEY" -t future -d ~/FetchWeather/out
	$python ~/FetchWeather/getFutureAccu.py -n "$location" --key "$ACC_KEY" -d ~/FetchWeather/out
done

# Pack everything into one CSV file
$python ~/FetchWeather/convertToCSV.py -d ~/FetchWeather/out -o ~/FetchWeather/out/weather_dk_predictions_accu.csv -t=accu

# Copy to archive
cp ~/FetchWeather/out/weather_dk_predictions.csv ~/FetchWeather/out/weather_dk_predictions_accu_"$(date +"%Y%m%d_%H%M%S")".csv
