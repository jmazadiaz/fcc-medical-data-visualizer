import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    plt.scatter(x=df['Year'], y=df['CSIRO Adjusted Sea Level'], s=10, c='black')

    # Create first line of best fit
    slope, intercept = linregress(
        x=df['Year'], y=df['CSIRO Adjusted Sea Level'])[0:2]
    ext_years = np.arange(df['Year'].iloc[0], 2050)
    plt.plot(ext_years, intercept + slope * ext_years, 'r')

    # Create second line of best fit
    mask = (df['Year'] >= 2000)
    slope, intercept = linregress(
        x=df.loc[mask, 'Year'],
        y=df.loc[mask, 'CSIRO Adjusted Sea Level'])[0:2]
    ext_years = np.arange(2000, 2050)
    plt.plot(ext_years, intercept + slope * ext_years, 'b')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()
