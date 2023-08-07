import streamlit as st
import pandas as pd
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


# dist_df = pd.read_csv('/Users/patrick/Downloads/spk_viz_data.csv')
dist_df = pd.read_csv('/sp-k-prediction-app/spk_viz_data.csv')

# dist_df.drop(columns=['prop_k', 'x_under', 'x_over', 'over', 'under'], inplace=True)

def calculate_sum_poisson_range_col(row, col):
    if row[col] % 1 == 0.5:
        under = round(sum(row[f'Poisson_{i}'] for i in range(int(row[col] - .5) + 1)), 3)
        over = round(sum(row[f'Poisson_{i}'] for i in range(int(row[col] - .5) + 1, 21)), 3)
        return pd.Series({'under': under, 'over': over})
    else:
        under = round(sum(row[f'Poisson_{i}'] for i in range(int(row[col]))), 3)
        over = round(sum(row[f'Poisson_{i}'] for i in range(int(row[col] + 1), 21)), 3)
        return pd.Series({'under': under, 'over': over})

def convert_percentage_odds_to_moneyline(percentage_odds):
    if percentage_odds >= 0 and percentage_odds <= 1:
        if percentage_odds == 0.5:
            return -100
        elif percentage_odds < 0.5:
            return round((1 / percentage_odds - 1) * 100)
        else:
            return round((percentage_odds / (1 - percentage_odds)) * -100)
    else:
        raise ValueError("Percentage odds must be between 0 and 1.")


def calculate_new_column(row):
    fractional_part = row['xProp'] - int(row['xProp'])
    if fractional_part == 0.5:
        return None
    else:
        return 1 - (row['xPropU%'] + row['xPropO%'])

def round_to_nearest_half(value):
    return round(value * 2) / 2

def convert_percentage_odds_to_moneyline_with_vig_rounded(percentage_odds):
    vig = 0.02
    percentage_odds = percentage_odds + vig
    if percentage_odds >= 0 and percentage_odds <= 1:
        if percentage_odds <= .51 and percentage_odds >= .49:
            return -110
        elif percentage_odds < 0.48:
            moneyline = round((1 / percentage_odds - 1) * 100)
        else:
            moneyline = round((percentage_odds / (1 - percentage_odds)) * -100)
        # Round the calculated moneyline to the nearest 5
        remainder = moneyline % 5
        if remainder > 2.5:
            moneyline = moneyline + (5 - remainder)
        else:
            moneyline = moneyline - remainder
        return moneyline
    else:
        # raise ValueError("Percentage odds must be between 0 and 1.")
        return None

#declare expected prop
dist_df['xProp'] = dist_df['xK'].apply(lambda value: round_to_nearest_half(value))

#create adjustments based on the xprop
# dist_df['xProp+.5'] = dist_df['xProp'].apply(lambda value: value + .5)
# dist_df['xProp-.5'] = dist_df['xProp'].apply(lambda value: value - .5)
# dist_df['xProp+1'] = dist_df['xProp'].apply(lambda value: value + 1)

#calc poission ranges for each variations
dist_df[['xPropU%', 'xPropO%']] = dist_df.apply(lambda row: calculate_sum_poisson_range_col(row, 'xProp'), axis=1)
dist_df['xPropTie%'] = dist_df.apply(calculate_new_column, axis=1)
# dist_df[['xProp+.5U%', 'xProp+.5O%']] = dist_df.apply(lambda row: calculate_sum_poisson_range_col(row, 'xProp+.5'), axis=1)
# dist_df[['xProp-.5U%', 'xProp-.5O%']] = dist_df.apply(lambda row: calculate_sum_poisson_range_col(row, 'xProp-.5'), axis=1)
# dist_df[['xProp+1U%', 'xProp+1O%']] = dist_df.apply(lambda row: calculate_sum_poisson_range_col(row, 'xProp+1'), axis=1)

