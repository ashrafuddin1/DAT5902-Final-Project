import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import numpy as np

sns.set_theme()

def prepare_data(filepath):
    """Loads and cleans the dataset."""
    df = pd.read_csv(filepath)
    df = df.drop(['Code', '900793-annotations', 'World regions according to OWID'], axis=1)
    countries_df = df[df['Entity'] != 'World']
    countries_df = countries_df.dropna()
    return countries_df

def filter_by_2022(countries_df):
    """Filter the dataset for 2022 values only."""
    countries_2022_df = countries_df[countries_df['Year'] == 2022].copy()
    return countries_2022_df

def add_income_group(countries_2022_df):
    """Adds an income group column based on GDP per capita, bounds taken from https://blogs.worldbank.org/en/opendata/new-world-bank-country-classifications-income-level-2022-2023."""
    def income_group(gdp):
        if gdp <= 1085:
            return 'Low Income'
        elif 1085 < gdp <= 4255:
            return 'Lower-middle Income'
        elif 4255 < gdp <= 13205:
            return 'Upper-middle Income'
        else:
            return 'High Income'
    countries_2022_df['Income group'] = countries_2022_df['GDP per capita'].apply(income_group)
    return countries_2022_df

def plot_scatter(countries_2022_df, highlight_countries, bubble_size):
    """Creates a scatter plot with annotations for key countries."""
    plt.figure(figsize=(12, 8))
    
    # Create scatter plot
    scatter = sns.scatterplot(
        data=countries_2022_df,
        x='GDP per capita',
        y='Annual CO₂ emissions (per capita)',
        size=bubble_size, # Bubble size allows varying size of points based on population of country https://seaborn.pydata.org/examples/scatter_bubbles.html
        hue='Income group', # Different colour for each income group
        sizes=(20, 500),
        alpha=0.7
    )
    
    # Annotates specific countries on the graph
    for index, row in countries_2022_df.iterrows(): # iterates over rows of the pd series
        if row['Entity'] in highlight_countries:
            plt.annotate(
                row['Entity'],  # Text to display i.e. the Country name
                (row['GDP per capita'], row['Annual CO₂ emissions (per capita)']),  # Coordinates of the point on the graph
                textcoords="offset points",  # Specify offset so that annotations are next to the point https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.annotate.html
                xytext=(5, 5),  # Position for the text, i.e. 5 points to the right and 5 points up from the country point
                ha='left',  # Horizontal alignment
                fontsize=9,  # Font size
                color='black'  # Text colour
            )
    return plt

def add_regression_line(countries_2022_df):
    """Adds a regression line to the plot."""
    sns.regplot( # https://seaborn.pydata.org/generated/seaborn.regplot.html
        data=countries_2022_df,
        x='GDP per capita',
        y='Annual CO₂ emissions (per capita)',
        scatter=False,  # Disable scatter points since we already plotted the graph
        color='red',  # Regression line colour  
        line_kws={"linewidth": 1}, # Customise line width
        ci = None # Gets rid of confidence interval
    )

def add_emissions_per_gdp(countries_2022_df):
    """Create a new column for carbon emissions per $100,000 GDP"""
    countries_2022_df['CO₂ emissions per $100,000 GDP'] =(countries_2022_df['Annual CO₂ emissions (per capita)']/countries_2022_df['GDP per capita']*100000)

    return countries_2022_df

