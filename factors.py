"""Factors Affectd by COVID-19 that Influence Food Insecurity

Description
============

This Python module contains the functions and classes that extract and perform any necessary
calculations on the data for food insecurity levels, confirmed cases, unemployment rate,
income levels, and consumer price index for multiple countries.
"""
import csv
import json
import statistics
from scrapy import Spider, Request
import scrapy


class IncorrectCountryError(Exception):
    """Exception raised when data for a country is not available in the datasets."""

    def __str__(self) -> str:
        """Return a string representation of this error."""
        return 'Data on this country is not available'


class FoodSecurity(Spider):
    """A spider that inherits from the scrapy.Spider class and extracts data of food security
    levels in 2020 as an index.

    Instance Attributes:
        - name: the name of the spider class
        - allowed_domains: a list of domains this spider is allowed to crawl
    """
    name: str
    allowed_domains: list[str]

    def __init__(self) -> None:
        """Initialize the attributes of this spider class."""
        Spider.__init__(self, 'FoodInsecurity')
        self.allowed_domains = ['impact.economist.com']

    def start_requests(self) -> None:
        """Generate Request objects from the given urls, and instantiate Response objects to be
        passed as arguments to the parse method."""
        # The specific request url
        urls = [
            'https://impact.economist.com/sustainability/project/food-security-index/Index/YoY'
        ]

        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.Response, **kwargs) -> None:
        """Generates dictionaries mapping countries to food security indices in 2020."""
        for row in response.xpath('//*[@id="yeartoyear"]//tbody/tr'):
            yield {row.xpath('td//text()')[1].get(): row.xpath('td//text()')[10].get()}


class FoodInsecurity:
    """A class for the food insecurity index of a country.

    Instance Attributes:
        - index: a dictionary mapping countries to food insecurity index

    Representation Invariants:
        - all(self.index[country] >= 0 for country in self.index)
    """
    index: dict[str, float]

    def __init__(self) -> None:
        """Initiate the index attribute of this class as an empty dictionary."""
        self.index = {}

    def calculate_food_insecurity(self) -> None:
        """Update the food insecurity index of each country in 2020.

        Preconditions:
            - the file 'food_security.json' created from FoodSecurity is in the same directory \
                as 'main.py'

        >>> fi = FoodInsecurity()
        >>> fi.calculate_food_insecurity()
        >>> len(fi.index)
        113
        >>> fi.index['Canada']
        22.0
        """
        # Open the json file created from the scrapy spider (FoodSecurity)
        filename = 'food_security.json'
        with open(filename) as json_file:
            data = json.load(json_file)

        # Convert food security index to food insecurity index by subtracting each value from 100
        for pair in data:
            country = list(pair.keys())[0]
            self.index[country] = round(100 - float(pair[country]), 1)


def get_unemployment(country: str) -> float:
    """Return the unemployment rate of country from a dataset in 2020.

    Preconditions:
        - country is a valid country name

    >>> get_unemployment('Canada')
    9.48
    """
    filename = 'datasets/unemployment.csv'

    # 'South Korea' is stored in this dataset as 'Korea, Rep.', so reassign country to match the
    # string in the dataset and return the correct value
    if country == 'South Korea':
        country = 'Korea, Rep.'

    # ACCUMULATOR unemployment_rate: the running unemployment of country so far
    unemployment_rate = 0

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')

        # Skip the first 5 lines
        _ = [next(reader) for _ in range(5)]

        for row in reader:
            current_country = row[0]
            if country == current_country:
                unemployment_rate = float(row[-2])

    # If no unemployment rate was found for country, raise an error
    if unemployment_rate == 0:
        raise IncorrectCountryError

    return unemployment_rate


def get_income_usd(country: str) -> float:
    """Return the average annual income of country in 2020, in US Dollars.

    Preconditions:
        - country is a valid country name

    >>> get_income_usd('Canada')
    56674.16
    """
    # A list of countries in the Euro Zone, who use Euros as their currency (country name in the
    # dataset would be 'Euro Zone')
    euro_zone = ['Belgium', 'Germany', 'Ireland', 'Spain', 'France', 'Italy', 'Luxembourg',
                 'Netherlands', 'Austria', 'Portugal', 'Finland', 'Greece', 'Slovenia', 'Cyprus',
                 'Malta', 'Slovakia', 'Estonia', 'Latvia', 'Lithuania']

    # Return the income level of the USA in USD, without needing to convert the value
    # 'South Korea' is stored in this dataset as 'Korea', so reassign country to match the string
    # in the dataset and return the correct value
    if country == 'United States':
        return get_income(country)
    elif country in euro_zone:
        country = 'Euro Zone'
    elif country == 'South Korea':
        country = 'Korea'

    filename = 'datasets/exchange_rates.csv'
    with open(filename) as file:
        reader = csv.reader(file)

        # Skip the header
        next(reader)

        for row in reader:
            if row[1] == country:
                usd_income = get_income(country) / float(row[4])
                return round(float(usd_income), 2)

    # If no income level was found for country, raise an error
    raise IncorrectCountryError


