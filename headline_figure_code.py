import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
        size=bubble_size,
        hue='Income group',
        sizes=(20, 500),
        alpha=0.7
    )
    
    # Annotates specific countries on the graph
    for index, row in countries_2022_df.iterrows():
        if row['Entity'] in highlight_countries:
            plt.annotate(
                row['Entity'],  # Text to display
                (row['GDP per capita'], row['Annual CO₂ emissions (per capita)']),  # Coordinates of the point on the graph
                textcoords="offset points",  # Specify offset so that annotations are next to the point
                xytext=(5, 5),  # Offset for the text, i.e. 5 units to the right and 5 units up from the country point
                ha='left',  # Horizontal alignment
                fontsize=9,  # Font size
                color='black'  # Text color
            )
    return plt

def add_regression_line(countries_2022_df):
    """Adds a regression line to the plot."""
    sns.regplot(
        data=countries_2022_df,
        x='GDP per capita',
        y='Annual CO₂ emissions (per capita)',
        scatter=False,  # Disable scatter points since we already plotted the graph
        color='red',  # Regression line color  
        line_kws={"linewidth": 1}, # Customise line width
        ci = None # Gets rid of confidence interval
    )

def create_final_plot(filepath):
    """Prepares data and creates the scatter plot."""
    # Preparation
    countries_df = prepare_data(filepath)
    countries_2022_df = filter_by_2022(countries_df)
    countries_2022_df = add_income_group(countries_2022_df)
    
    # Plot the headline figure
    headline_figure = plot_scatter(
        countries_2022_df,
        highlight_countries = ['United States', 'China', 'India', 'Germany', 'Nigeria', 'Qatar', 'Japan', 'United Kingdom', 'Singapore', 'South Africa',
                       'Brazil', 'South Korea', 'Russia', 'Saudi Arabia', 'Canada', 'Italy', 'Burundi', 'Norway', 'Kuwait', 'United Arab Emirates',
                       'Iran'],
        bubble_size='Population (historical)',
    )
    add_regression_line(countries_2022_df)
    
    # Add labels and title
    plt.title('2022 CO2 Emissions vs. GDP Per Capita', fontsize=16)
    plt.xlabel('GDP Per Capita (USD)', fontsize=14)
    plt.ylabel('CO2 Emissions Per Capita (Metric Tons)', fontsize=14)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.tight_layout() # Makes sure the graph fits inside the figure
    plt.savefig('headline_figure.png', format='png')

create_final_plot('co2-emissions-vs-gdp.csv')