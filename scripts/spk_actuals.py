import pandas as pd
import unicodedata
from datetime import date, timedelta
from sklearn.metrics import mean_absolute_error, mean_squared_error
import logging

logging.basicConfig(level=logging.INFO)

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None

def normalize_name(name):
    normalized_name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    return normalized_name

def calculate_regression_metrics(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    mse = mean_squared_error(actual, predicted)
    rmse = mean_squared_error(actual, predicted, squared=False)
    return mae, mse, rmse

def evaluate_regression_metrics(df):
    mae, mse, rmse = calculate_regression_metrics(df['SO'], df['xK'])
    logging.info("Regression Metrics:")
    logging.info(f"MAE: {mae}")
    logging.info(f"MSE: {mse}")
    logging.info(f"RMSE: {rmse}")

def main():
    # Load data
    sp_log = load_data('output/sp_log_2023.csv')
    spk_history = load_data('output/spk_history.csv')

    if sp_log is None or spk_history is None:
        return

    # Date manipulation
    today = date.today()
    yesterday = today - timedelta(days=1)
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    # Data preprocessing
    sp_log['Date'] = pd.to_datetime(sp_log['Date'])
    spk_history['commence_time'] = pd.to_datetime(spk_history['commence_time'])

    spk_yesterday = spk_history[spk_history['commence_time'].dt.date == yesterday]
    sp_log_yesterday = sp_log[sp_log['Date'].dt.date == yesterday]

    sp_log_yesterday = sp_log_yesterday[['Name', 'SO', 'IP']]
    sp_log_yesterday['Name'] = sp_log_yesterday['Name'].apply(normalize_name)

    df = pd.merge(spk_yesterday, sp_log_yesterday, how='left', on='Name')
    df = df[['Name', 'xK', 'prop_k', 'SO', 'IP']]
    df.dropna(inplace=True)
    df['SO'] = df['SO'].astype(int)
    df.sort_values(by='SO', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv('spk_yesterday_results.csv', index=False, header=True)
    df.to_csv('output/spk_results_history.csv', index=False, header=False, mode='a')

    # Evaluate regression metrics
    evaluate_regression_metrics(df)

if __name__ == '__main__':
    main()

