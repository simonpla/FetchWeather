#!/bin/bash

python=/usr/bin/python3

locations=("Odense,DK" "Svendborg,DK")
yesterday=$(date -d "@$(($(date +%s) - 86400))" +"%d.%m.%Y")

for location in ${locations[@]}; do
	$python ~/FetchWeather/getWeatherPeriod.py -d ~/FetchWeather/out -s 01.10.2022 -e $yesterday -n $location -k $OWM_KEY
done
