# FetchWeather
fetches weather from past and future, inserts relevant information into csv database

## getWeatherPeriod
|name|short|explanation|default|                                      
|----|-----|-----------|-------|                                                    
|`--key`|`-k`|The API key for OWM|env|                                              
|`--directory`|`-d`|Directory for JSON files|out|                                   
|`--start`|`-s`|start date|01.10.2022|                                              
|`--end`|`-e`|end date|05.10.2022|                                                  
|`--name`|`-n`|location name|Odense,DK|                                             
|`--index`|`-i`|index of cities from list used|`0`|  

## convertToCSV
| name          | short | explanation                  | default      |                                      
|---------------|-------|------------------------------|--------------|                                                                                                
| `--directory` | `-d`  | Directory for JSON files     | out          |
| `--out`       | `-o`  | CSV Database file name       | training.csv |
| `--tense`     | `-t`  | Use data from future or past | history      |
