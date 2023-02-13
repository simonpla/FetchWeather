# FetchWeather

fetches weather from past and future, inserts relevant information into csv database

## getWeatherPeriod

| name          | short | explanation                         | default    |                                      
|---------------|-------|-------------------------------------|------------|                                                    
| `--key`       | `-k`  | The API key for OWM                 | env        |                                              
| `--directory` | `-d`  | Directory for JSON files            | out        |                                   
| `--start`     | `-s`  | start date. irrelevant for forecast | 01.10.2022 |                                              
| `--end`       | `-e`  | end date. irrelevant for forecast   | 05.10.2022 |                                                  
| `--name`      | `-n`  | location name                       | Odense,DK  |                                             
| `--index`     | `-i`  | index of cities from list used      | `0`        |  
| `--tense`     | `-t`  | Use data from future or past        | history    |

## convertToCSV

| name          | short | explanation                          | default      |                                      
|---------------|-------|--------------------------------------|--------------|                                                                                                
| `--directory` | `-d`  | Directory for JSON files             | out          |
| `--out`       | `-o`  | CSV Database file name               | training.csv |
| `--tense`     | `-t`  | Use data from future or past or accu | history      |

## getFutureAccu

| name     | short | explanation              | default   |                                      
|----------|-------|--------------------------|-----------|                                                                                                
| `--key`  | `-k`  | API key for Accuweather  | env       |
| `--out`  | `-o`  | Directory for JSON files | out       |
| `--name` | `-n`  | location name            | Odense,DK |