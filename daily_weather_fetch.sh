#!/bin/bash

python=/usr/bin/python3

locations=("Odense,DK" "Svendborg,DK")
yesterday=$(date --date="yesterday" +"%d.%m.%Y")

for location in ${locations[@]}; do
	$python ~/FetchWeather/getWeatherPeriod.py -d out -s 01.10.2022 -e $yesterday -n $location -k $OWM_KEY
done
