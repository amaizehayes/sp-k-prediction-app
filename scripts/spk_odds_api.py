import pandas as pd
import numpy as np
import re
import requests
import argparse
from datetime import datetime
from dateutil import parser, tz
import json
import time
import pytz

def get_api_data(api_key, sport, regions, markets, odds_format, date_format, bookmakers):
    """Gets baseball odds from the The Odds API.

    Args:
        api_key: The API key for The Odds API.
        sport: The sport to get odds for.
        regions: The regions to get odds for.
        markets: The markets to get odds for.
        odds_format: The format of the odds.
        date_format: The format of the dates.
        bookmakers: The bookmakers to get odds from.

    Returns:
        A dictionary of odds.
    """

    odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/odds', params={
        'api_key': api_key,
        'regions': regions,
        'markets': markets,
        'oddsFormat': odds_format,
        'dateFormat': date_format,
        'bookmakers': bookmakers
    })

    if odds_response.status_code != 200:
        raise Exception(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    odds_json = odds_response.json()
    print('Number of events:', len(odds_json))
    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    return odds_json

def get_event_ids(odds_json):
    """Gets the event IDs from the odds JSON.

    Args:
        odds_json: The odds JSON.

    Returns:
        A list of event IDs.
    """

    event_ids = []
    for event in odds_json:
        event_ids.append(event['id'])
    print('Grabbed number of event IDs:', len(event_ids))
    return event_ids


def get_props(event_ids, api_key, sport, regions, propmarkets, odds_format, date_format, bookmakers):
    """Gets the props for the given event IDs from the The Odds API.

    Args:
        event_ids: The event IDs to get props for.
        api_key: The API key for The Odds API.
        sport: The sport to get props for.
        regions: The regions to get props for.
        propmarkets: The markets to get props for.
        odds_format: The format of the odds.
        date_format: The format of the dates.
        bookmakers: The bookmakers to get props from.

    Returns:
        A list of props.
    """

    all_props = []
    for event_id in event_ids:
        props_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/events/{event_id}/odds', params={
            'api_key': api_key,
            'regions': regions,
            'markets': propmarkets,
            'oddsFormat': odds_format,
            'dateFormat': date_format,
            'bookmakers': bookmakers
        })

        if props_response.status_code != 200:
            raise Exception(f'Failed to get odds: status_code {props_response.status_code}, response body {props_response.text}')

        prop_json = props_response.json()
        all_props.append(prop_json)
    print('props have been grabbed')
    return all_props

def normalize_props(all_props):
    """Normalizes the props to a Pandas DataFrame.

    Args:
        all_props: The list of props to normalize.

    Returns:
        A Pandas DataFrame.
    """

    ndf = pd.json_normalize(
        all_props,
        record_path=["bookmakers", "markets", "outcomes"],
        meta=["id", "sport_key", "sport_title", "commence_time", "home_team", "away_team",
             ["bookmakers", "key"],
             ["bookmakers", "title"],
             ["bookmakers", "markets", "key"],
             ["bookmakers", "markets", "last_update"],
             ],
    )
    df = ndf[['name', 'description', 'price', 'point', 'commence_time']]
    df = df.pivot(index='description', columns='name', values=['price', 'point', 'commence_time'])
    df = df.reset_index()
    df.columns = ['name', 'over', 'under', 'prop_k', 'point', 'commence_time', 'ct_drop']
    df = df.drop(['point', 'ct_drop'], axis=1)
    print('props have been normalized')
    return df


def format_date(row):
    """Formats the commence_time column in a Pandas DataFrame to the %Y-%m-%d %H:%M:%S format.

    Args:
        row: A row from a Pandas DataFrame.

    Returns:
        The row with the commence_time column formatted.
    """

    dt = row['commence_time'].tz_convert(pytz.timezone('America/New_York'))
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_current_day_odds(api_key, sport, regions, markets, propmarkets, odds_format, date_format, bookmakers):
    """Retrieves baseball props odds from the The Odds API for the current day.

    Args:
        api_key: The API key for The Odds API.
        sport: The sport to get odds for.
        regions: The regions to get odds for.
        markets: The markets to get odds for.
        odds_format: The format of the odds.
        date_format: The format of the dates.
        bookmakers: The bookmakers to get odds from.

    Returns:
        A Pandas DataFrame containing the odds for the current day.
    """

    odds_json = get_api_data(api_key, sport, regions, markets, odds_format, date_format, bookmakers)
    event_ids = get_event_ids(odds_json)
    props = get_props(event_ids, api_key, sport, regions, propmarkets, odds_format, date_format, bookmakers)
    df = normalize_props(props)
    df['commence_time'] = pd.to_datetime(df['commence_time'])
    df['commence_time'] = df.apply(format_date, axis=1)
    df['commence_time'] = pd.to_datetime(df['commence_time'])
    today = datetime.now().date()
    df = df[df['commence_time'].dt.date == today]
    print('today\'s props have been uploaded')
    return df

if __name__ == '__main__':
    API_KEY = '78631749ab3c6ebcb3af78400a36298b'
    #backup 78631749ab3c6ebcb3af78400a36298b
    # edbcea9d1c4dd9fb281dd8d884eaedd6
    SPORT = 'baseball_mlb'
    REGIONS = 'us'
    MARKETS = 'h2h'
    ODDS_FORMAT = 'american'
    DATE_FORMAT = 'iso'
    BOOKMAKERS = 'fanduel'
    PROPMARKETS = 'pitcher_strikeouts'

    try:
        sp_prop_odds = get_current_day_odds(API_KEY, SPORT, REGIONS, MARKETS, PROPMARKETS, ODDS_FORMAT, DATE_FORMAT, BOOKMAKERS)
        #return today's odds into a csv file
        sp_prop_odds.to_csv('sp-k-prediction-app/output/sp_prop_odds_today.csv', index=False, header=True)
        #append today's odds to the history file
        sp_prop_odds.to_csv('sp-k-prediction-app/output/sp_prop_odds_history.csv', index=False, header=False, mode='a')
    except Exception as e:
        print(e)