def get_income(country: str) -> float:
    """Return the average annual income of country in 2020, in country's currency.

    Preconditions:
        - country is a valid country name

    >>> get_income('Canada')
    72259.55
    """
    filename = 'datasets/income.csv'

    with open(filename) as file:
        reader = csv.reader(file)

        # Skip the header
        next(reader)

        for row in reader:
            if row[1] == country and row[5] == '2020':
                income = row[12]
                return round(float(income), 2)

    # If no income level was found for country, return 0, so that an error will be raised in
    # get_income_usd
    return 0


def get_cpi(country: str) -> float:
    """Return the average consumer price index for food of country in 2020.

    Preconditions:
        - country is a valid country name

    >>> get_cpi('Canada')
    107.02
    """
    filename = 'datasets/cpi.csv'

    # 'South Korea' is stored in this dataset as 'Republic of Korea', so reassign country to
    # match the string in the dataset and return the correct value
    if country == 'South Korea':
        country = 'Republic of Korea'

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')

        # Skip the header
        next(reader)

        # ACCUMULATOR cpi_value_so_far: keeps track of each month's CPI value for a country
        cpi_value_so_far = []

        for row in reader:
            current_country = row[3]
            cpi_value = row[11]
            # 'United States' is stored in this dataset as 'United States of America', so
            # check if country is in current_country
            if country in current_country:
                cpi_value_so_far.append(float(cpi_value))

        # If no cpi was found for country, raise an error
        if cpi_value_so_far == []:
            raise IncorrectCountryError

        # Calculate the mean of all the CPI values over 12 months
        average_value = statistics.mean(cpi_value_so_far)
        return round(average_value, 2)


def get_confirmed_cases() -> dict[str, float]:
    """Return a dictionary mapping countries to their amount of COVID-19 cases as a percent of
    the population.

    >>> cases = get_confirmed_cases()
    >>> cases['Canada']
    1.55
    """
    filename = 'datasets/confirmed_cases.csv'

    # ACCUMULATOR confirmed_cases_so_far: the dictionary of confirmed cases for each country so far
    confirmed_cases_so_far = {}

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')

        # Skip the first 8 lines
        _ = [next(reader) for _ in range(8)]

        for row in reader:
            if row[1] != '' and row[3] == '2020-12-31' and row[4] != '' and ppln(row[2]) != 0:
                country = row[2]
                confirmed_cases = float(row[4])
                confirmed_cases_so_far[country] = percentage(confirmed_cases, ppln(country))

    return confirmed_cases_so_far


def ppln(country: str) -> int:
    """Return the population of the country from a dataset.

    Preconditions:
        - country is a valid country name

    >>> ppln('Canada')
    38005238
    """
    filename = 'datasets/population.csv'

    # 'South Korea' is stored in this dataset as 'Korea, Rep', so reassign country to match the
    # string in the dataset and return the correct value
    if country == 'South Korea':
        country = 'Korea, Rep.'

    # ACCUMULATOR total_population: the population of country in 2020 so far
    total_population = 0

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')

        # Skip the first 5 lines
        _ = [next(reader) for _ in range(5)]

        for row in reader:
            current_country = row[0]
            if country == current_country and row[-2].isdigit():
                total_population = int(row[-2])

    return total_population


def percentage(numerator: float, denominator: float) -> float:
    """Return the percentage value, given numerator and denominator, rounded to 2 decimal places.

    Preconditions:
        - denominator != 0

    >>> percentage(90, 100)
    90.0
    """
    return round((numerator / denominator) * 100, 2)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'scrapy', 'csv', 'json', 'statistics'],
        'allowed-io': ['FoodInsecurity.calculate_food_insecurity', 'get_unemployment',
                       'get_income_usd', 'get_income', 'get_cpi',
                       'get_confirmed_cases', 'ppln'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9998'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
