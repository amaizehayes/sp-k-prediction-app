import bs4
import requests
import pandas as pd
from datetime import date, datetime
import time
import re


def roto_sps():
    """
    Scrapes RotoGrinders for probable starters, their handedness, their opponent, and their RGID.
    """

    # Define constants
    URL = 'https://rotogrinders.com/lineups/mlb?site=fanduel'

    # Send a GET request to the URL and store the response
    response = requests.get(URL)

    # Check the response status code
    if response.status_code != 200:
        raise Exception(f'Failed to get response from URL: {URL}')

    # Get the content of the response
    html = response.content

    # Create a BeautifulSoup object to parse the HTML
    soup = bs4.BeautifulSoup(html, 'html.parser')

    lineup_cards = soup.find_all(attrs={'data-role': 'lineup-card'})

    # Iterate through the lineup cards
    lc = []
    for lineup_card in lineup_cards:
        pitcher_players = lineup_card.select('.pitcher.players .player-popup')
        pitcher_hand = lineup_card.select('.pitcher.players .meta.stats .stats')
        pitcher_id = lineup_card.select('.pitcher.players [data-url]')
        for player in pitcher_players[0]:
            for hand in pitcher_hand[0]:
                rgid = pitcher_id[0]['data-url'].split("-")[-1].split("?")[0]
                lc.append([player.text, hand.text.strip(), lineup_card['data-away'], lineup_card['data-home'], rgid])
        for player in pitcher_players[1]:
            for hand in pitcher_hand[1]:
                rgid = pitcher_id[1]['data-url'].split("-")[-1].split("?")[0]
                lc.append([player.text, hand.text.strip(), lineup_card['data-home'], lineup_card['data-away'], rgid])

    # Extract the date from the page header
    span_element = soup.select_one('#top > div > section > div > header > h1 > span')
    span_text = span_element.text.strip()
    date_str = span_text.split(' (')[0]
    date_obj = datetime.strptime(date_str, '%B %d, %Y')
    date_string = date_obj.date().strftime('%Y-%m-%d')

    # Create a DataFrame from the list of tuples, with columns for Name, Handedness, Team, Opponent, and Date
    rg_df = pd.DataFrame(lc, columns=['Name', 'Handedness', 'Team', 'Opponent', 'RGID'])
    rg_df['Date'] = date_string
    rg_df = rg_df[['Name', 'Handedness', 'Team', 'Opponent', 'Date', 'RGID']]

    # Return the number of probable starters scraped
    print('RotoGrinders scrape successful.')
    return rg_df

def baseball_press():
    """
    Scrapes baseball press for probable starters, their handedness, their opponent, and baseball ref and mlb ids.
    """

    # Define constants
    URL = 'https://www.baseballpress.com/lineups'

    # Send a GET request to the URL and store the response
    response = requests.get(URL)

    # Check the response status code
    if response.status_code != 200:
        raise Exception(f'Failed to get response from URL: {URL}')

    # Get the content of the response
    html = response.content

    # Create a BeautifulSoup object to parse the HTML
    soup = bs4.BeautifulSoup(html, 'html.parser')

    player_links = soup.select('.lineup-card-header .player-link')
    lc = []
    for player_link in player_links:
        mlbid = player_link['data-mlb']
        brefid = player_link['data-bref']
        try:
            name = player_link.select_one('.desktop-name').text
            # print(name)
        except AttributeError:
            name = player_link.text
            # print(name)
        lc.append([name, mlbid, brefid])

    # Create a DataFrame from the list of tuples, with columns for Name, mlbid and brefid
    bp_df = pd.DataFrame(lc, columns=['Name', 'mlbid', 'brefid'])

    def remove_middle_initial(name):
        if re.search(r'\b\w\.\s*[A-Z]\.\s*[A-Z]', name):
            return name
        else:
            return re.sub(r"\b\w\.\s*", "", name)

    bp_df['Name'] = bp_df['Name'].apply(remove_middle_initial)

    # Return the number of probable starters scraped
    print('Baseball Press scrape successful.')
    return bp_df

def combine_scrapes(rg_df, bp_df):
    """
    Combines the RotoGrinders and Baseball Press DataFrames. Outputs 2 csvs.
    """
    HISTORY_CSV = 'sp-k-prediction-app/output/probable_starter_history.csv'
    TODAY_CSV = 'sp-k-prediction-app/output/probable_starter_today.csv'

    df = pd.merge(rg_df, bp_df, on='Name', how='left')

    # Write the DataFrame to the history CSV file
    try:
        df.to_csv(HISTORY_CSV, index=False, mode='a', header=False)
    except Exception as e:
        print(e)

    # # Write the DataFrame to the standalone CSV file
    try:
        df.to_csv(TODAY_CSV, index=False, header=True)
    except Exception as e:
        print(e)

    return len(df)

if __name__ == '__main__':
    # Scrape the data
    combo_scrape = combine_scrapes(roto_sps(), baseball_press())

    # Print the number of probable starters scraped
    print(f'{combo_scrape} probable starters scraped successfully.')
