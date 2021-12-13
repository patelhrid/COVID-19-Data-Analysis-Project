"""Graphing COVID-19 Cases, Food Insecurity, and Other Economic Factors

Instructions
============

This Python module contains the functions that will create the plots of our datasets using plotly.
There are 8 main countries whose data is being plotted: Canada, United States, United Arab
Emirates, France, China, Japan, Australia, and United Kingdom.

There are 5 plots with the independent variable as the percent of confirmed COVID-19 cases in
each country. The first dependent variable is Food Insecurity for all countries whose data was
available. The rest focus on the 8 countries listed above: Food Insecurity, Unemployment,
Consumer Price Index, and Income.
"""
import math
import statistics
import plotly.graph_objects as go
from countries import Country
from factors import FoodInsecurity, get_confirmed_cases


def plot_graph(food_insecurity: FoodInsecurity) -> None:
    """Graph the data for confirmed cases to food insecurity for all countries and
    specific countries.

    Preconditions
        - food_insecurity.percentages != {}
    """

    # Create the 8 countries as Country objects and get the data for confirmed cases
    countries = create_countries(food_insecurity)
    confirmed_cases = get_confirmed_cases()

    # FOOD INSECURITY PLOTS
    all_food_insecurity_plot = plot_fi_all(food_insecurity, confirmed_cases)
    food_insecurity_plot, food_insecurity_lobf = get_graphs('Food Insecurity', countries)

    # UNEMPLOYMENT, CPI, AND INCOME PLOTS
    unemployment_plot, unemployment_lobf = get_graphs('Unemployment', countries)
    cpi_plot, cpi_lobf = get_graphs('Consumer Price Index', countries)
    # income_plot, income_lobf = get_graphs('Consumer Price Index', countries)

    # Create the plot and add traces for each graph
    fig = go.Figure()
    fig.add_trace(all_food_insecurity_plot)     # Trace 1
    fig.add_trace(food_insecurity_plot)         # Trace 2
    fig.add_trace(food_insecurity_lobf)         # Trace 3
    fig.add_trace(unemployment_plot)            # Trace 4
    fig.add_trace(unemployment_lobf)            # Trace 5
    fig.add_trace(cpi_plot)                     # Trace 6
    fig.add_trace(cpi_lobf)                     # Trace 7

    # Change the initial titles of the plots
    fig.update_layout(title={'text': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'y': 0.932, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top',
                             'font': {'size': 25}},
                      xaxis_title='Confirmed Cases (%)',
                      yaxis_title='Food Insecurity (%)')

    # Create buttons to toggle between the plots
    # The values in args correspond to each trace of fig: [Trace 1, Trace 2, Trace 3, ...] and so on
    fig.update_layout(updatemenus=[
        # Buttons for food insecurity plots
        dict(type='buttons',
             direction='left',
             x=0, y=1.07,
             xanchor='left', yanchor='top',
             font={'size': 14},
             buttons=list([
                 dict(label='All Countries',
                      method='update',
                      args=[{'visible': [True, False, False, False, False, False, False]},
                            {'title': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'xaxis': {'title': 'Confirmed Cases (%)'},
                             'yaxis': {'title': 'Food Insecurity (%)'},
                             'font': {'size': 15},
                             }]),
                 dict(label='8 Countries',
                      method='update',
                      args=[{'visible': [False, True, 'legendonly', False, False, False, False]},
                            {'title': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'xaxis': {'title': 'Confirmed Cases (%)'},
                             'yaxis': {'title': 'Food Insecurity (%)'},
                             'font': {'size': 15}
                             }]),
             ]), ),

        # Buttons for economic factors plots
        dict(type='buttons',
             direction='left',
             x=1, y=1.07,
             xanchor='right', yanchor='top',
             font={'size': 14},
             buttons=list([
                 dict(label='Unemployment',
                      method='update',
                      args=[{'visible': [False, False, False, True, 'legendonly', False, False]},
                            {'title': 'Confirmed COVID-19 Cases vs Unemployment',
                             'xaxis': {'title': 'Confirmed Cases (%)'},
                             'yaxis': {'title': 'Unemployment Rate (%)'},
                             'font': {'size': 15},
                             }]),
                 dict(label='CPI',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, True, 'legendonly']},
                            {'title': 'Confirmed COVID-19 Cases vs CPI',
                             'xaxis': {'title': 'Confirmed Cases (%)'},
                             'yaxis': {'title': 'Consumer Price Index (%)'},
                             'font': {'size': 15}
                             }]),
             ]), )
    ])

    # Add labels for the buttons
    fig.update_layout(annotations=[
        dict(text='Food Insecurity:', showarrow=False, x=0, y=1.107, yref='paper', xref='paper',
             visible=True, font_size=15),
        dict(text='Economic Factors:', showarrow=False, x=1, y=1.107, yref='paper', xref='paper',
             visible=True, font_size=15)
    ])

    # Adjust size for x and y axes
    fig.for_each_xaxis(lambda axis: axis.title.update(font=dict(size=18)))
    fig.for_each_yaxis(lambda axis: axis.title.update(font=dict(size=18)))

    # Display the graph
    fig.show()


