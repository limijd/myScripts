#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint: disable=C0103,W0703,R0902,R1711,R0912,R0914,R0911

import os
import sys
import argparse
import logging
import requests
from contextlib import closing
import codecs
import json
import urllib.request, json 
from datetime import datetime
import time
from prettytable import PrettyTable

def load_api_key():
    fn = "~/.configs.secure/owm.key.json"
    try:
        fp = open(os.path.expanduser(fn), "r")
    except:
        logging.error("Failed to open config file which contains the OWM API key: %s",  fn)
        sys.exit(1)
    js = json.load(fp)
    fp.close()
    return js["API_key"]

def load_home_loc():
    fn = "~/.configs.secure/homeloc.json"
    try:
        fp = open(os.path.expanduser(fn), "r")
    except:
        logging.error("Failed to open config file which contains the home location: %s",  fn)
        sys.exit(1)
    js = json.load(fp)
    fp.close()
    return js["homeloc"]


home_loc = load_home_loc()
beach_pacific_city = ("Pacific City Beach", "45.21", "-123.97")
beach_sunset = ("Sunset Beach", "46.10", "-123.94")
beach_cannon = ("Cannon Beach", "45.89", "-123.96")
beaches = (beach_pacific_city, beach_sunset, beach_cannon)

GOOD_WIND = 9
GOOD_WIND_GUST = 14


class OWM_reader:
    def __init__(self, key):
        self.key = key

    def getData(self, lat, lon, excl):
        owm_url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=%s&appid=%s&units=imperial"%(lat,lon, excl,self.key)
        with urllib.request.urlopen(owm_url) as url:
            data = json.loads(url.read().decode())
            return data

    def showForcast(self, place, data, weo=False):
        daily = data["daily"]
        days = {}
        for d in daily:
            utc_sec = int(d["dt"])
            dt = datetime.fromtimestamp(utc_sec)
            temp = d["temp"]["day"]
            wind = d["wind_speed"]
            windg = d["wind_gust"]
            weather = d["weather"][0]["main"]
            days[utc_sec] = [dt, temp, wind, weather, windg]
    
        keys = list(days.keys())
        keys.sort()

        print("\n")
        print(place)
        x = PrettyTable()

        fields = ["metric/day"]
        for k in keys:
            day = days[k][0].strftime("%m/%d")
            weekdays=["Mon","Tue", "Wed", "Thu","Fri", "Sat", "Sun"]
            wd = days[k][0].weekday()
            if weo and not wd in [5,6]:
                continue
            fields.append("%s(%s)"%(day, weekdays[wd]))
        x.field_names = fields

        rowweather = ["main weather"]
        for k in keys:
            wd = days[k][0].weekday()
            if weo and not wd in [5,6]:
                continue
            rowweather.append(days[k][3])
        x.add_row(rowweather)

        row_temp = ["temperature(F)"]
        for k in keys:
            wd = days[k][0].weekday()
            if weo and not wd in [5,6]:
                continue
            row_temp.append(days[k][1])
        x.add_row(row_temp)

        row_wind= ["wind speed(MPH)"]
        for k in keys:
            wd = days[k][0].weekday()
            if weo and not wd in [5,6]:
                continue
            row_wind.append(days[k][2])
        x.add_row(row_wind)

        row_wind= ["wind gust speed(MPH)"]
        for k in keys:
            wd = days[k][0].weekday()
            if weo and not wd in [5,6]:
                continue
            row_wind.append(days[k][4])
        x.add_row(row_wind)

        print(x)

        return

def cli(args):
    owm_reader = OWM_reader(load_api_key())
    beaches_data = {}

    found_good_weather = False
    printed_good_news = False
    for bc in beaches:
        data = owm_reader.getData(bc[1], bc[2], "current,hourly,minutely,alerts")
        beaches_data[bc[0]] = data

        daily = data["daily"]
        for d in daily:
            utc_sec = int(d["dt"])
            dt = datetime.fromtimestamp(utc_sec)
            wd = dt.weekday()

            day = dt.strftime("%m/%d")
            temp = d["temp"]["day"]
            wind = d["wind_speed"]
            windg = d["wind_gust"]
            weather = d["weather"][0]["main"]

            if wd in [5,6] and wind<GOOD_WIND and windg<GOOD_WIND_GUST and weather not in ["Rain"]:
                if not printed_good_news:
                    #print("Good News! Nice weather in weekend found:")
                    print("好消息！发现周末天气状况良好！")
                    printed_good_news = True
                print("%s, %s: temp=%2.1f, wind=%2.1f, wind gust=%2.1f, weather=%s "%(bc[0], day, temp, wind, windg,weather))

    if not printed_good_news:
        #print("Unfortunately there is no nice weather in beach in coming weekend!")
        print("继续等待, 周末天气状况不佳！")

    print("\n注：海边沙滩的良好天气状况是指风速小于9MPH, 极端风速小于14MPH, 并且为多云或者晴天的天气\n")

    for bc_name, data in beaches_data.items():
        owm_reader.showForcast(bc_name, data, args.weekend_only)

    #home 
    data = owm_reader.getData(home_loc[1], home_loc[2], "current,hourly,minutely,alerts")
    owm_reader.showForcast(home_loc[0], data, args.weekend_only)

    return

def main():
    """ entry of program """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog=os.path.basename(__file__)
        , description="fetch weather data from OopenWeatherMap")
    parser.add_argument('-d', '--debug', action='store_true', help="debug mode")
    parser.add_argument('-weo', '--weekend_only', action='store_true', help="only display weekend")
    parser.set_defaults(func=cli)

    args = parser.parse_args()
    try:
        args.func
    except AttributeError:
        parser.error("too few arguments")

    if args.debug:
        logging.basicConfig(format='[alc: %(asctime)s %(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    else:
        logging.basicConfig(format='[alc: %(asctime)s %(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

    args.func(args)

main()


