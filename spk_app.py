# import pandas as pd
# import numpy as np
from datetime import date, datetime, timedelta
import pytz
# import random
# import math
# import seaborn as sns
# import matplotlib.pyplot as plt
import streamlit as st
import os
import spk_app_dfs

st.set_page_config(
    page_title="Probable Starting Pitcher Strikeouts",
    page_icon="⚾",
    # layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': """# Created by Patrick Hayes
        Visit left hand menu for more information
        """,
        'Report a bug': "mailto:pfhayes@umich.edu",
    }
)
st.set_option('deprecation.showPyplotGlobalUse', False)

tab1, tab2, tab3, tab4, tab5= st.tabs(["Expected Ks", "xK Distribution", "Over/Under Bets", "Most Ks Odds", "Results"])

def time_since_last_import():
    timestamp = os.path.getmtime('output/spk_today.csv')
    last_import = datetime.fromtimestamp(timestamp)
    eastern = pytz.timezone('US/Eastern')
    last_updated_est = eastern.localize(last_import)
    updated_minus_4_hours = last_updated_est - timedelta(hours=4)
    formatted_datetime = updated_minus_4_hours.strftime("%m-%d-%Y %H:%M %Z")
    return formatted_datetime

formatted_datetime = time_since_last_import()

# Get the current date and format it as a string
today = date.today().strftime("%A, %B %d, %Y")

def app():

    site_purpose = """*SP-K-Prediction identifies expected value in MLB starting pitcher strikeout bets*"""
    games_today = f"For MLB games played on {today}"
    last_update = f"Updated @ {formatted_datetime}"

    with tab1:
        st.write(site_purpose)
        st.markdown('First time here? Visit <a href="/about" target="_self">About</a> for more information', unsafe_allow_html=True)
        st.subheader("Starting Pitcher Expected Strikeouts (xK)")
        st.text(games_today)
        st.text(last_update)
        with st.expander('Glossary & Methodology (Click to Expand)'):
            st.markdown("""
            - **xK**: expected number of strikeouts *(now accounts for handedness of the pitcher and the opposing team)*
            - **prop_k**: FanDuel over / under prop bet for strikeouts
            """)
            st.write('The expected number of strikeouts is calculated using pitcher stats and opponent team batting stats. A further explanation is coming.')
        st.dataframe(sp_df, height=700, width=1000)
    with tab2:
        st.write(site_purpose)
        st.subheader("SP Expected Strikeout Distributions")
        st.text(games_today)
        st.text(last_update)
        st.write('A Poisson distribution plot of the expected number of strikeouts per pitcher')
        with st.expander('Glossary & Methodology (Click to Expand)'):
            st.markdown("""
            - **Poisson Distribution**: discrete probability distribution that expresses the probability of a given number of events occurring in a fixed interval of time or space if these events occur with a known constant mean rate and independently of the time since the last event
            - **xK**: expected number of strikeouts *(now accounts for handedness of the pitcher and the opposing team)*
            - **prop_k**: FanDuel over / under prop bet for strikeouts
            """)
        # fig = plot_strikeout_distributions(df)
        fig = plot_strikeout_distributions
        st.pyplot(fig)

    with tab3:
        st.write(site_purpose)
        st.subheader("Over/Under Bets")
        st.text(games_today)
        st.text(last_update)
        with st.expander('Glossary & Methodology (Click to Expand)'):
            st.markdown("""
            - **Expected Value**: the difference between the expected percent likelihood vs. the prop bet percent likelihood
            - **xK**: expected number of strikeouts *(now accounts for handedness of the pitcher and the opposing team)*
            - **prop_k**: FanDuel over / under prop bet for strikeouts
            - **more to come**
            """)
        st.subheader("Under Props")
        st.dataframe(df_under)
        st.subheader("Over Props")
        st.dataframe(df_over)
    with tab4:
        st.write(site_purpose)
        st.subheader("Most Ks Odds")
        st.text(games_today)
        st.text(last_update)
        st.write('The odds below are based on 10,000 simulations of the games being played today.')
        with st.expander('Glossary & Methodology (Click to Expand)'):
            st.markdown("""
            - **Probability**: the percent likelihood of the pitcher having the most strikeouts out of 10k simulations
            - **Moneyline**: the moneyline odds for the pitcher to have the most strikeouts in 10k simulations
            - **more to come**
            *Notice: Moneyline to be fixed for lines that should be negative*
            """)

        st.table(df_spk_sim)

    with tab5:
        st.write(site_purpose)
        st.subheader("Yesterday's SP K Results")
        st.text(last_update)
        with st.expander('Glossary & Methodology (Click to Expand)'):
            st.markdown("""
            - **xK**: expected number of strikeouts *(now accounts for handedness of the pitcher and the opposing team)*
            - **prop_k**: FanDuel over / under prop bet for strikeouts
            - **SO**: the amount of strikeouts a starter pitcher had yesterday
            - **IP**: the amount of innings pitched a starter pitcher had yesterday
            - **more to come**
            """)
        st.dataframe(df_results, height=900)


if __name__ == '__main__':
    df, sp_df, df_under, df_over, df_spk_sim, plot_strikeout_distributions, df_results = spk_app_dfs.app_dfs()
    app()
