# Import necessary libraries.
import numpy as np
import pandas as pd
# from scipy.stats import poisson

# Define a function to generate a random number of strikeouts for a given pitcher.
def generate_strikeouts(pitcher):
  """Generates a random number of strikeouts for the given pitcher."""
  expected_strikeouts = pitching_stats_df[pitching_stats_df['Name'] == pitcher]['xK'].values[0]
  return np.random.poisson(expected_strikeouts)

# Define a function to simulate a day of baseball and return a DataFrame of the results.
def simulate_day(num_iterations):
  """Simulates a day of baseball and returns a DataFrame of the results."""
  # Get the list of starting pitchers.
  starting_pitchers = pitching_stats_df['Name'].values

  # Create a dictionary to store the number of times each pitcher had the most strikeouts.
  pitcher_counts = {}
  for pitcher in starting_pitchers:
    pitcher_counts[pitcher] = 0

  # Repeat steps 2-3 for a large number of iterations.
  for i in range(num_iterations):
    # Generate a random number of strikeouts for each pitcher.
    new_strikeouts_list = [generate_strikeouts(pitcher) for pitcher in starting_pitchers]

    # Keep track of the pitchers with the most strikeouts (including ties).
    max_strikeouts = max(new_strikeouts_list)
    max_pitchers = [pitcher for pitcher, strikeouts in zip(starting_pitchers, new_strikeouts_list) if strikeouts == max_strikeouts]
    for pitcher in max_pitchers:
      pitcher_counts[pitcher] += 1

  # Create a DataFrame from the pitcher_counts dictionary.
  df = pd.DataFrame(list(pitcher_counts.items()), columns=['Pitcher', 'Count'])

  # Calculate the percentage of times each pitcher had the most strikeouts.
  df['Percent'] = df['Count'] / num_iterations

  # Calculate the moneyline for each pitcher.
  df['Moneyline'] = df['Percent'].apply(lambda x: int(round(100 / x - 100, -1)))

  # Sort the DataFrame by the moneyline column.
  df.sort_values('Moneyline', ascending=True, inplace=True)

  return df


if __name__ == '__main__':
  pitching_stats_df = pd.read_csv('sp-k-prediction-app/output/spk_today.csv')

  # Simulate a day of baseball and print the results.
  df = simulate_day(10000)

  df.to_csv('spk_sim.csv', index=False, header=True)

  print(df)