#Odds to moneylines
dist_df['xPropUml'] = dist_df['xPropU%'].apply(convert_percentage_odds_to_moneyline_with_vig_rounded)
dist_df['xPropOml'] = dist_df['xPropO%'].apply(convert_percentage_odds_to_moneyline_with_vig_rounded)
dist_df['xPropTieml'] = dist_df['xPropTie%'].apply(convert_percentage_odds_to_moneyline_with_vig_rounded)
# dist_df['xProp+.5Uml'] = dist_df['xProp+.5U%'].apply(convert_percentage_odds_to_moneyline_with_vig_rounded)
# dist_df['xProp+.5Oml'] = dist_df['xProp+.5O%'].apply(convert_percentage_odds_to_moneyline_with_vig_rounded)
# dist_df['xProp-.5Uml'] = dist_df['xProp-.5U%'].apply(convert_percentage_odds_to_moneyline_with_vig_rounded)
# dist_df['xProp-.5Oml'] = dist_df['xProp-.5O%'].apply(convert_percentage_odds_to_moneyline_with_vig_rounded)
# dist_df['xProp+1Uml'] = dist_df['xProp+1U%'].apply(convert_percentage_odds_to_moneyline_with_vig_rounded)
# dist_df['xProp+1Oml'] = dist_df['xProp+1O%'].apply(convert_percentage_odds_to_moneyline_with_vig_rounded)

cols = ['Name',
#  'Handedness',
 'Team',
 'Opponent',
 'xK',
 'xProp',
 'xPropU%',
 'xPropO%',
 'xPropTie%',
 'xPropUml',
 'xPropOml',
 'xPropTieml',
  'commence_time',]

dist_df = dist_df[cols]

results = []
for index1, player1 in dist_df.iterrows():
    for index2, player2 in dist_df.iterrows():
        if index1 != index2:
            u_x_u = convert_percentage_odds_to_moneyline(player1['xPropU%'] * player2['xPropU%'])
            u_x_o = convert_percentage_odds_to_moneyline(player1['xPropU%'] * player2['xPropO%'])
            o_x_u = convert_percentage_odds_to_moneyline(player1['xPropO%'] * player2['xPropU%'])
            o_x_o = convert_percentage_odds_to_moneyline(player1['xPropO%'] * player2['xPropO%'])

            results.append({
                'Player': player1['Name'],
                'OtherPlayer': player2['Name'],
                'UxU': u_x_u,
                'UxO': u_x_o,
                'OxU': o_x_u,
                'OxO': o_x_o
            })

results_df = pd.DataFrame(results)

print(results_df)




min_u_x_u = results_df['UxU'].idxmin()
min_u_x_o = results_df['UxO'].idxmin()
min_o_x_u = results_df['OxU'].idxmin()
min_o_x_o = results_df['OxO'].idxmin()

lowest_df = pd.DataFrame([
    results_df.loc[min_u_x_u],
    results_df.loc[min_u_x_o],
    results_df.loc[min_o_x_u],
    results_df.loc[min_o_x_o]
])

# Print the player names corresponding to the lowest values
print("Lowest UxU value:", results_df.loc[min_u_x_u, 'Player'], results_df.loc[min_u_x_u, 'OtherPlayer'], results_df.loc[min_u_x_u, 'UxU'])
print("Lowest UxO value:", results_df.loc[min_u_x_o, 'Player'], results_df.loc[min_u_x_o, 'OtherPlayer'], results_df.loc[min_u_x_o, 'UxO'])
print("Lowest OxU value:", results_df.loc[min_o_x_u, 'Player'], results_df.loc[min_o_x_u, 'OtherPlayer'], results_df.loc[min_o_x_u, 'OxU'])
print("Lowest OxO value:", results_df.loc[min_o_x_o, 'Player'], results_df.loc[min_o_x_o, 'OtherPlayer'], results_df.loc[min_o_x_o, 'OxO'])




def app():
    # mkdown = """
    # #### Future Iterations:
    # """
    st.header("xK Prop Parlay")
    st.dataframe(dist_df, height=900, hide_index=True)
    st.subheader("Parlays with Best Odds")
    st.dataframe(lowest_df, height=200, hide_index=True)
    st.subheader("All parlay variation odds")
    st.dataframe(results_df, height=900, hide_index=True)
    # st.markdown(mkdown)

if __name__ == '__main__':
    app()
