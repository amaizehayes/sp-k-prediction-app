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
    # with st.sidebar:
    #     st.write('test')
    #### mark down test here
    tab1kd = """
    #### Objective:
    to showcase data science skills in creating a sports analytics app
    #### Method:
    - scrape SP probables from two sites (Rotogrinders and BaseballPress)
    - scrape team batting stats from Baseball Reference via pybaseball package
    - scrape pitcher stats from Baseball Reference via pybaseball package
    - calculate expected strikeout distributions for each pitcher
    - use API to pull over / under prop bets from FanDuel
    - calculate expected value for each pitcher
    - create a streamlit app to display the data
    """
    st.header("About Page")
    st.markdown(tab1kd)

if __name__ == '__main__':
    app()
