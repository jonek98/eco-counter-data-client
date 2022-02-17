# -*- coding: utf-8 -*-

import requests
import xlwt
from xlwt import Workbook

# Sites links
URL_STATIONS = "https://www.eco-visio.net/api/aladdin/1.0.0/pbl/publicwebpageplus/6113?withNull=true"
URL_STATION_VALUES = "https://www.eco-visio.net/api/aladdin/1.0.0/pbl/publicwebpageplus/data/{station_id}"


# Data Intervals
class Interval:
    DAYS = 4
    WEEKS = 5
    MONTHS = 6


# Load all of the stations - once is fine
def load_stations():
    return requests.get(URL_STATIONS).json()


# Load station values for stations from exact period
def load_station_values(station, date_from='01/01/2021', date_to='31/12/2021', interval=Interval.MONTHS):
    station_id = station['idPdc']

    params = {
        "idOrganisme": 6113,
        "idPdc": station_id,
        "debut": date_from,
        "fin": date_to,
        "interval": interval,
        "flowIds": ';'.join(map(lambda x: str(x['id']), station['pratique']))
        # Jakaś lista idków, nie wiem co to ale czeba
    }

    url = URL_STATION_VALUES.format(station_id=station_id)

    return requests.get(url, params=params).json()



def format_station(station):
    return {
        "id": station['idPdc'],
        "lat": station['lat'],
        "long": station['lon'],
        "name": station['nom'],
        "photo_url": station['photo'][0]['lien'],
        "organisation": station['nomOrganisme'],
        "logo_url": station['logo'],
        "total": station['total'],
        "lastDay": station['lastDay'],
    }


# Application
def main():
    stations = load_stations()

    print('Stations:')
    for i, station in enumerate(stations):
        s = format_station(station)

        print('{n}. {name} (total: {total})'.format(
            n=i + 1,
            name=s['name'],
            total=s['total'],
        ))

    print('===')
    print('Values for choosen stations:')

    first_station = stations[0]

    values = load_station_values(first_station, date_from='01/01/2018', date_to='01/01/2021')

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet2')
    sheet1.write(0, 0, 'Data')
    sheet1.write(0, 1, 'Monthly number of bikes: ')

    i = 1;
    j = 1;

    for date, value in values:
        print('{date}. {value}'.format(
            date=date,
            value=value
        ))

        sheet1.write(i, 0, date)
        sheet1.write(j, 1, value)
        i += 1
        j += 1

    wb.save('data2.xls')


main()