def get_graphs(factor: str, countries: list[Country]) -> list[go.Scatter]:
    """Return a list of scatter plots, the first being the main plot, and the second being the
    line of best fit plot.

    Preconditions
        - countries is the list returned from the create_countries function
        - factor in ['Food Insecurity', 'Unemployment', 'Consumer Price Index', 'Income']
    """
    x, y, c = get_data(countries, factor)
    main_plot = get_plot(x, y, c, factor)
    line_of_best_fit = get_lobf(x, y)
    return [main_plot, line_of_best_fit]


def get_plot(x_values: list[float], y_values: list[float], countries: list[Country], factor: str) \
        -> go.Scatter:
    """Return a scatter plot displaying data for factor, plotting each value in x_values and
    y-values for their corresponding country in countries.

    Preconditions:
        - x_values != []
        - y_values != []
        - countries != []
        - countries is the list returned from the create_countries function
        - factor in ['Food Insecurity', 'Unemployment', 'Consumer Price Index', 'Income']
    """
    plot = go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        name='Data',
        text=countries,
        hovertemplate='<b>%{text}</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      f'{factor}'': %{y:.1%}<br>' +
                      '<extra></extra>',
        showlegend=True,
        visible=False
    )

    return plot


def get_lobf2(x_values: list[float], y_values: list[float], countries: list[Country], factor: str) \
        -> go.Scatter:
    """Return a line plot with the line of best fit for unemployment rate and
    confirmed cases.

    Preconditions:
        - x_values != []
        - y_values != []
        - countries != []
        - countries is the list returned from the create_countries function
        - factor in ['Food Insecurity', 'Unemployment', 'Consumer Price Index', 'Income']
    """
    # Line of best fit coordinates
    lobf_x_values = []
    lobf_y_values = []

    slopes = []
    for i in range(len(x_values) - 1):
        slopes.append((x_values[i + 1] - x_values[i]) /
                      (y_values[i + 1] - y_values[i]))
    slope = statistics.mean(slopes)
    y_intercept = (sum(y_values) - (slope * (sum(x_values)))) / len(countries)

    # For a meaningful LOBF
    max_unemployment = max(y_value for y_value in y_values)
    max_confirmed_cases = max(x_value for x_value in x_values)

    for x in range(0, math.ceil(max_confirmed_cases) * 620, 1):  # * 620 for more points...
        y = slope * (x / 10000) + y_intercept
        if 0 < y < max_unemployment * 1.5:  # * 1.5 for a bit more insight
            lobf_x_values.append(x / 10000)
            lobf_y_values.append(y)

    lobf = go.Scatter(
        x=lobf_x_values,
        y=lobf_y_values,
        mode='lines',
        name='Line of Best Fit',
        hovertemplate='<b>Line of Best Fit</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      f'{factor}'': %{y:.1%}<br>' +
                      '<extra></extra>',
        line=dict(color='firebrick', width=2),
        showlegend=True,
        visible=False
    )

    return lobf


