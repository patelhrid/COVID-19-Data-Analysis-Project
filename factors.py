"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19
Instructions
============
This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""


class Unemployment:
    """Unemployment factor class"""

    def __init__(self):
        """Initializer"""
        raise NotImplementedError

    def extract(self, country_name: str):
        """Extract the data from the .csv file"""
        raise NotImplementedError


class ConsumerPriceIndex:
    """Consumer Price Index factor class"""

    def extract(self, country_name: str, file_name: str) -> int:
        """Extract the data from the .csv file"""
        with open(file_name) as file:
            file_text = file.read()
            file_lst = file_text.split('\"')

        for x in file_lst:
            if x == '' or x == ',' or x == ',\n\n':
                file_lst.remove(x)

        table = []
        for _ in range(46):
            table.append([])

        x = 0
        for k in table:
            while file_lst[x] != ',\n':
                k.append(file_lst[x])
                x += 1
            if file_lst[x] == ',\n':
                x += 1

        for x in table:
            if x[0] == country_name:
                return x[-1]
