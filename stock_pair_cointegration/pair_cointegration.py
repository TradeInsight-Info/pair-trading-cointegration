from matplotlib import pyplot as plt
from arch.unitroot import engle_granger
from arch.unitroot.cointegration import FullyModifiedOLS
from numpy import nan as NaN, log, mean, std
from pandas import DataFrame, Series, merge
from statsmodels.api import OLS

from stock_pair_cointegration.figure_to_svg_string import figure_to_svg_string


def merge_df(df1: DataFrame, df2: DataFrame):
    df = merge(df1, df2, on='time', suffixes=('_1', '_2'))
    # drop rows with empty values
    df = df.dropna()
    return df


def cal_half_life(z: Series):
    prevz = z.shift()
    dz = z - prevz
    dz = dz[1:, ]
    prevz = prevz[1:, ]
    model2 = OLS(dz, prevz - mean(
        prevz))  # This term is the spread series centered around its mean. By subtracting the mean of prevz, this removes any constant trend in the spread and centers it around zero. In time series analysis, this step is essential when testing for mean reversion, as it helps to see if deviations from the mean revert back to zero. Ornstein-Uhlenbeck formula_ see note
    results2 = model2.fit()
    theta = results2.params
    return log(2) / theta


def get_z(series1: Series, series2: Series, hr: float, c: float):
    return series1 - (hr * series2 + c)


def calc_cointegration(df1: DataFrame, df2: DataFrame, days=None, calculate_half_life=False, debug=False):
    merged_df = merge_df(df1, df2)
    if days:
        days = int(days)
        merged_df = merged_df[-days:]

    merged_df = merged_df.dropna()
    price1 = merged_df['price_1']
    price2 = merged_df['price_2']

    result = engle_granger(price1, price2, trend="c")
    print('co-integration test:', result)

    output = {
        'test_statics': result.stat,
        'pvalue': result.pvalue,
        'critical_values': list(result.critical_values),
        'hedge_ratio': NaN,
        'constant': NaN,
        'half_life': NaN,
    }
    is_co_integrated = result.pvalue < 0.05

    if not is_co_integrated:
        fig, axes = plt.subplots(1, 2, figsize=(15, 10))

        result.plot(axes=axes[0])
        axes[1].plot(price1.pct_change(), label='close_1')
        axes[1].plot(price2.pct_change(), label='close_2')
        # title
        axes[1].set_title('Price Change %')
        axes[1].legend()

    if is_co_integrated:
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        result.plot(axes=axes[0, 0])
        axes[0, 0].set_title('Cointegration Test')
        axes[0, 1].plot(price1.pct_change(), label='Stock 1')
        axes[0, 1].plot(price2.pct_change(), label='Stock 2')
        # title
        axes[0, 1].set_title('Price Change %')
        axes[0, 1].legend()

        # OLD Fit and get hedge ratio and constant
        model = FullyModifiedOLS(price1, price2, trend='c')  # Ordinary Least Squares
        res = model.fit()
        print(res.summary(), res.params)
        hedge_ratio = res.params.iloc[0]  # slot
        con = res.params.iloc[1]


        z = get_z(price1, price2, hedge_ratio, con)
        if calculate_half_life:
            # calculate half life
            hl = cal_half_life(z)
            print('Half Life:', hl)
            output['half_life'] = hl['x1']
        output['hedge_ratio'] = hedge_ratio
        output['constant'] = con

        z_standard = (z - mean(z)) / std(z)

        axes[1, 0].plot(price1, label='Stock 1')
        axes[1, 0].plot(price2 * hedge_ratio + con, label='Stock 2 Hedged')
        axes[1, 0].set_title('Price1 and Price 2 Hedged')
        axes[1, 0].legend()

        axes[1, 1].plot(z_standard, label='spread standardized')
        axes[1, 1].axhline(2, color='r', linestyle='--', label='2 * std')
        axes[1, 1].axhline(-2, color='r', linestyle='--', label='-2 * std')
        axes[1, 1].axhline(1, color='g', linestyle='--', label='1 * std')
        axes[1, 1].axhline(-1, color='g', linestyle='--', label='-1 * std')
        axes[1, 1].set_title('Spread Standardized')
        axes[1, 1].legend()

    output['figure'] = figure_to_svg_string(fig, save=debug)

    return output


if __name__ == '__main__':
    import os
    import pandas as pd

    cwd = os.getcwd()
    df1_path = os.path.join(cwd, '../tests/test_data/KO.csv')
    df2_path = os.path.join(cwd, '../tests/test_data/PEP.csv')

    df1 = pd.read_csv(df1_path, header=0, )[-2500:-2400]
    df2 = pd.read_csv(df2_path, header=0,  )[-2500:-2400]

    result = calc_cointegration(df1, df2, calculate_half_life=True, debug=True)
    print(result)
