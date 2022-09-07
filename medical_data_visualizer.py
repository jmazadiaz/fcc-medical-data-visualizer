import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv',index_col=0)

# Add 'overweight' column
df['overweight'] = 0
df.loc[(df['weight']/((df['height']/100)**2) >25)
       ,'overweight'] = 1

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df.loc[~(df['cholesterol']>1), 'cholesterol'] = 0
df.loc[(df['cholesterol']>1), 'cholesterol'] = 1

df.loc[~(df['gluc']>1), 'gluc'] = 0
df.loc[(df['gluc']>1), 'gluc'] = 1



# Filter Data
df.drop(index = df[( ~(df['ap_lo'] <= df['ap_hi'])
                    |~(df['height'] >= df['height'].quantile(0.025))
                    |~(df['height'] <= df['height'].quantile(0.975))
                    |~(df['weight'] >= df['weight'].quantile(0.025))
                    |~(df['weight'] <= df['weight'].quantile(0.975)))
                  ].index, inplace = True )

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,value_vars=['active', 'alco', 'cholesterol','gluc', 'overweight','smoke'] ,id_vars='cardio')


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    
    df_cat = df_cat.groupby('cardio')
    
    d_temp_ = pd.DataFrame()
    

    for i,x_ in df_cat:
        count = x_.value_counts()

    # Serie to D.Frame
        for k,m in count.iteritems():
            pieces = pd.Series([i,k[1],k[2],m],index=['cardio','variable','value','total'])
            d_temp_ = pd.concat([d_temp_,pieces.to_frame().T],ignore_index=True)
            

    # Entero
    d_temp_['cardio'] = pd.to_numeric(d_temp_['cardio'], downcast='integer') 
    d_temp_['value'] = pd.to_numeric(d_temp_['value'], downcast='integer')  

    

    # Draw the catplot with 'sns.catplot()'
    cp = sns.catplot(x='variable', kind='bar', hue='value', y='total', col='cardio' 
                     , order= ['active','alco','cholesterol','gluc','overweight' 
                               ,'smoke']  , data=d_temp_)


    # Get the figure for the output
    fig = cp.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig



# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.copy()
    
    df_heat.reset_index(inplace=True)
    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask =  np.triu(df_heat.corr())


    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10.0, 10.0))

    # Draw the heatmap with 'sns.heatmap()'

    sns.heatmap(ax=ax, data=corr, annot=True, fmt='.1f', mask=mask)


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
