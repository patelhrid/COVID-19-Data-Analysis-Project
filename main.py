"""The Global Threat of Food Insecurity from the Economic Fallout of COVID-19

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
