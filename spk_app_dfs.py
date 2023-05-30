import pandas as pd
# import numpy as np
from datetime import date, datetime, timedelta
import pytz
import random
import math
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import os

def app_dfs():

    def to_percent(x):
        x = x
        return "{:.1%}".format(x)

    # def to_pm_est(time_str):
    #     datetime_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    #     datetime_obj += datetime.timedelta(hours=4)
    #     time_str = datetime_obj.strftime("%H:%M")
    #     timezone = pytz.timezone("US/Eastern")
    #     converted_time_str = datetime_obj.astimezone(timezone).strftime("%-I:%M %p %Z")
    #     return converted_time_str
    #imports
    df = pd.read_csv('spk_viz_data.csv')
    sp_df = pd.read_csv('spk_today.csv')
    # sp_df['Game Time'] = sp_df['commence_time'].apply(to_pm_est)
    sp_df = df[['Name', 'Team', 'Opponent', 'xK', 'prop_k']]
    # sp_df = sp_df[['Name', 'Team', 'Opponent', 'xK', 'prop_k', 'Game Time']]
    # sp_df.sort_values(by=['Game Time'], ascending=True, inplace=True)
    # sp_df.reset_index(drop=True, inplace=True)
    # sp_df['Game Time'] = sp_df['commence_time'].apply(to_pm_est)

    df_under = pd.read_csv('spk_under_today.csv')
    df_over = pd.read_csv('spk_over_today.csv')
    df_spk_sim = pd.read_csv('spk_sim.csv')
    df_results = pd.read_csv('spk_yesterday_results.csv')

    ### over/ under updates
    df_over.rename(columns={'over_diff': 'expected value'}, inplace=True)
    df_under.rename(columns={'under_diff': 'expected value'}, inplace=True)


    over_odds = ['expected value', 'over_odds', 'x_over']
    under_odds = ['expected value', 'under_odds', 'x_under']

    for col in over_odds:
        df_over[col] = df_over[col].apply(to_percent)

    for col in under_odds:
        df_under[col] = df_under[col].apply(to_percent)

    df_over = df_over[['Name', 'Team', 'Opponent', 'xK', 'prop_k', 'over', 'expected value',  'over_odds', 'x_over']]
    df_under = df_under[['Name', 'Team', 'Opponent', 'xK', 'prop_k', 'under', 'expected value', 'under_odds', 'x_under']]
    #sim updates
    df_spk_sim['Percent'] = df_spk_sim['Percent'].apply(to_percent)
    df_spk_sim.drop(columns=['Count'], inplace=True)
    df_spk_sim.rename(columns={'Percent': 'Probability'}, inplace=True)

    def plot_strikeout_distributions(df, fig_width=8, fig_height=10, n_cols=2):
        # Define the number of plots
        n_plots = len(df)

        # Calculate the number of rows needed
        n_rows = int(math.ceil(n_plots / n_cols))

        # Create the figure and subplots
        fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(fig_width, fig_height))

        # Flatten the axes array to make it easier to iterate over
        axes = axes.flatten()

        # Loop through each row in the dataframe and plot the distribution
        for index, row in df.iterrows():
            # Get the subplot index for this row
            plot_index = index % n_plots

            # Plot the distribution for the row
            ax = sns.lineplot(x=range(len(row['Poisson_0':'Poisson_20'])), y=row['Poisson_0':'Poisson_20'], ax=axes[plot_index])
            # ax.fill_between(x=range(len(row['Poisson_0':'Poisson_20'])), y1=row['Poisson_0':'Poisson_20'], alpha=0.5)

            # Add vertical lines for xK and prop_k
            ax.axvline(x=row['xK'], color='red', linestyle='--', label='xK')
            ax.axvline(x=row['prop_k'], color='black', linestyle='-', label='prop_k')

            # Set the title and axis labels for the subplot
            ax.set_title(f"{row['Name']} ({row['Team']} vs. {row['Opponent']})")
            ax.set_ylabel("Probability")
            ax.set_xlim([0, 17])
            ax.set_ylim([0, 0.25])
            sns.despine(ax=ax)

        # Add a master legend
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right')

        # Hide any unused subplots
        for i in range(n_plots, len(axes)):
            axes[i].set_visible(False)

        # Adjust the spacing between subplots
        fig.tight_layout()
        # plt.show()

    return df, sp_df, df_under, df_over, df_spk_sim, plot_strikeout_distributions(df), df_results

if __name__ == '__main__':
    app_dfs()

