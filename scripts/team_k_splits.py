import pandas as pd
import requests
import collections as co
from bs4 import BeautifulSoup
import bs4


def scrape_and_save_data(url, output_file):
    r = requests.get(url)
    html = r.content

    soup = bs4.BeautifulSoup(html, 'html.parser')

    table = soup.find('section', {'class': 'stats-type-body stats-type-teamHitting'})
    table_body = table.find('tbody')
    table_head = table.find('thead')

    header = []
    for th in table_head.find_all('th'):
        key = th.get_text()
        header.append(key)

    trlist = []
    for tr in table_body.find_all('tr'):
        trlist.append(tr)

    find_teams = soup.find_all(class_="bui-link")
    team_list = []
    for team in find_teams:
        aria_label = team.get("aria-label")
        if aria_label:
            team_list.append(aria_label)

    listofdicts = []
    for row in trlist:
        the_row = []
        for td in row.findAll('td'):
            the_row.append(td.text)
        od = co.OrderedDict(zip(header, the_row))
        listofdicts.append(od)

    standf = pd.DataFrame(listofdicts)
    standf.insert(0, 'Team', team_list)
    new_cols = ['Team', 'Leage', 'Games', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'SO', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS']
    standf.columns = new_cols
    standf = standf[['Team', 'AB', 'BB', 'SO']]
    standf['AB'] = standf['AB'].astype(int)
    standf['BB'] = standf['BB'].astype(int)
    standf['SO'] = standf['SO'].astype(int)
    standf['PA'] = standf['AB'] + standf['BB']
    standf['K%'] = standf['SO'] / standf['PA']
    standf.sort_values(by=['Team'], ascending=True, inplace=True)

    standf.to_csv(output_file, index=False)

if __name__ == '__main__':
    # Scrape the data
    url_l = "https://www.mlb.com/stats/team/batting-average?split=vl"
    output_l = "output/mlb_team_k_vs_l.csv"
    scrape_and_save_data(url_l, output_l)

    url_r = "https://www.mlb.com/stats/team/batting-average?split=vr"
    output_r = "output/mlb_team_k_vs_r.csv"
    scrape_and_save_data(url_r, output_r)

    # Print the number of probable starters scraped
    print("team strikeout percent splits scraped successfully.")