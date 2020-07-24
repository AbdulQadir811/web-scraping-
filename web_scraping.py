from lxml import html
import requests
import csv
import pandas as pd
import re

import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup


def my_function(link, csv_file_name):
    page = requests.get(link)
    tree = html.fromstring(page.content)
    # print("Hello")

    # buyers = tree.xpath('//div[@title="buyer-name"]/text()')
    # This will create a list of prices  title="Houses for sale in Mehmoodabad"
    # buyers = tree.xpath('//a[@title="Houses for sale in Mehmoodabad"]/text()')

    # Location
    location = tree.xpath(
        '//div[@class="_162e6469"]/text()')  # <div class="_7ac32433" title="Brand New Triple Storey House For Sale At Prime Location"><div class="_1e0ca152 _026d7bff"><div><div class="cd6d5974 _532a0352"><div class="c4fc20ba"><span class="c2cc9762" aria-label="Listing currency">PKR</span><span class="_14bafbc4"></span><span class="f343d9ce" aria-label="Listing price">80 Lakh</span></div></div></div></div></div>
    # price
    prices = tree.xpath('//span[@class="f343d9ce"]/text()')

    description = tree.xpath('//div[@class="ee550b27"]/text()')

    ################################################title start #######################################################
    title_list = []

    for x in range(10):
        title = tree.xpath('//div[@class="_1d4d62ed _01e2e273 c7b81b5c"]')[x]  # _1d4d62ed  _1d4d62ed _01e2e273 c7b81b5c
        title = title.xpath('./div[@class="_7ac32433"]/@title')
        title_list.append(title)
        # print(title)
        # print (x)

    for x in range(15):
        try:
            title = tree.xpath('//div[@class="_1d4d62ed"]')[x]  # _1d4d62ed  _1d4d62ed _01e2e273 c7b81b5c
            title = title.xpath('./div[@class="_7ac32433"]/@title')
            title_list.append(title)
            # print(title)
            # print (x)
        except:
            print("An exception occurred")
            break

    ######################################Title End#############################################

    ######################################Area Strat############################################

    data = requests.get(link)
    soup = BeautifulSoup(data.text, 'html.parser')
    data = []
    for span in soup.find_all('div', {'class': '_1e0ca152 _026d7bff'}):
        values = [span.text for span in span.find_all('span')]
        data.append(values)
    x = 1
    x = len(data) / 2
    # print()
    y = int(x)
    # print(len(data))
    # print(type(y))
    x = 1
    area_list = []
    for i in range(len(data)):
        if (i == y):
            break
        else:
            z = data[x][0]
            x = x + 2
            area_list.append(z)
            # print(i)

    ########################## AREA END########################################3

    for x in range(15):
        # print ("dictionary")
        my_dict = {'Title': title_list[x], 'Price': prices[x], 'Description': description[x]}

    name_dict = {
        'Title': title_list,
        'location': location,
        'Area': area_list,
        'Price': prices,
        'Description': description,
    }

    df = pd.DataFrame(name_dict)

    df.to_csv(csv_file_name)


def parseint(string):
    m = re.search(r"(\d*\.?\d*)", string)
    return m.group() if m else None


def data_fetching(csv_file_name):
    data = pd.read_csv(csv_file_name)
    price = data['Price']
    area = data['Area']

    price_list = []
    area_list = []

    for i in price:
        if (i.find('crore')):  # converting crore to lakh so that ican plot the gragp correctly
            # print(i)
            x = float(parseint(i))
            x = x * 100
            # print(type(x))
            price_list.append(x)
        else:
            x = parseint(i)
            price_list.append(x)

    for i in area:
        if (i.find('Kanal')):  # converting Kanal to Marla so that ican plot the gragp correctly
            # print(i)
            x = float(parseint(i))
            x = x * 20
            # print(type(x))
            area_list.append(x)
        else:
            x = parseint(i)
            area_list.append(x)

    return price_list, area_list


def plot_graph(price_list, area_list):
    plt.xlabel("Area")
    plt.ylabel("Price")
    plt.title("Price Area Graph")
    plt.plot( area_list,price_list)

    plt.show()


if __name__ == "__main__":
    csv_file_name = "lahore_zameen.csv"
    my_function('https://www.zameen.com/Homes/Lahore-1-1.html', csv_file_name)

    csv_file_name = "multan_zameen.csv"
    my_function('https://www.zameen.com/Homes/Multan-15-1.html', csv_file_name)
    x = data_fetching(csv_file_name)
    plot_graph(x[0], x[1])
    print(x[0]) #price in lakhs
    print(x[1]) #price area in canals

