import os

import pandas as pd

from stock_pair_cointegration.pair_cointegration import merge_df


def test_merge_df():
    cwd = os.getcwd()
    df1_path = os.path.join(cwd, 'test_data/KO.csv')
    df2_path = os.path.join(cwd, 'test_data/PEP.csv')

    df1 = pd.read_csv(df1_path)
    df2 = pd.read_csv(df2_path)

    assert len(df1) == 4886
    assert len(df1.columns) == 2
    assert 'date' in df1.columns
    assert 'price' in df1.columns

    assert len(df2) == 4904
    assert len(df2.columns) == 2
    assert 'date' in df2.columns
    assert 'price' in df2.columns

    result = merge_df(df1, df2)
    assert len(result) == 4886  # about 19 years data
    assert len(result.columns) == 3
    assert 'date' in result.columns
    assert 'price_1' in result.columns
    assert 'price_2' in result.columns
