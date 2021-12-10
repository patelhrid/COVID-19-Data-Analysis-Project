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


class CPI:
    """A country's consumer price index for food in 2020.
    Instance Attributes:
        - percent: the consumer price index as a percentage for the country
    """
    # Private Instance Attributes:
    #     _average_value: the average CPI across the 12 months in 2020
    _average_value: float
    percent: float

    def __init__(self) -> None:
        """Initialize values for CPI."""
        self._average_value = 0.0
        self.percent = 0.0

    def calculate_average_cpi(self, country: str) -> float:
        """Return and update the average CPI of country from filename."""
        filename = 'FAOSTAT_data_12-9-2021.csv'
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            header = next(reader)

            # ACCUMULATOR cpi_value_so_far: keeps track of each month's cpi value for a country.
            cpi_value_so_far = []

            for row in reader:
                current_country = row[3]
                cpi_value = row[11]
                if country == current_country:
                    list.append(cpi_value_so_far, cpi_value)
                    # convert strings into integer
            int_cpi_value_so_far = [float(x) for x in cpi_value_so_far]
            # calculate the mean of all the cpi values over 12 months
            self._average_value = statistics.mean(int_cpi_value_so_far)
            return self._average_value


class Income:
    """The average income for a country in 2020.

    Instance Attributes:
        - percent: the percentage of income for a country, relative to the maximum and minimum \
            wages of the countries in COUNTRIES
    """
    _value: float
    _max_income: float
    percent: float  # percent relative to the maximum and minimum wages?

    def __init__(self) -> None:
        """Initialize values for income levels."""


class ConfirmedCases:
    """The amount of confirmed COVID-19 cases in 2020 of a country.

    Instance Attributes:
        - all_cases: countries mapping to their amount of confirmed cases
        - percent: the percentage of confirmed cases in the population
    """
    all_cases: dict[str, int]
    percent: float

    def __init__(self) -> None:
        """Initialize values for confirmed cases."""
        self.all_cases = {}
        self.percent = 0.0

        self.total_cases('datasets/owid-covid-data - confirmed_cases.csv')

    # def total_cases(self, filename: str, country: str) -> int:
    #     """Update the amount of total cases and the percent of cases for country from filename.
    #     """
    #     with open(filename) as f:
    #         # skip the first 8 lines
    #         for _ in range(0, 8):
    #             reader = csv.reader(f, delimiter=',')
    #             next(reader)
    #
    #         for row in reader:
    #             current_country = row[2]
    #             if country == current_country and row[3] == '2020-12-31':
    #                 confirmed_cases = float(row[4])
    #                 self._total_value = int(confirmed_cases)
    #
    #     return self._total_value

    def total_cases(self, filename: str) -> None:
        """Update the amount of total cases for each country in filename.

        Preconditions:
            - filename == 'datasets/owid-covid-data - confirmed_cases.csv'  # prob change
        """
        with open(filename) as f:
            reader = csv.reader(f, delimiter=',')
            # skip the first 8 lines
            _ = [next(reader) for _ in range(8)]

            for row in reader:
                if row[1] != '' and row[3] == '2020-12-31' and row[4] != '':
                    country = row[2]
                    confirmed_cases = float(row[4])
                    self.all_cases[country] = int(confirmed_cases)

        # self.total_value = amount_confirmed_cases(filename)[country]

    def calculate_percent(self, country: str, population: int) -> None:
        """Update the percent of total cases of country with population.

        Preconditions:
            - the second last row for each country is the population in 2020
        """
        if country not in self.all_cases:
            raise IncorrectCountryError
        else:
            self.percent = percentage(self.all_cases[country], population)

        # self.percent = round((self.total_value / population_all(filename)[self.country]) * 100, 2)

        # with open(filename) as f:
        #     # skip the first 5 lines
        #     for _ in range(0, 5):
        #         reader = csv.reader(f, delimiter=',')
        #         next(reader)
        #
        #     for row in reader:
        #         current_country = row[0]
        #         if country == current_country:
        #             self.percent = round(self.total_value / int(row[-2]), 2)


def percentage(numerator: int, denominator: int) -> float:  # maybe have to change
    """Calculate"""
    return round((numerator / denominator) * 100, 2)


# can probably remove these extra functions
def amount_confirmed_cases(filename: str) -> dict[str, int]:
    """Return a dictionary mapping each country to the amount of confirmed cases from filename.

    Preconditions:
        - # do we have to use python code?
    """
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        # skip the first 8 lines
        _ = [next(reader) for _ in range(8)]

        countries_so_far = {}
        for row in reader:
            country = row[2]
            if country in COUNTRIES and row[0].isalpha() and row[3] == '2020-12-31':
                confirmed_cases = float(row[4])
                total_cases_so_far = int(confirmed_cases)
                countries_so_far[country] = total_cases_so_far

    return countries_so_far


def population_all(filename: str) -> dict[str, int]:
    """Return the population of each country from filename.

    Preconditions:
        - each country in COUNTRIES is in filename
        - the second last row for each country is the population in 2020
    """
    with open(filename) as f:
        # skip the first 5 lines
        reader = csv.reader(f, delimiter=',')
        _ = [next(reader) for _ in range(5)]

        countries_so_far = {}
        for row in reader:
            country = row[0]
            if country in COUNTRIES:
                countries_so_far[country] = int(row[-2])

    return countries_so_far


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
