#!/env/bin/python3

import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import requests
import json

url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'

def yield_curve(url):
    print("scraping")
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    table = soup.find("table", attrs= {"class":"t-chart"}) 
    rows = table.find_all('tr')
    th_td_list = []
    for row in rows[1:]:
        tds = row.findAll('td')
        th_td_data_row = []
        for td in tds:
            td_text = td.text.strip()
            #print(td_text)
            if td_text == '':
                td_text = 0.0      
            else:
                td_text = td_text
            th_td_data_row.append(td_text)
        th_td_list.append(th_td_data_row)
        #print(th_td_list)
    return th_td_list


def make_chart(data, filename):
    print("generating matplotlib chart")
    
    data = yield_curve(url)
    df = pd.DataFrame(data, columns= ["Date", "1 Mo", "2 Mo", "3 Mo", "6 Mo", "1 Yr","2 Yr","3 Yr","5 Yr","7 Yr", "10 Yr", "20 Yr", "30 Yr"])
    df = df.astype({"1 Mo": "float64", "2 Mo": "float64", "3 Mo": "float64", "6 Mo": "float64", "1 Yr": "float64", "2 Yr": "float64", "3 Yr": "float64", \
           "5 Yr": "float64", "7 Yr": "float64", "10 Yr": "float64", "20 Yr": "float64", "30 Yr": "float64"})
    dates = tuple([i for i in df["Date"].value_counts().keys()])
    values = df[["1 Yr","2 Yr","3 Yr","5 Yr","7 Yr", "10 Yr", "20 Yr", "30 Yr"]]
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(dates,values)
    ax.set_xlabel("Date")
    ax.set_ylabel("Values")
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax.set(xlim=[0, 19], title='US Tresury Yield Curve')
    ax.legend(["1 Yr","2 Yr","3 Yr","5 Yr","7 Yr", "10 Yr", "20 Yr", "30 Yr"])

    plt.savefig(f'charts/{filename}.png')
    print("completed")

def main():
    data = yield_curve(url)
    dt_now = dt.datetime.now()
    dt_fmt = dt_now.strftime("%m-%d-%y-%H%M%S")
    make_chart(np.arange(10), f'daily_chart-{dt_fmt}')

if __name__ == '__main__':
    main()