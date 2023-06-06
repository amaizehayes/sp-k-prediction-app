import pandas as pd
import pybaseball as pyb
import numpy as np
from scipy.stats import poisson
import warnings
import json

warnings.filterwarnings('ignore')

def clean_pyb_data(df):
    cols = ['IDfg', 'Name', 'GS', 'IP', 'TBF', 'K%']
    new_df = df[cols]
    print('pyb data grabbed')
    return new_df

def calculate_avg_ip(df, avg_ip):
    def pitch_avg_ip(row):
        if row['GS'] == 0 or row['IP'] / row['GS'] >= 6.5:
            return avg_ip * 0.95  # 0.95 arbitrary number to account for relievers or those with little SP history
        else:
            return row['IP'] / row['GS']

    df['avgIP'] = df.apply(pitch_avg_ip, axis=1)
    df.dropna(inplace=True)
    print('avgIP calculated')
    return df

def team_batting_ks(df_team_l, df_team_r):
    with open('sp-k-prediction-app/scripts/mlb-dict.json', 'r') as file:
        mlb_dict = json.load(file)
    df_team_l['Team'] = df_team_l['Team'].map(mlb_dict)
    df_team_r['Team'] = df_team_r['Team'].map(mlb_dict)
    mlb_k_avg_l = df_team_l['K%'].mean()
    mlb_k_avg_r = df_team_r['K%'].mean()
    team_bat_l = df_team_l
    team_bat_r = df_team_r
    print('team handedness ks calculated')
    return team_bat_l, team_bat_r, mlb_k_avg_l, mlb_k_avg_r

def merge_data(prob_sp_start, df, fg_sp_data, team_bat_l, team_bat_r, mlb_k_avg_l, mlb_k_avg_r):
    sp_df_merge = pd.merge(prob_sp_start, fg_sp_data[['key_mlbam', 'key_fangraphs']], left_on='mlbid', right_on='key_mlbam', how='left')
    sp_df_merge.drop(columns='key_mlbam', inplace=True)

    sp_pyb_merge = pd.merge(sp_df_merge, df, left_on='key_fangraphs', right_on='IDfg', how='left')
    sp_pyb_merge.drop(columns=['RGID', 'mlbid', 'brefid', 'key_fangraphs', 'IDfg', 'Name_y'], inplace=True)
    sp_pyb_merge = sp_pyb_merge.rename(columns={'Name_x': 'Name'})

    sp_pyb_merge['BF/IP'] = sp_pyb_merge['TBF'] / sp_pyb_merge['IP']

    #here for batting l/r splits
    df_l = sp_pyb_merge[sp_pyb_merge['Handedness'] == 'L']
    df_l = df_l.rename(columns={'K%': 'Team K%'})
    df_r = sp_pyb_merge[sp_pyb_merge['Handedness'] == 'R']
    df_r = df_r.rename(columns={'K%': 'Team K%'})

    df_l = pd.merge(df_l, df_team_l, left_on='Team', right_on='Team', how='left')
    df_r = pd.merge(df_r, df_team_r, left_on='Team', right_on='Team', how='left')
    df_l['MLB K%'] = mlb_k_avg_l
    df_r['MLB K%'] = mlb_k_avg_r
    df_l['OppvsMLBavg'] = df_l['Team K%'] / df_l['MLB K%']
    df_r['OppvsMLBavg'] = df_r['Team K%'] / df_r['MLB K%']
    df_l['xK'] = df_l['K%'] * df_l['OppvsMLBavg'] * df_l['BF/IP'] * df_l['avgIP']
    df_r['xK'] = df_r['K%'] * df_r['OppvsMLBavg'] * df_r['BF/IP'] * df_r['avgIP']
    df_concat = pd.concat([df_l, df_r])
    ccols = ['Name', 'Handedness', 'Team', 'Opponent', 'xK']
    df_concat = df_concat[ccols]
    df_concat.reset_index(drop=True, inplace=True)
    average_xK = df_concat['xK'].mean() * .95
    df_concat['xK'] = df_concat['xK'].fillna(average_xK)
    all_merged_df = df_concat
    print('all_merged_df_created')
    return all_merged_df

def load_data_files():
    avg_ip = pd.read_csv('sp-k-prediction-app/output/sp_log_2023.csv')['IP'].mean()
    prob_sp_start = pd.read_csv('sp-k-prediction-app/output/probable_starter_today.csv')
    sp_prop = pd.read_csv('sp-k-prediction-app/output/sp_prop_odds_today.csv')
    mlb_ids = list(prob_sp_start['mlbid'])
    fg_sp_data = pyb.playerid_reverse_lookup(mlb_ids, key_type='mlbam')
    df_team_l = pd.read_csv('sp-k-prediction-app/output/mlb_team_k_vs_l.csv')
    df_team_r = pd.read_csv('sp-k-prediction-app/output/mlb_team_k_vs_r.csv')
    print('data_files_loaded')
    return avg_ip, prob_sp_start, fg_sp_data, sp_prop, df_team_l, df_team_r

def calculate_poisson_distribution(prop_ou_df):
    range_nums = range(0, 21)
    # Define a lambda function to calculate the Poisson distribution for each row
    poisson_func = lambda row: [poisson.pmf(i, row['xK']) for i in range_nums]
    # Apply the lambda function to the DataFrame to get a list of lists containing the Poisson distributions
    poisson_dists = prop_ou_df.apply(poisson_func, axis=1)
    # Convert the list of lists to a DataFrame and add as new columns to the original DataFrame
    poisson_df = pd.DataFrame(poisson_dists.values.tolist(), columns=[f'Poisson_{i}' for i in range_nums])
    prop_ou_df = pd.concat([prop_ou_df, poisson_df], axis=1)
    print('poisson_distribution_calculated')
    return prop_ou_df

