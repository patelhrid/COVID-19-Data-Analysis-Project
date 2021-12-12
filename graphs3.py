"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the functions and classes that will create the plots of our datasets
using plotly.
"""

import plotly.graph_objects as go
from typing import Iterable
from countries import Country
from factors import FoodInsecurity, get_confirmed_cases


# Creating classes
def plot_graph(food_insecurity: FoodInsecurity) -> None:
    """Graph the data for confirmed cases to food insecurity for all countries and
    specific countries.

    Preconditions
        - food_insecurity.percentages != {}
    """
    # Data and plot for all countries
    all_cases_vs_fi = AllCasesVsFoodInsecurity(food_insecurity)
    all_cases_vs_fi_data = all_cases_vs_fi.data

    # Plot for the 8 specific countries
    cases_vs_fi = CasesVsFoodInsecurity(food_insecurity, all_cases_vs_fi_data)

    # Create the first plot for all countries (from all_cases_vs_fi)
    fig = go.Figure()
    fig.add_trace(all_cases_vs_fi.get_plot())

    # Create the second plot for the 8 countries (from cases_vs_fi)
    fig.add_trace(cases_vs_fi.get_plot())

    # Change the titles of the plots
    fig.update_layout(title={'text': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'y': 0.932, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top',
                             'font': {'size': 25}},
                      xaxis_title='Confirmed Cases (%)',
                      yaxis_title='Food Insecurity (%)')

    # Create buttons to toggle between the plots
    fig.update_layout(updatemenus=[
        dict(type='buttons',
             direction='left',
             x=0, y=1.07,
             xanchor='left', yanchor='top',
             font={'size': 14},
             buttons=list([
                 dict(label='All Countries',
                      method='update',
                      args=[{'visible': [True, False]},
                            {'title': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'xaxis_title': 'Confirmed Cases (%)',
                             'yaxis_title': 'Food Insecurity (%)',
                             'font': {'size': 14}
                             }]),
                 dict(label='8 Countries',
                      method='update',
                      args=[{'visible': [False, True]},
                            {'title': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'xaxis_title': 'Confirmed Cases (%)',
                             'yaxis_title': ' Insecurity (%)',
                             'font': {'size': 14}
                             }]),
             ]), )
    ])

    # Add labels for the buttons
    fig.update_layout(annotations=[
        dict(text='Food Insecurity:', showarrow=False, x=0, y=1.107, yref='paper', xref='paper',
             visible=True, font_size=15)
    ])

    # Adjust size for x and y axes
    fig.for_each_xaxis(lambda axis: axis.title.update(font=dict(size=18)))
    fig.for_each_yaxis(lambda axis: axis.title.update(font=dict(size=18)))

    # Display the graph
    fig.show()


class GraphData:
    """An abstract class representing the data of a graph.

    Instance Attributes:
        - data: the data for the graph
    """
    data: Iterable

    def get_data(self, **kwargs) -> None:
        """Update the data needed to graph, containing the x-values, y-values, and countries."""
        raise NotImplementedError

    def get_plot(self) -> go.Scatter:
        """Return a scatter plot containing the values in data."""
        raise NotImplementedError


class AllCasesVsFoodInsecurity(GraphData):
    """A concrete class representing a graph comparing confirmed cases to food insecurity for
    many countries.

    Instance Attributes:
        - data: the data for the graph
    """
    data: dict[str, tuple[float, float]]

    def __init__(self, food_insecurity: FoodInsecurity) -> None:
        self.data = {}
        self.get_data(food_insecurity)

    def get_data(self, food_insecurity: FoodInsecurity) -> None:
        """Update the data for the plot graphing confirmed cases vs food insecurity levels for each
        country as a dictionary mapping countries to x and y coordinates, where x is the confirmed
        case and y is the food insecurity level.

        Preconditions
            - food_insecurity.percentages != {}
        """
        confirmed_cases = get_confirmed_cases()

        countries = [key for key in food_insecurity.percentages]

        for country in countries:
            if country in confirmed_cases:
                x, y = confirmed_cases[country], food_insecurity.percentages[country]
                self.data[country] = (x, y)

        x_coords = []
        y_coords = []
        all_countries = []

        for country in self.data:
            x_coords.append(self.data[country][0] / 100)
            y_coords.append(self.data[country][1] / 100)
            all_countries.append(country)

    def get_plot(self) -> go.Scatter:
        """Return a scatter plot containing the values in self.data of food insecurity and
        confirmed cases for all countries.

        Preconditions:
            - self.data != []
        """
        # Unpacking the data for all countries
        x_coords = []
        y_coords = []
        all_countries = []

        # Dividing by 100 to get decimal values that will later be converted to percentages on the plot
        for country in self.data:
            x_coords.append(self.data[country][0] / 100)
            y_coords.append(self.data[country][1] / 100)
            all_countries.append(country)

        # Create a plot
        plot = go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='markers',
            text=all_countries,
            hovertemplate='<b>%{text}</b><br><br>' +
                          'Confirmed Cases: %{x:.2%}<br>' +
                          'Food Insecurity: %{y:.1%}<br>' +
                          '<extra></extra>',
            showlegend=False,
        )

        return plot


class CasesVsFoodInsecurity(GraphData):
    """A concrete class representing a graph comparing confirmed cases to food insecurity for the
    8 specific countries.

    Instance Attributes:
        - data: the data for the graph
    """
    data: list[tuple[float, float, str]]

    def __init__(self, food_insecurity: FoodInsecurity, data: dict[str, tuple[float, float]]) -> None:
        self.data = []
        self.get_data(food_insecurity, data)

    def get_data(self, food_insecurity: FoodInsecurity, data: dict[str, tuple[float, float]]) \
            -> None:
        """Return the specific values from data for the eight countries as a sorted list of tuples,
        from least to greatest. Each tuple is in the form (x, y, c), where x is the percent of
        confirmed cases, y is the food insecurity level, and c refers to the country. Each country
        is a Country object, given the input food_insecurity.

        Preconditions:
            - food_insecurity != {}
        """
        countries = create_countries(food_insecurity)

        for country in countries:
            x, y, c = data[country.name][0], data[country.name][1], country.name
            self.data.append((x, y, c))
        self.data.sort()

    def get_plot(self) -> go.Scatter:
        """Return a scatter plot containing the values in self.data of food insecurity and confirmed
        cases for 8 specific countries.

        Preconditions:
            - self.data != []
        """
        # Unpacking the data for the 8 specific countries
        # Dividing by 100 to get decimal values that will later be converted to percentages on the plot
        x_coords = [value[0] / 100 for value in self.data]
        y_coords = [value[1] / 100 for value in self.data]
        countries_so_far = [value[2] for value in self.data]

        # Create a plot
        plot = go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='lines+markers',
            text=countries_so_far,
            hovertemplate='<b>%{text}</b><br><br>' +
            'Confirmed Cases: %{x:.2%}<br>' +
            'Food Insecurity: %{y:.1%}<br>' +
            '<extra></extra>',
            showlegend=False,
            visible=False
        )

        return plot


# OR in separate functions
def plot_graph2(food_insecurity: FoodInsecurity) -> None:
    """Graph the data for confirmed cases to food insecurity for all countries and
    specific countries.

    Preconditions
        - food_insecurity.percentages != {}
    """
    # Data for all countries
    data1 = data_cases_vs_fi(food_insecurity)

    # Data for the 8 specific countries
    data2 = data_cases_vs_fi_countries(food_insecurity, data1)

    # Create the first plot for all countries (from data1)
    fig = go.Figure()
    fig.add_trace(cases_vs_fi_all(data1))

    # Create the second plot for the 8 countries (from data2)
    fig.add_trace(cases_vs_fi(data2))

    # Change the titles of the plots
    fig.update_layout(title={'text': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'y': 0.932, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top',
                             'font': {'size': 25}},
                      xaxis_title='Confirmed Cases (%)',
                      yaxis_title='Food Insecurity (%)')

    # Create buttons to toggle between the plots
    fig.update_layout(updatemenus=[
        dict(type='buttons',
             direction='left',
             x=0, y=1.07,
             xanchor='left', yanchor='top',
             font={'size': 14},
             buttons=list([
                 dict(label='All Countries',
                      method='update',
                      args=[{'visible': [True, False]},
                            {'title': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'xaxis_title': 'Confirmed Cases (%)',
                             'yaxis_title': 'Food Insecurity (%)',
                             'font': {'size': 14}
                             }]),
                 dict(label='8 Countries',
                      method='update',
                      args=[{'visible': [False, True]},
                            {'title': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'xaxis_title': 'Confirmed Cases (%)',
                             'yaxis_title': ' Insecurity (%)',
                             'font': {'size': 14}
                             }]),
             ]), )
    ])

    fig.update_layout(annotations=[
        dict(text='Food Insecurity:', showarrow=False, x=0, y=1.107, yref='paper', xref='paper',
             visible=True, font_size=15)
    ])

    fig.for_each_xaxis(lambda axis: axis.title.update(font=dict(size=18)))
    fig.for_each_yaxis(lambda axis: axis.title.update(font=dict(size=18)))

    fig.show()


def cases_vs_fi_all(all_data: dict[str, tuple[float, float]]) -> go.Scatter:
    """Return a scatter plot containing the values in all_data of food insecurity and confirmed
    cases for all countries.

    Preconditions:
        - all_data != []
    """
    # Unpacking the data for all countries
    x_coords = []
    y_coords = []
    all_countries = []

    # Dividing by 100 to get decimal values that will later be converted to percentages on the plot
    for country in all_data:
        x_coords.append(all_data[country][0] / 100)
        y_coords.append(all_data[country][1] / 100)
        all_countries.append(country)

    # Create a plot
    plot = go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers',
        text=all_countries,
        hovertemplate='<b>%{text}</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      'Food Insecurity: %{y:.1%}<br>' +
                      '<extra></extra>',
        showlegend=False,
    )

    return plot


def cases_vs_fi(data: list[tuple[float, float, str]]) -> go.Scatter:
    """Return a scatter plot containing the values in data of food insecurity and confirmed cases
    for 8 specific countries.

    Preconditions:
        - data != []
    """
    # Unpacking the data for the 8 specific countries
    # Dividing by 100 to get decimal values that will later be converted to percentages on the plot
    x_coords = [value[0] / 100 for value in data]
    y_coords = [value[1] / 100 for value in data]
    countries_so_far = [value[2] for value in data]

    # Create a plot
    plot = go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='lines+markers',
        text=countries_so_far,
        hovertemplate='<b>%{text}</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      'Food Insecurity: %{y:.1%}<br>' +
                      '<extra></extra>',
        showlegend=False,
        visible=False
    )

    return plot


def data_cases_vs_fi(food_insecurity: FoodInsecurity) -> dict[str, tuple[float, float]]:
    """Return the data for the plot graphing confirmed cases vs food insecurity levels for each
    country as a dictionary mapping countries to x and y coordinates, where x is the confirmed case
    and y is the food insecurity level.

    Preconditions
        - food_insecurity.percentages != {}
    """
    confirmed_cases = get_confirmed_cases()

    # ACCUMULATOR data_so_far: the data for confirmed cases and food insecurity for each country,
    # so far
    data_so_far = {}
    countries = [key for key in food_insecurity.percentages]

    for country in countries:
        if country in confirmed_cases:
            x, y = confirmed_cases[country], food_insecurity.percentages[country]
            data_so_far[country] = (x, y)

    x_coords = []
    y_coords = []
    all_countries = []

    for country in data_so_far:
        x_coords.append(data_so_far[country][0] / 100)
        y_coords.append(data_so_far[country][1] / 100)
        all_countries.append(country)

    return data_so_far


def data_cases_vs_fi_countries(food_insecurity: FoodInsecurity,
                               data: dict[str, tuple[float, float]]) \
        -> list[tuple[float, float, str]]:
    """Return the specific values from data for the eight countries as a list of tuples in the form
    (x, y, c), where x is the percent of confirmed cases, y is the food insecurity level, and c
    refers to the country. Each country is a Country object, given the input food_insecurity.

    Preconditions:
        - food_insecurity != {}
    """
    countries = create_countries(food_insecurity)

    # ACCUMULATOR values_so_far: the x, y, c values in the data so far
    values_so_far = []

    for country in countries:
        x, y, c = data[country.name][0], data[country.name][1], country.name
        values_so_far.append((x, y, c))
    values_so_far.sort()

    return values_so_far


def create_countries(food_insecurity: FoodInsecurity) -> list[Country]:
    """Return a list of Country objects that will be plotted on the graph.

    Preconditions
        - food_insecurity.percentages != {}
    """
    canada = Country('Canada', food_insecurity)
    usa = Country('United States', food_insecurity)
    # uae = Country('United Arab Emirates', food_insecurity)
    # france = Country('France', food_insecurity)
    # china = Country('China', food_insecurity)
    japan = Country('Japan', food_insecurity)
    australia = Country('Australia', food_insecurity)
    uk = Country('United Kingdom', food_insecurity)

    return [canada, usa, japan, australia, uk]  # uae, france, china
