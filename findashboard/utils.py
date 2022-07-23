import numpy as np
import pandas as pd
from findashboard.constants import column_priceclose


def find_dividend_dates_in_df_prices(df_dividends_, df_prices_):

    def backtrack_from_lastdate(date_, length_backtrack=10):
        for i in np.arange(length_backtrack):
            date_backtrack = date_ - pd.to_timedelta(i, unit='d')
            try:
                return df_prices_.loc[date_backtrack, column_priceclose]
            except:
                continue

    list_priceclose = []
    for date in df_dividends_.index:
        priceclose = backtrack_from_lastdate(date)
        list_priceclose.append(priceclose)

    return list_priceclose