def calculate_sum_poisson_range(row):
    under = round(sum(row[f'Poisson_{i}'] for i in range(int(row['prop_k'] - .5) + 1)), 3)
    over = round(sum(row[f'Poisson_{i}'] for i in range(int(row['prop_k'] - .5) + 1, 21)), 3)
    return pd.Series({'under': under, 'over': over})


def convert_moneyline_to_percentage_odds(moneyline_odds):
    if moneyline_odds >= 0:
        return round(100 / (moneyline_odds + 100), 3)
    else:
        return round((moneyline_odds) / (moneyline_odds - 100), 3)

def prop_over_under(all_merged_df, sp_prop):
    prop_ou_df = pd.merge(all_merged_df, sp_prop, how='left', left_on='Name', right_on='name')
    prop_ou_df.dropna(inplace=True)
    prop_ou_df.drop(columns=['name'], inplace=True)
    prop_ou_df.rename(columns={'Team_x': 'Team'}, inplace=True)
    prop_ou_df['over'] = prop_ou_df['over'].astype(int)
    prop_ou_df['under'] = prop_ou_df['under'].astype(int)
    prop_ou_df['prop_k'] = round(prop_ou_df['prop_k'], 1)
    prop_ou_df.reset_index(drop=True, inplace=True)
    prop_ou_df[['x_under', 'x_over']] = prop_ou_df.apply(calculate_sum_poisson_range, axis=1)
    prop_ou_df['xK'] = prop_ou_df['xK'].round(2)
    #output for visualization
    prop_ou_df.to_csv('sp-k-prediction-app/spk_viz_data.csv', index=False)

    print('over under probabilities calculated')
    return prop_ou_df

def create_final_df(prop_ou_df):
    cols = ['Name', 'Handedness', 'Team', 'Opponent', 'xK', 'prop_k', 'over', 'under', 'x_under', 'x_over', 'commence_time']
    df_close = prop_ou_df[cols]

    # Write final data to CSV files
    # Calculate odds and differences
    df_close['over_odds'] = df_close['over'].apply(convert_moneyline_to_percentage_odds)
    df_close['under_odds'] = df_close['under'].apply(convert_moneyline_to_percentage_odds)
    df_close['under_diff'] = round(df_close['x_under'] - df_close['under_odds'], 3)
    df_close['over_diff'] = round(df_close['x_over'] - df_close['over_odds'], 3)

    # Determine betting decisions
    df_close['bet_under'] = np.where(df_close['under_diff'] > 0.02, 1, 0)
    df_close['bet_over'] = np.where(df_close['over_diff'] > 0.02, 1, 0)

    # Reorder columns for final output
    col_reorder = ['Name', 'Handedness', 'Team', 'Opponent', 'xK', 'prop_k', 'over', 'over_odds', 'x_over', 'over_diff', 'under', 'under_odds', 'x_under', 'under_diff', 'bet_over', 'bet_under', 'commence_time']
    df_final = df_close[col_reorder]

    print('final dataframe created!')

    return df_final

def generate_output_files(df_final):
    df_under = df_final[df_final['bet_under'] == 1].sort_values(by='under_diff', ascending=False)
    df_over = df_final[df_final['bet_over'] == 1].sort_values(by='over_diff', ascending=False)

    ucs = ['Name', 'Handedness', 'Team', 'Opponent', 'xK', 'prop_k', 'under', 'under_odds', 'x_under', 'under_diff', 'bet_under', 'commence_time']
    ocs = ['Name', 'Handedness', 'Team', 'Opponent', 'xK', 'prop_k', 'over', 'over_odds', 'x_over', 'over_diff', 'bet_over', 'commence_time']

    df_under = df_under[ucs]
    df_over = df_over[ocs]

    df_final.to_csv('sp-k-prediction-app/output/spk_today.csv', index=False)
    df_final.to_csv('sp-k-prediction-app/output/spk_history.csv', index=False, mode='a', header=False)

    df_under.to_csv('sp-k-prediction-app/spk_under_today.csv', index=False)
    df_over.to_csv('sp-k-prediction-app/spk_over_today.csv', index=False)

    return print('All files written successfully')

if __name__ == "__main__":
    # Load data files
    avg_ip, prob_sp_start, fg_sp_data, sp_prop, df_team_l, df_team_r = load_data_files()

    # Calculate team batting K% and MLB average K%
    team_bat_l, team_bat_r, mlb_k_avg_l, mlb_k_avg_r = team_batting_ks(df_team_l, df_team_r)

    # Clean and process data
    df = pyb.pitching_stats(2022, 2023, qual=1, split_seasons=0)
    df = clean_pyb_data(df)
    df = calculate_avg_ip(df, avg_ip)
    all_merged_df = merge_data(prob_sp_start, df, fg_sp_data, team_bat_l, team_bat_r, mlb_k_avg_l, mlb_k_avg_r)

    # Calculate Poisson distribution
    # prop_ou_df = prop_over_under(all_merged_df, sp_prop)

    prop_ou_df = calculate_poisson_distribution(all_merged_df)

    # Calculate over/under probabilities
    df_final = prop_over_under(prop_ou_df, sp_prop)

    # Create final dataframe
    df_final = create_final_df(df_final)

    # Generate output files
    generate_output_files(df_final)

