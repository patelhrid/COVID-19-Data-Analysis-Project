"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""
import csv
import json
from scrapy import Spider, Request, settings, crawler
import statistics


COUNTRIES = ['Canada', 'United States', 'China', 'Japan', 'Russia', 'France',
             'United Arab Emirates', 'United Kingdom']


class IncorrectCountryError(Exception):
    """Exception raised when data for a country is not available in the datasets."""

    def __str__(self) -> str:
        """Return a string representation of this error."""
        return 'Data on this country is not available'


class FoodInsecurity(Spider):
    """The level of food insecurity """
    name = 'FoodInsecurity'
    # req = Request("https://impact.economist.com/sustainability/project/food-security-index/Index/YoY")
    # req.replace()

    def start_requests(self) -> None:
        """Start requests"""
        urls = [
            'https://impact.economist.com/sustainability/project/food-security-index/Index/YoY'
        ]

        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs) -> None:
        """TODO"""
        with open('food_insecurity.json', 'w') as f:
            for row in response.xpath('//*[@id="yeartoyear"]//tbody/tr'):
                json.dump({
                    row.xpath('td//text()')[1].get(): row.xpath('td//text()')[10].get()
                }, f)
                f.write(', ')

    # def _fetch_parse(self, response) -> None:
    #     from scrapy.shell import inspect_response
    #     inspect_response(response, self)

    # def fetch(self, url):
        # crawler.engine.schedule(Request(url, self._fetch_parse, priority=1000))


def get_unemployment(country: str) -> int:
    """Return the population of the country from a dataset.

    # Preconditions:
    #     - the second last row for each country is the population in 2020
    """
    filename = 'datasets/API_SL.UEM.TOTL.ZS_DS2_en_csv_v2_3358447 - unemployment.csv'
    unemployment_rate = 0
    with open(filename) as f:
        # skip the first 5 lines
        reader = csv.reader(f, delimiter=',')
        _ = [next(reader) for _ in range(5)]

        for row in reader:
            current_country = row[0]
            if country == current_country:
                unemployment_rate = float(row[-2])
    
    if unemployment_rate == 0:
        raise IncorrectCountryError

    return unemployment_rate


def get_income(filename: str, country: str) -> str:
    """ Extraction """
    with open(filename) as file:
        reader = csv.reader(file)

        next(reader)

        for row in reader:
            if row[1] == country and row[5] == '2020':
                income = row[12]
                return income

def get_cpi_average(country: str) -> float:
    """Get a country's average consumer price index for food in 2020."""
    filename = 'CPI.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)

        # ACCUMULATOR cpi_value_so_far: keeps track of each month's cpi value for a country.
        cpi_value_so_far = []

        for row in reader:
            current_country = row[3]
            cpi_value = row[11]
            if country == current_country:
                list.append(cpi_value_so_far, cpi_value)
                # convert strings into floats
        int_cpi_value_so_far = [float(x) for x in cpi_value_so_far]
        # calculate the mean of all the cpi values over 12 months
        average_value = statistics.mean(int_cpi_value_so_far)
        return average_value

def get_cpi_percent(country: str) -> int:
    """Get a country's consumer price index percentage for food in 2020."""
    base_value = 100
    percent_value = get_cpi_average(country) - base_value
    return int(percent_value)

def confirmed_cases() -> dict[str, float]:
    """Update the amount of total cases for each country in filename."""
    filename = 'datasets/owid-covid-data - confirmed_cases.csv'

    # ACCUMULATOR confirmed_cases_so_far: the dictionary of confirmed cases for each country so far
    confirmed_cases_so_far = {}

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        # skip the first 8 lines
        _ = [next(reader) for _ in range(8)]

        # depending on how the graphs look, may have to use number of cases, not percent
        for row in reader:
            if row[1] != '' and row[3] == '2020-12-31' and row[4] != '' and ppln(row[2]) != 0:
                country = row[2]
                confirmed_cases = float(row[4])
                confirmed_cases_so_far[country] = percentage(confirmed_cases, ppln(country))

    return confirmed_cases_so_far


def ppln(country: str) -> int:
    """Return the population of the country from a dataset.

    # Preconditions:
    #     - the second last row for each country is the population in 2020
    """
    filename = 'datasets/API_SP.POP.TOTL_DS2_en_csv_v2_3358390.csv'
    total_population = 0
    with open(filename) as f:
        # skip the first 5 lines
        reader = csv.reader(f, delimiter=',')
        _ = [next(reader) for _ in range(5)]

        for row in reader:
            current_country = row[0]
            if country == current_country and row[-2].isdigit():
                total_population = int(row[-2])
    
    # might have to raise error in main file...
    # if total_population == 0:
    #     raise IncorrectCountryError


def percentage(numerator: int, denominator: int) -> float:  # maybe have to change
    """Calculate"""
    return round((numerator / denominator) * 100, 2)


# if __name__ == '__main__':
#     import python_ta
#
#     python_ta.check_all(config={
#         'max-line-length': 100,
#         'extra-imports': ['python_ta.contracts', 'scrapy', 'csv', 'percentage'],
#         'disable': ['R1705', 'C0200'],
#     })
#
#     import python_ta.contracts
#
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()
#
#     import doctest
#
#     doctest.testmod()
