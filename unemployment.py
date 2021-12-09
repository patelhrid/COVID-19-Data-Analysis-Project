"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19
Instructions
============
This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""


class Unemployment:
    """Consumer Price Index factor class"""

    def extract(self, country_name: str, file_name: str) -> int:
        """Extract the data from the .csv file"""
        # Reading the file
        with open(file_name) as file:
            file_text = file.read()
            file_lst = file_text.split('\"')

        # Cleaning up file_lst to remove unnecessary characters
        for x in file_lst:
            if x == '' or x == ',' or x == ',\n\n':
                file_lst.remove(x)

        # Creating the empty table for the data
        table = []
        for _ in range(267):
            table.append([])

        # Filling in the table
        x = 0
        for k in table:
            while file_lst[x] != ',\n':
                k.append(file_lst[x])
                x += 1
            if file_lst[x] == ',\n':
                x += 1

        # Finding the desired country and the CPI of 2020 for that country
        for x in table:
            if x[0] == country_name:
                return x[-1]
