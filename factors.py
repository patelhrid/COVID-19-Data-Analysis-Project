"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""
import csv
import scrapy
from formulas import percentage

COUNTRIES = ['Canada', 'United States', 'China', 'Japan', 'Russia', 'France',
             'United Arab Emirates', 'United Kingdom']


class IncorrectCountryError(Exception):
    """Exception raised when data for a country is not available in the datasets."""

    def __str__(self) -> str:
        """Return a string representation of this error."""
        return 'Data on this country is not available'


class FoodInsecurity(scrapy.Spider):
    """The level of food insecurity """
    name = 'food insecurity'
    urls = ['https://impact.economist.com/sustainability/project/food-security-index/Index']

    def parse(self, response, **kwargs) -> None:
        """TODO"""
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }


class Unemployment:
    """The unemployment rate for a country in 2020.

    Instance Attributes:
        - percent: the percentage of unemployment rate
    """
    percent: float

    def __init__(self) -> None:
        """Initialize values for unemployment rate."""
        self.percent = 0.0

    def extract_data(self, filename: str, country: str) -> None:
        """Update the percent of unemployment for country in filename."""


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

    def calculate_average_cpi(self, filename: str, country: str) -> float:
        """Return and update the average CPI of country from filename."""

    def calculate_percent(self, filename: str, country: str) -> None:
        """Update the CPI percent for country from filename."""


# Hrid
class ConsumerPriceIndex:
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
        for _ in range(46):
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
            - filename == 'datasets/owid-covid-data - confirmed_cases.csv'
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

    def calculate_percent(self, country: str) -> None:
        """Update the percent of total cases of country from ppln_file.

        Preconditions:
            - the second last row for each country is the population in 2020
        """
        if country not in self.all_cases:
            raise IncorrectCountryError
        else:
            self.percent = percentage(self.all_cases[country], ppln(country))

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


def ppln(country: str) -> int:
    """Return the population of the country from a dataset.

    Preconditions:
        - the second last row for each country is the population in 2020
    """
    filename = 'datasets/API_SP.POP.TOTL_DS2_en_csv_v2_3358390.csv'
    total_population = 0
    with open(filename) as f:
        # skip the first 5 lines
        reader = csv.reader(f, delimiter=',')
        _ = [next(reader) for _ in range(5)]

        for row in reader:
            current_country = row[0]
            if country == current_country:
                total_population = int(row[-2])

    return total_population


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
#         'disable': ['R1705', 'C0200', 'E9998', 'E9999'],
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
