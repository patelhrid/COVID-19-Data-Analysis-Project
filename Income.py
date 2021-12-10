""" File for extracting data from CSV file"""

import csv


def read_country_income(filename: str, country_name: str) -> str:
    """ Extraction """
    with open(filename) as file:
        reader = csv.reader(file)

        next(reader)

        for row in reader:
            if row[1] == country_name and row[5] == '2020':
                income = row[12]
                return income
