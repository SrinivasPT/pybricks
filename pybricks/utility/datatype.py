import bs4
from bs4 import BeautifulSoup
import functools
import os
import re
from fastnumbers import fast_float, isfloat
import pandas as pd
import numpy as np
import sys
# sys.path.append("C:\\Users\\srini\\Anaconda3\\lib\\site-packages")


def hello_world():
    print("Hello World")


def ffloat(string):
    if string is None:
        return np.nan
    if type(string) == float or type(string) == int or type(string) == np.int64 or type(string) == np.float64:
        return string
    string = re.sub("[^0-9\.]", '', string.split(" ")[0])
    return fast_float(string, default=np.nan)


def ffloat_list(string_list):
    return list(map(ffloat, string_list))


def remove_multiple_spaces(string):
    if type(string) == str:
        return ' '.join(string.split())
    return string


def get_children(html_content):
    children = list()
    for item in html_content.children:
        if type(item) == bs4.element.Comment:
            continue
        if type(item) == bs4.element.Tag or len(str(item).replace("\n", "").strip()) > 0:
            children.append(item)

    return children


def get_table_simple(table, is_table_tag=True):
    elems = table.find_all('tr') if is_table_tag else get_children(table)
    table_data = list()
    for row in elems:
        row_data = list()
        row_elems = get_children(row)
        for elem in row_elems:
            text = elem.text.strip().replace("\n", "")
            text = remove_multiple_spaces(text)
            if len(text) == 0:
                continue
            if isfloat(text):
                text = ffloat(text)
            row_data.append(text)
        table_data.append(row_data)
    return table_data
