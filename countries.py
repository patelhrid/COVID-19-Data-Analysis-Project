"""Countries Affected by COVID-19 and their Attributes

Description
============

This Python module contains a class representing a country with several instance attributes
representing the different factors we will be analyzing.
"""
from factors import ppln, get_unemployment, get_cpi, get_income_usd, get_confirmed_cases, \
    FoodInsecurity, IncorrectCountryError


class Country:
    """A class representing a country, along with several factors related to the
    pandemic.

    Instance Attributes:
        - name: the name of the country
        - population: the total population of the country
        - food_insecurity: the food insecurity index (a score out of 100 based on several \
            indicators from the Global Food Security Index)
        - confirmed cases: the amount of confirmed COVID-19 cases as a percent of the population
        - unemployment: the unemployment rate of the country, as a percentage
        - cpi: the consumer price index for food
        - income: the average income of the country, in USD

    Representation Invariants:
        - self.name != ''
        - self.population >= 0
        - 0 <= self.food_insecurity <= 100
        - 0 <= self.confirmed_cases <= 100
        - 0 <= self.unemployment <= 100
        - self.cpi >= 0
        - self.income >= 0
        - data for each attribute is available for the country

    Sample Usage:
    >>> fi = FoodInsecurity()
    >>> fi.index = {'Canada': 22.0}
    >>> canada = Country('Canada', fi)
    >>> canada.name
    'Canada'
    >>> canada.food_insecurity
    22.0
    """
    name: str
    population: int
    food_insecurity: float
    confirmed_cases: float
    unemployment: float
    cpi: float
    income: float

    def __init__(self, name: str, fi: FoodInsecurity) -> None:
        """Initialize the attributes of Country."""
        self.name = name

        # If no data is available for food insecurity or confirmed cases, raise an error
        if name not in fi.index or name not in get_confirmed_cases():
            raise IncorrectCountryError

        self.population = ppln(self.name)
        self.food_insecurity = fi.index[self.name]
        self.confirmed_cases = get_confirmed_cases()[self.name]
        self.unemployment = get_unemployment(self.name)
        self.cpi = get_cpi(self.name)
        self.income = get_income_usd(self.name)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['python_ta.contracts', 'factors'],
        'disable': ['R1705', 'C0200'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
