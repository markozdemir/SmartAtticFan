import matplotlib.pyplot as plt
import pymongo
import numpy as np
import pandas as pd
import sys
from matplotlib import cm
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
import requests
from bs4 import BeautifulSoup
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
DB = client["fan_train"]
db = DB["user"]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Invalid input\nusage: python weather_webScaper.py town_in_USA")
        exit(0)

    result_df = pd.DataFrame(columns=["time", "temp (C)", "hum"])

    town = sys.argv[1]
    day = 1
    hour = 0
    minute = 15
    res_row = 0

    for year in range(2019, 2021):
        for month in range(1, 13):
            
            print(f'{month}/{year}')

            weather_page = "https://www.timeanddate.com/weather/usa/" + str(town) + "/historic?month=" + str(month) + "&year=" + str(year)
            
            weather_resp = requests.get(weather_page)
            # print(weather_resp.text)
            print(f'\t\tResponse = {weather_resp.status_code}')

            soup = BeautifulSoup(weather_resp.content, "html.parser")
            # print(soup)
            # print(soup.find(id="wt-his"))

            rows = soup.find(id="wt-his").find("tbody").find_all("tr")

            # for given day
            for row in rows:
                cell_time = row.find("th").get_text().split()
                t = cell_time[0].split(':')

                if "am" in cell_time[1]:
                    if int(t[0]) == 12:
                        hour = 0
                if "pm" in cell_time[1]:
                    if int(t[0]) != 12:
                        hour = int(t[0]) + 12
                
                minute = int(t[1])

                cells = row.find_all("td")

                # day's temp
                temp = cells[1].get_text().split()[0]
                tempC = (int(temp) - 32) * 5.0/9.0
                
                # day's humidity
                hum = cells[5].get_text().split()[0]

                # print(cells[1].get_text().split()[0])

                # rn = cells[0].get_text()

                unix_ts = datetime.datetime(year, month, day, hour, minute).timestamp()

                result_df.loc[res_row] = [unix_ts, tempC, int(int(hum[0:-1])*0.8)]
                res_row += 1

                hum_conv = int(int(hum[0:-1])*0.8)
                db.insert({"time": unix_ts, "temp (C)": tempC, "hum": hum_conv})


    result_df.to_csv("historic_weather.csv", index=False)
