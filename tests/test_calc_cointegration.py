from stock_pair_cointegration.pair_cointegration import calc_cointegration
import os
import pandas as pd
import numpy as np

def test_calc_cointegration():
    cwd = os.getcwd()
    df1_path = os.path.join(cwd, 'test_data/KO.csv')
    df2_path = os.path.join(cwd, 'test_data/PEP.csv')

    df1 = pd.read_csv(df1_path)
    df2 = pd.read_csv(df2_path)

    result = calc_cointegration(df1, df2)
    print(result)


def test_calc_cointegration_with_mock_data():
    # mock the calc_cointegration function
    np.random.seed(42)

    # Step 1: Generate the first time series (random walk)
    n = 500  # Length of the series
    noise1 = np.random.normal(0, 1, n)
    y1 = np.cumsum(noise1)  # Random walk

    # Step 2: Generate the second time series as a linear combination of the first
    beta = 0.5  # Cointegration coefficient
    noise2 = np.random.normal(0, 1, n)
    y2 = beta * y1 + noise2  # Add some noise

    df1 = pd.DataFrame({
        'time': pd.date_range(start='1/1/2021', periods=n),
        'price': y1
    })
    df2 = pd.DataFrame({
        'time': pd.date_range(start='1/1/2021', periods=n),
        'price': y2
    })

    result = calc_cointegration(df1, df2, calculate_half_life=True, debug=True)
    print(result)

