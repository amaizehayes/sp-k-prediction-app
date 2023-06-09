import streamlit as st

st.set_page_config(
    page_title="SP K Roadmap",
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
    mkdown = """
    #### Future Iterations:
    - ~~use handedness for team strikeouts, requires manual scrape from FanGraphs~~
    - ~~fix moneyline + sign and remove, from odds~~
    - ~~add glossary and methodology for each tab/page~~
    - ~~move scripts to the cloud via PythonAnywhere~~
    - update historical data based on game logs (fix logs for April games)
    - use a ratio of 2022 and 2023 data for pitchers (use game logs at a future state)
    - fangraphs with -1 for some player ids. need to fix
    - pull in player specific game logs for 2022
    - create historical record for expected value prop bets, with $$ won/lost
    - record closing line value for prop bets
    """
    st.header("Roadmap")
    st.markdown(mkdown)

if __name__ == '__main__':
    app()
