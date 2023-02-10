#!/bin/bash

python=/usr/bin/python3

locations=("Odense,DK" "Svendborg,DK")
yesterday=$(date -d "@$(($(date +%s) - 86400))" +"%d.%m.%Y")

echo "`date`"

for location in ${locations[@]}; do
	$python ~/FetchWeather/getWeatherPeriod.py -d ~/FetchWeather/out -s 10.02.2022 -e $yesterday -n $location -k $OWM_KEY
done

# Pack everything into one CSV file
$python ~/FetchWeather/convertToCSV.py -d ~/FetchWeather/out -o ~/FetchWeather/out/weather_dk.csv -t=history

