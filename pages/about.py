import streamlit as st

st.set_page_config(
    page_title="SP K About",
    page_icon="⚾",
    # layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': """# Created by Patrick Hayes
        Visit left hand menu for more information
        """,
        'Report a bug': "mailto:pfhayes@umich.edu",
    }
)

def app():
    abtmkdwn = """
    ### Objective:
    Showcase my sports analytics data science skills for future employers while creating an app for personal use.

    ### Summary of App:
    To identify value in the strikeout prop bet market for starting pitchers, and produce a streamlit app to display the data.

    The app displays the expected strikeout values and distributions for each pitcher and compares it to the over / under prop bet line based on these expected strikeout amounts.

    ### Navigating the App:
    **SPK App:** Home page with five tabs of data being displayed:
    - **Expected Ks**: Expected K predictions for each pitcher with their prop bet line
    - **K Distributions**: Poisson strikeout distributions for each pitcher
    - **Over / Under Bets**: Expected value for each pitcher's over / under prop bet
    - **Most K Odds**: Expected moneyline for each pitcher's most strikeouts prop bet
    - **Results**: Results of the previous day's games. Plenty more to come here.

    **About:** This page

    **Roadmap:** Future iterations of the app

    ### Approach Details (deatils a work in progress):
    - scrape probable starting pitchers from Rotogrinders and BaseballPress
    - scrape left and right team heandedness batting stats from MLB.com
    - scrape previous day pitcher stat lines from Baseball Reference
    - use API to pull over / under prop bets from FanDuel
    - use pybaseball to return pitcher stats for each probable starting pitcher
    - run calculation based on SP K%, SP average inning pitched, SP average batters faced per inning and normalized team handedness K%
    - calculate expected strikeout Poisson distributions for each pitcher
    - caculate sum of over or under Poisson distributions for each pitcher based on prop bet line
    - compare expected value to prop bet line over or under
    - identify over and under bets with most exepected value
    - use expected Ks data to simulate 10000 games and determine moneyline odds for pitcher with most Ks on the day
    - update yesterday's results from Baseball Reference stat line log
    - connect data to Streamlit to display all data which runs from GitHub repo
    - integrate PythonAnywhere to run scripts daily and update app (including pulling and pushing to GitHub)

    ### Data Sources:
    - [Baseball Reference](https://www.baseball-reference.com/)
    - [FanDuel](https://www.fanduel.com/)
    - [MLB](https://www.mlb.com/)
    - [Rotogrinders](https://rotogrinders.com/)
    - [Baseball Press](https://www.baseballpress.com/)
    - [PyBaseball](https://pypi.org/project/pybaseball/)
    - [Baseball Savant](https://baseballsavant.mlb.com/)
    - [Odds API](https://the-odds-api.com/)
    - [Streamlit](https://streamlit.io/)
    - [PythonAnywhere](https://www.pythonanywhere.com/)

    ### GitHub Repo:
    [SPK Repo](https://github.com/amaizehayes/sp-k-prediction-app)
    """
    st.header("About Page")
    st.markdown(abtmkdwn)

if __name__ == '__main__':
    app()
