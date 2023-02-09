#!/bin/bash

python=/usr/bin/python3

locations=("Odense,DK" "Svendborg,DK")

for location in ${locations[@]}; do
	$python ~/FetchWeather/getWeatherPeriod.py -n $location --key $OWM_KEY -t future -d ~/FetchWeather/out
done
