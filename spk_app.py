import pandas as pd
import numpy as np
from datetime import date
import random
import math
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Probable Starting Pitcher Strikeouts",
    # page_icon="🧊",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# SP Strikeouts!"
    }
)

tab1, tab2, tab3, tab4 = st.tabs(["Expected Ks", "xK Distribution", "Over/Under Bets", "Most Ks Odds"])

st.set_option('deprecation.showPyplotGlobalUse', False)

df = pd.read_csv('spk_viz_data.csv')
sp_df = df[['Name', 'Team', 'Handedness', 'Opponent', 'xK', 'prop_k']]
df_under = pd.read_csv('spk_under_today.csv')
df_over = pd.read_csv('spk_over_today.csv')
df_spk_sim = pd.read_csv('spk_sim.csv')

### over/ under updates
df_over.rename(columns={'over_diff': 'expected value'}, inplace=True)
df_under.rename(columns={'under_diff': 'expected value'}, inplace=True)

def to_percent(x):
    x = x
    return "{:.1%}".format(x)

over_odds = ['expected value', 'over_odds', 'x_over']
under_odds = ['expected value', 'under_odds', 'x_under']

for col in over_odds:
    df_over[col] = df_over[col].apply(to_percent)

for col in under_odds:
    df_under[col] = df_under[col].apply(to_percent)

df_over = df_over[['Name', 'Team', 'Opponent', 'xK', 'prop_k', 'over', 'expected value',  'over_odds', 'x_over']]
df_under = df_under[['Name', 'Team', 'Opponent', 'xK', 'prop_k', 'under', 'expected value', 'under_odds', 'x_under']]

df_spk_sim['Percent'] = df_spk_sim['Percent'].apply(to_percent)
df_spk_sim.drop(columns=['Count'], inplace=True)

# Get the current date and format it as a string
today = date.today().strftime("%A, %B %d, %Y")

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
    plt.show()


def app():
    with tab1:
        st.header("Expected Strikeouts (xK)")
        st.text(f"For games played on {today}")
        st.text('The expected number of strikeouts is calculated using pitcher stats and opponent team batting stats. A further explanation is coming.')
        st.dataframe(sp_df, height=700, width=1000)
    with tab2:
        st.header("Expected Strikeout Distributions")
        st.text(f"For games played on {today}")
        st.text('A Poisson distribution plot of the expected number of strikeouts per pitcher')
        fig = plot_strikeout_distributions(df)
        st.pyplot(fig)

    with tab3:
        st.text(f"For games played on {today}")
        st.text('expected value is the difference between the expected percent likelihood vs. the prop bet percent likelihood')
        st.subheader("Under Prop Bets")
        st.dataframe(df_under)
        st.subheader("Over Prop Bets")
        st.dataframe(df_over)
    with tab4:
        st.header("Most Ks Odds")
        st.text(f"For games played on {today}")
        st.text('The odds below are based on 10,000 simulations of the games being played today.')
        st.text('Moneyline to be fixed for lines that should be negative.')
        st.dataframe(df_spk_sim)


if __name__ == '__main__':
    app()
