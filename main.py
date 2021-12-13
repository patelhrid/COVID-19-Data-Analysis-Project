"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main function and blocks of code required to run the entire
program. When this module is run, the food_security.json file is created from the factors module.
Call the show_graph function to produce interactive graphs in your browser of food insecurity,
confirmed COVID-19 cases, and the potential factor influencing food insecurity!
"""

from scrapy.crawler import CrawlerProcess
from factors import FoodSecurity, FoodInsecurity
import graphs


def show_graph() -> None:
    """Generate a graph showing the food insecurity, confirmed cases, and different factors."""
    graphs.plot_graph(food_insecurity)


if __name__ == '__main__':
    process = CrawlerProcess(settings={'FEEDS': {'food_security.json': {'format': 'json',
                                                                        'overwrite': True}, },
                                       'LOG_ENABLED': False})
    process.crawl(FoodSecurity)
    process.start()

    food_insecurity = FoodInsecurity()
    food_insecurity.calculate_food_insecurity()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'scrapy.crawler', 'factors', 'graphs'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