def get_lobf(x_values: list[float], y_values: list[float]) -> go.Scatter:
    """Return a line plot with the line of best fit for unemployment rate and
    confirmed cases.

    Equation for line of best fit:
    Let x1 and y1 be coordinates in the data. Let X and Y be the means of the x-values and y-values
        slope = summation((x1 - X)(y1 - y)) / summation((x1 - X)^2),
        y_intercept = Y - slope * x

    Preconditions:
        - x_values != []
        - y_values != []
        - len(x_values) == len(y_values)
    """
    # Calculate the slope and y-intercept for the line of best fit
    # ACCUMULATORS: the running numerator and denominator of the equation for line of best fit
    numerator_so_far = 0
    denominator_so_far = 0
    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)

    for i in range(len(x_values)):
        numerator_so_far += (x_values[i] - x_mean) * (y_values[i] - y_mean)
        denominator_so_far += (x_values[i] - x_mean) ** 2

    slope = numerator_so_far / denominator_so_far
    y_intercept = y_mean - slope * x_mean

    # Generate points for the line of best fit
    # ACCUMULATORS: the line of best fit coordinates so far
    lobf_x_values = []
    lobf_y_values = []

    for x in x_values:
        lobf_x_values.append(x)
        lobf_y_values.append(slope * x + y_intercept)

    lobf = go.Scatter(
        x=lobf_x_values,
        y=lobf_y_values,
        mode='lines',
        name='Line of Best Fit',
        line=dict(color='firebrick', width=2),
        showlegend=True,
        visible=False
    )

    return lobf


def get_data(countries: list[Country], factor: str) -> list[list]:
    """Return the data for the plot showing data for the 8 specific countries. The data returned
     is a list of x-values as the confirmed cases, y-values as the factor values, and country names.

    Preconditions
        - countries is the list returned from the create_countries function
        - factor in ['Unemployment', 'Consumer Price Index', 'Income']
    """
    # Get the proper y-values, depending on the factor input
    if factor == 'Food Insecurity':
        data = [(country.confirmed_cases, country.food_insecurity, country.name)
                for country in countries]
    elif factor == 'Unemployment':
        data = [(country.confirmed_cases, country.unemployment, country.name)
                for country in countries]
    elif factor == 'Consumer Price Index':
        data = [(country.confirmed_cases, country.cpi, country.name)
                for country in countries]
    else:  # factor == 'Income'
        data = [(country.confirmed_cases, country.income, country.name)
                for country in countries]
    data.sort()

    # Unpacking the data for the 8 specific countries
    # Dividing by 100 to get decimal values that will later be converted to percentages on
    # the plot
    x_values = [value[0] / 100 for value in data]
    y_values = [value[1] / 100 for value in data]
    countries = [value[2] for value in data]

    return [x_values, y_values, countries]


def plot_fi_all(food_insecurity: FoodInsecurity, confirmed_cases: dict[str, float]) -> go.Scatter:
    """Return a scatter plot displaying data in confirmed_cases as the x-values and data in
    food_insecurity as the y-values for all available countries.

    Preconditions:
        - food_insecurity.percentages != {}
        - confirmed_cases != {}
    """
    x_values, y_values, countries = data_fi_all(food_insecurity, confirmed_cases)
    plot = go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        text=countries,
        hovertemplate='<b>%{text}</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      'Food Insecurity: %{y:.1%}<br>' +
                      '<extra></extra>',
        showlegend=False,
    )

    return plot


def data_fi_all(food_insecurity: FoodInsecurity, confirmed_cases: dict[str, float]) -> list[list]:
    """Return the data for the plot graphing confirmed cases vs food insecurity levels for each
    country as a list of x-values as the confirmed cases, y-values as the food insecurity level,
    and country names.

    Preconditions
        - food_insecurity.percentages != {}
        - confirmed_cases != {}
    """
    # ACCUMULATORS: the data for confirmed cases and food insecurity so far
    x_values = []
    y_values = []
    countries_so_far = []

    countries = [key for key in food_insecurity.percentages]

    for country in countries:
        # Only get data for the countries in both food_insecurity.percentages and confirmed_cases
        if country in confirmed_cases:
            x_values.append(confirmed_cases[country] / 100)
            y_values.append(food_insecurity.percentages[country] / 100)
            countries_so_far.append(country)

    return [x_values, y_values, countries_so_far]


def create_countries(food_insecurity: FoodInsecurity) -> list[Country]:
    """Return a list of 8 Country objects that will be plotted on the graph.

    Preconditions
        - food_insecurity.percentages != {}
        - data for the Country attributes is available for each Country made
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


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'plotly.graph_objects', 'countries', 'factors',
                          'statistics', 'math'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9989', 'R1721'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