def create_top_10_barplot(countries_2022_df):

    top_10 = countries_2022_df.sort_values(by='CO₂ emissions per $100,000 GDP',ascending=False).head(10)

    # Create barplot https://seaborn.pydata.org/generated/seaborn.barplot.html#
    plt.figure(figsize=(12, 4))
    sns.barplot(
        data=top_10,
        y='Entity',
        x='CO₂ emissions per $100,000 GDP',
        hue='Income group',  # Colour by income group
        dodge=False
    )
    plt.title('Least carbon efficient countries w.r.t GDP ', fontsize=16)
    plt.xlabel('CO2 Emissions (tons) per $100,000 GDP', fontsize=12)
    plt.ylabel('Country', fontsize=12)
    plt.legend(title='Income Group', bbox_to_anchor=(1, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('top10_figure.png', format='png')

def create_bottom_10_barplot(countries_2022_df):

    bottom_10 = countries_2022_df.sort_values(by='CO₂ emissions per $100,000 GDP',ascending=False).tail(10)

    # Create barplot
    plt.figure(figsize=(12, 4))
    sns.barplot(
        data=bottom_10,
        y='Entity',
        x='CO₂ emissions per $100,000 GDP',
        hue='Income group',  # Colour by income group
        dodge=False
    )
    plt.title('Most carbon efficient countries w.r.t economic production ', fontsize=16)
    plt.xlabel('CO2 Emissions (tons) per $100,000 GDP', fontsize=12)
    plt.ylabel('Country', fontsize=12)
    plt.legend(title='Income Group', bbox_to_anchor=(1, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('bottom10_figure.png', format='png')

def create_headline_plot(countries_2022_df):
    """Creates the scatter plot with regression line and annotations."""  
    # Plot the headline figure
    headline_figure = plot_scatter(
        countries_2022_df,
        highlight_countries = ['United States', 'China', 'India', 'Germany', 'Nigeria', 'Qatar', 'Japan', 'United Kingdom', 'Singapore', 'South Africa',
                       'Brazil', 'South Korea', 'Russia', 'Saudi Arabia', 'Canada', 'Italy', 'Burundi', 'Norway', 'Kuwait', 'United Arab Emirates',
                       'Iran'], # Countries to annotate
        bubble_size='Population (historical)',
    )
    add_regression_line(countries_2022_df)
    
    # Add labels and title
    plt.title('2022 CO2 Emissions vs. GDP Per Capita', fontsize=16)
    plt.xlabel('GDP Per Capita ($)', fontsize=14)
    plt.ylabel('CO2 Emissions Per Capita (Tons)', fontsize=14)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.tight_layout() # Makes sure the graph fits inside the figure
    plt.savefig('headline_figure.png', format='png')

def headlineplot_analysis(countries_2022_df):

    gdp_pc = countries_2022_df['GDP per capita']
    co2_pc = countries_2022_df['Annual CO₂ emissions (per capita)']

    # Calculate correlation coefficient
    corr_coef, p_value = pearsonr(gdp_pc, co2_pc) # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html

    print(f"Correlation Coefficient between GDP per capita and Annual CO₂ emissions per capita: {corr_coef:.4f}")

    population = countries_2022_df['Population (historical)']
    co2 = countries_2022_df['Annual CO₂ emissions (per capita)']*countries_2022_df['Population (historical)']

    # Calculate correlation coefficient
    corr_coef, p_value = pearsonr(population, co2)

    print(f"Correlation Coefficient between Population and Estimated total CO₂ emissions: {corr_coef:.4f}")

    gdp = countries_2022_df['GDP per capita']*countries_2022_df['Population (historical)']

    # Calculate correlation coefficient
    corr_coef, p_value = pearsonr(gdp, co2)

    print(f"Correlation Coefficient between Estimated total GDP and Estimated total CO₂ emissions: {corr_coef:.4f}")

    # Regression analysis

    x = countries_2022_df['GDP per capita'] / 20000
    y = countries_2022_df['Annual CO₂ emissions (per capita)']

    slope, intercept = np.polyfit(x, y, 1) # Fitting a linear model: y = mx + b https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html

    print(f"Gradient (Slope): {slope:.2f}")
    print(f"Intercept: {intercept:.2f}")

    # Summary statistics

    averages = countries_2022_df.groupby('Income group')[['GDP per capita', 'Annual CO₂ emissions (per capita)', 
                                                          'CO₂ emissions per $100,000 GDP']].mean().round(2)
    print(averages)

    overall_averages = countries_2022_df[['GDP per capita', 'Annual CO₂ emissions (per capita)', 'CO₂ emissions per $100,000 GDP']].mean().round(2)
    print(overall_averages)

def create_final_analysis(filepath):
    """Create the 3 final plots and print quantitative analysis"""

    # Data preparation
    countries_df = prepare_data(filepath)
    countries_2022_df = filter_by_2022(countries_df)
    countries_2022_df = add_income_group(countries_2022_df)
    countries_2022_df = add_emissions_per_gdp(countries_2022_df)

    create_headline_plot(countries_2022_df)
    create_top_10_barplot(countries_2022_df)
    create_bottom_10_barplot(countries_2022_df)
    headlineplot_analysis(countries_2022_df)

create_final_analysis('co2-emissions-vs-gdp.csv')