"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""
import csv
import json
from scrapy import Spider, Request
import statistics
from scrapy.crawler import CrawlerProcess


COUNTRIES = ['Canada', 'United States', 'China', 'Japan', 'Australia', 'France',
             'United Arab Emirates', 'United Kingdom']


class IncorrectCountryError(Exception):
    """Exception raised when data for a country is not available in the datasets."""

    def __str__(self) -> str:
        """Return a string representation of this error."""
        return 'Data on this country is not available'


class FoodSecurity(Spider):
    """A spider that extracts data of food security levels in 2020 as a percentage."""
    name = 'FoodSecurity'
    allowed_domains = ['impact.economist.com']

    def start_requests(self) -> None:
        """Generate Request objects from the given urls, and instantiate Response objects to be
        passed as arguments to the parse method."""
        urls = [
            'https://impact.economist.com/sustainability/project/food-security-index/Index/YoY'
        ]

        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs) -> None:
        """Generates dictionaries mapping countries to food security levels in 2020."""
        for row in response.xpath('//*[@id="yeartoyear"]//tbody/tr'):
            yield {row.xpath('td//text()')[1].get(): row.xpath('td//text()')[10].get()}


class FoodInsecurity:
    """A class for the amount of food insecurity of a country."""
    percentages: dict[str, float]

    def __init__(self) -> None:
        self.percentages = {}

    def calculate_food_insecurity(self) -> None:
        """Return the food insecurity levels of each country available in the dataset as a
        percentage."""
        file = open('food_security.json')
        data = json.load(file)

        # ACCUMULATOR food_insecurity_so_far: the running dictionary mapping country to food insecurity
        # food_insecurity_so_far = {}

        for dict in data:
            country = list(dict.keys())[0]
            self.percentages[country] = round(100 - float(dict[country]), 1)

        # return self.percentages


def get_food_insecurity() -> dict[str, float]:
    """Return the food insecurity levels of each country available in the dataset as a
    percentage."""
    process = CrawlerProcess(settings={'FEEDS': {'food_security.json': {'format': 'json',
                                                                        'overwrite': True}, },
                                       'LOG_ENABLED': False})
    process.crawl(FoodSecurity)
    process.start()

    file = open('food_security.json')
    data = json.load(file)

    # ACCUMULATOR food_insecurity_so_far: the running dictionary mapping country to food insecurity
    food_insecurity_so_far = {}

    for dict in data:
        country = list(dict.keys())[0]
        food_insecurity_so_far[country] = round(100 - float(dict[country]), 1)

    return food_insecurity_so_far


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


def get_income_usd(country: str) -> float:
    """ Convert the income per capita of the country into US Dollars

    >>> get_income_usd('Canada')
    56674.16
    """
    if country == 'United States':
        return get_income(country)

    filename = 'datasets/RprtRateXchg_20201231_20201231.csv'
    with open(filename) as file:
        reader = csv.reader(file)

        next(reader)

        for row in reader:
            if row[1] == country:
                usd_income = get_income(country) / float(row[4])
                return round(float(usd_income), 2)

    raise IncorrectCountryError


def get_income(country: str) -> float:
    """ Get the average annual income per captia of a country

    >>> get_income('Canada')
    72259.55
    """
    filename = 'datasets/AV_AN_WAGE_30112021180149473 - income.csv'
    with open(filename) as file:
        reader = csv.reader(file)

        next(reader)

        for row in reader:
            if row[1] == country and row[5] == '2020':
                income = row[12]
                return round(float(income), 2)


def get_cpi_percent(country: str) -> int:
    """Get a country's consumer price index percentage for food in 2020."""
    base_value = 100
    percent_value = get_cpi_average(country) - base_value
    return int(percent_value)


def get_cpi_average(country: str) -> float:
    """Get a country's average consumer price index for food in 2020."""
    filename = 'datasets/FAOSTAT_data_12-10-2021.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

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


def get_confirmed_cases() -> dict[str, float]:
    """Return a dictionary mapping countries to their amount of COVID-19 cases as a percent of
    the population."""
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

    return total_population


def percentage(numerator: float, denominator: float) -> float:  # maybe have to change
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
