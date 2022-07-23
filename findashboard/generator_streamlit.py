import pandas as pd
import numpy as np
from pandas_datareader import data
from pandas.tseries.offsets import BDay
from datetime import datetime

from findashboard.constants import column_yieldpct, column_priceclose, column_dividendamt
from findashboard.constants import URL_NEWS

from findashboard.utils import find_dividend_dates_in_df_prices

import requests
from bs4 import BeautifulSoup


def call_datareader(name_stock, date_start, date_end, data_source):
    return data.DataReader(
        name=name_stock,
        data_source=data_source,
        start=date_start,
        end=date_end
    )


def generate_dividend_yieldpct(
        name_stock: str,
        date_start: datetime,
        date_end: datetime,
        days_adjust: int,
):
    """
    Generate stock dividend history and dividend yield percent
    from Yahoo Finance data

    Parameters:
        name_stock (str): Yahoo Finance stock name of the target company
        date_start (datetime): left-bound date of the dividend history search
        date_end (datetime): right-bound date of the dividend history search
        days_adjust (int): number of days to adjust from dividend recording-date to cum-date
            Will automatically adjust for working days

    Returns:
        df_yield (pd.DataFrame): df containing:
            dividend_amt: dividend given per stock unit
            closing_price: closing price of the stock at the given date
            yield_pct: dividend_amt divided by closing_price
    """

    df_prices = call_datareader(
        name_stock=name_stock,
        data_source="yahoo",
        date_start=date_start,
        date_end=date_end
    )

    df_dividends = call_datareader(
        name_stock=name_stock,
        data_source="yahoo-dividends",
        date_start=date_start,
        date_end=date_end
    )

    # adjust to last working day
    df_dividends.index -= BDay(days_adjust)

    df_yield = pd.DataFrame({
        column_dividendamt: df_dividends[column_dividendamt],
        column_priceclose: find_dividend_dates_in_df_prices(df_dividends, df_prices)
    })

    df_yield[column_yieldpct] = df_yield.apply(
        lambda row: row[column_dividendamt] / row[column_priceclose],
        axis=1
    )

    df_yield = df_yield.rename(columns={
        column_dividendamt: "Dividend Amount",
        column_priceclose: "Closing Price"
    })

    df_yield.index = df_yield.index.strftime('%d %B %Y')

    return df_yield


def generate_close_returnpctchange(
        name_stock: str,
        date_start: datetime,
        date_end: datetime,
        datetime_grouper: str = "M"
):
    """
    Generate stock return in a matrix divided by month and year
    from Yahoo Finance data

    Parameters:
        name_stock (str): Yahoo Finance stock name of the target company
        date_start (datetime): left-bound date of the dividend history search
        date_end (datetime): right-bound date of the dividend history search
        datetime_grouper (string): string shortcut for Pandas resample function

    Returns:
        df_close_grp (pd.DataFrame): df containing monthly returns indexed by year and month
    """

    df_prices = call_datareader(
        name_stock=name_stock,
        data_source="yahoo",
        date_start=date_start,
        date_end=date_end
    )

    df_close_changepct = df_prices["Close"] \
        .resample(datetime_grouper).last() \
        .pct_change()\
        .reset_index(name="Return")

    df_close_changepct["Year"] = df_close_changepct["Date"].dt.year
    df_close_changepct["Month"] = df_close_changepct["Date"].dt.month

    df_close_grp = df_close_changepct.pivot_table(
        values=["Return"],
        index=["Year"],
        columns=["Month"],
        aggfunc=np.mean,
        margins=False
    )

    return df_close_grp.droplevel(level=0, axis=1)


def generate_dict_news(
        query:str,
        limit: int=5
):
    datas = requests.get(URL_NEWS.format(query))
    soup = BeautifulSoup(datas.text, 'html.parser')
    list_news = soup.find("div", {"class": "list-berita"})

    dict_news = {}

    for i, link in enumerate(list_news.find_all("li")[0:limit]):
        dict_news[i] = {}
        dict_news[i]["title"] = link.find("img").attrs["alt"]
        dict_news[i]["recency"] = link.find("span", {"class": "font-gray"}) .text # .replace("|", "").strip()
        dict_news[i]["url"] = "https:{}".format(link.find("a").attrs["href"])

    return dict_news

