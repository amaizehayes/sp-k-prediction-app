import requests
import pandas as pd
from datetime import date, timedelta
import bs4

class BaseballScraper:
    def __init__(self):
        self.pitching_log_headers = ['Name','','','Age','Lev','Tm','\xa0','Opp','GS','W','L','SV','IP','H',
                        'R','ER','BB','SO','HR','HBP','GSc','AB','2B','3B','IBB','GDP','SF','SB',
                        'CS','PO','BF','Pit','Str','StL','StS','GB/FB','LD','PU']
        self.date = date.today()
        self.date_str = self.date.strftime('%Y-%m-%d')


    def scrape_data(self):
        '''
        function that scrapes bf for data for a given date
        '''
        url = f'https://www.baseball-reference.com/leagues/daily.fcgi?request=1&type=p&dates=yesterday&lastndays=7&since=2023-03-01&fromandto=2023-04-01.{self.date_str}&level=mlb&franch=ANY&stat=p%3AGS&stat_value=1'

        # bf_table_headers = []
        col_len = len(self.pitching_log_headers)

        #opens bf log and pulls the text from the Table Header tag
        headers = requests.get(url)

        headers_text = bs4.BeautifulSoup(headers.text, "lxml")
        bf_table_contents = headers_text('td')
        bf_table_contents_text = []
        for x in range(len(bf_table_contents)):
            bf_table_contents_text.append(bf_table_contents[x].getText())
        bf_table_contents_slice = [bf_table_contents_text[i:i + col_len] for i in range(0, len(bf_table_contents_text), col_len)]
        print('Scraping data for ' + self.date_str)
        return bf_table_contents_slice

    def write_bf_data(self):
        '''
        function that writes the scraped data to a csv
        '''
        bf_table_contents_slice = self.scrape_data()
        temp_df = pd.DataFrame(bf_table_contents_slice, columns = self.pitching_log_headers)
        temp_df['Date'] = self.date_str
        temp_df['Date'] = pd.to_datetime(temp_df['Date'])
        temp_df['Date'] = temp_df['Date'] - timedelta(days=1)
        temp_df.to_csv('output/sp_log_2023.csv', index=False, mode='a', header=False)
        print(f'{self.date_str} sp scrape done')

if __name__ == '__main__':
    bs = BaseballScraper()
    bs.write_bf_data()