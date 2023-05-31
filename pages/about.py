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

    ### Approach Details (work in progress):
    - scrape SP probables from two sites (Rotogrinders and BaseballPress)
    - scrape team batting stats from Baseball Reference via pybaseball package
    - scrape pitcher stats from Baseball Reference via pybaseball package
    - calculate expected strikeout distributions for each pitcher
    - use API to pull over / under prop bets from FanDuel
    - calculate expected value for each pitcher
    - create a streamlit app to display the data

    ### Data Sources:
    - [Baseball Reference](https://www.baseball-reference.com/)
    - [FanDuel](https://www.fanduel.com/)
    - [Rotogrinders](https://rotogrinders.com/)
    - [Baseball Press](https://www.baseballpress.com/)
    - [PyBaseball](https://pypi.org/project/pybaseball/)
    - [Baseball Savant](https://baseballsavant.mlb.com/)
    - [Odds API](https://the-odds-api.com/)
    """
    st.header("About Page")
    st.markdown(abtmkdwn)

if __name__ == '__main__':
    app()
