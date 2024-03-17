import numpy as np
import yfinance as yf
import pandas_ta as ta
from datetime import datetime, timedelta
import pytz
import requests
from bs4 import BeautifulSoup

from findashboard.constants import column_yieldpct, column_priceclose, column_dividendamt
from findashboard.constants import URL_NEWS
from findashboard.constants import rsi_length, bb_length, bb_std, bb_offset
from findashboard.constants import COLUMN_RSI, COLUMN_BBANDS_PERC, COLUMN_CLOSE, COLUMN_PREVIOUS, COLUMN_PROCESS_TOP, COLUMN_PROCESS_BOTTOM
from findashboard.constants import VALUE_THRESHOLD_BOTTOM_BBANDS_PERC, VALUE_THRESHOLD_BOTTOM_RSI, VALUE_THRESHOLD_TOP_BBANDS_PERC, VALUE_THRESHOLD_TOP_RSI
from findashboard.utils import process_threshold_bottom, process_threshold_top


# TODO: Refactor DF out of other functions
def call_datareader(
    name_stock: str,
    date_start: datetime,
    date_end: datetime,
    yf_auto_adjust: bool
):
    if len(name_stock.split(" ")) == 1:
        ticker = yf.Ticker(name_stock)
    else:
        ticker = yf.Tickers(name_stock)
    return ticker.history(
        interval="1d",
        start=date_start,
        end=date_end,
        auto_adjust=yf_auto_adjust
    )


def generate_close_returnpctchange(
    name_stock: str,
    date_start: datetime,
    date_end: datetime,
    yf_auto_adjust: bool=False,
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
        date_start=date_start,
        date_end=date_end,
        yf_auto_adjust=yf_auto_adjust
    )
    df_close_changepct = df_prices[column_priceclose] \
        .resample(datetime_grouper).last() \
        .pct_change()\
        .reset_index(name="Return")
    df_close_changepct["Year"] = df_close_changepct["Date"].dt.strftime("%Y")
    df_close_changepct["Month"] = df_close_changepct["Date"].dt.strftime("%m - %B")
    df_close_grp = df_close_changepct.pivot_table(
        values=["Return"],
        index=["Year"],
        columns=["Month"],
        aggfunc=np.mean,
        margins=True,
        margins_name="0 - Average"
    )
    return df_close_grp.droplevel(level=0, axis=1).sort_index(ascending=False)


def generate_dividend_yieldpct(
    name_stock: str,
    date_start: datetime,
    date_end: datetime=datetime.now().date(),
    yf_auto_adjust: bool=False
):
    """
    Generate stock dividend history and dividend yield percent
    from Yahoo Finance data

    Parameters:
        name_stock (str): Yahoo Finance stock name of the target company
        date_start (datetime): left-bound date of the dividend history search
        date_end (datetime): right-bound date of the dividend history search

    Returns:
        df_yield (pd.DataFrame): df containing:
            dividend_amt: dividend given per stock unit
            closing_price: closing price of the stock at the given date
            yield_pct: dividend_amt divided by closing_price
    """

    df_yield = call_datareader(
        name_stock=name_stock,
        date_start=date_start,
        date_end=date_end,
        yf_auto_adjust=yf_auto_adjust
    )[[column_priceclose, column_dividendamt]]
    df_yield = df_yield[df_yield[column_dividendamt] != 0].copy()

    try:
        df_yield[column_yieldpct] = df_yield.apply(
            lambda row: row[column_dividendamt] / row[column_priceclose],
            axis=1
        )
        df_yield = df_yield.rename(columns={
            column_dividendamt: "Dividend Amount",
            column_priceclose: "Closing Price"
        })
        df_yield.index = df_yield.index.date
        df_yield.index.name = "Date"
        return df_yield.sort_index(ascending=False)
    except:
        return df_yield


def generate_dict_news(
    query: str,
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


def generate_annual_logreturn(
    list_name_stock: str,
    date_start: datetime,
    date_end: datetime=datetime.now().date(),
    yf_auto_adjust: bool=False
):
    df = call_datareader(
        name_stock=list_name_stock,
        date_start=date_start,
        date_end=date_end,
        yf_auto_adjust=yf_auto_adjust
    )


def cron_run_indicators(
        name_stock: str,
        yf_auto_adjust: bool=False
):
    date_end = datetime.now(pytz.utc).date() - timedelta(days=1)
    date_start = date_end - timedelta(weeks=8)

    df_stock = call_datareader(
        name_stock=name_stock,
        date_start=date_start,
        date_end=date_end,
        yf_auto_adjust=yf_auto_adjust
    )

    df_stock.ta.rsi(length=rsi_length, append=True)
    df_stock.ta.bbands(length=bb_length, std=bb_std, offset=bb_offset, append=True)

    X = df_stock[[COLUMN_CLOSE, COLUMN_RSI, COLUMN_BBANDS_PERC]].copy()
    X[f"{COLUMN_RSI}_{COLUMN_PREVIOUS}"] = X[COLUMN_RSI].shift(1)
    X[f"{COLUMN_BBANDS_PERC}_{COLUMN_PREVIOUS}"] = X[COLUMN_BBANDS_PERC].shift(1)

    X[f"{COLUMN_RSI}_{COLUMN_PROCESS_TOP}"] = X.apply(
        lambda row:
            process_threshold_top(
              column_now=row[COLUMN_RSI],
              column_previous=row[f"{COLUMN_RSI}_{COLUMN_PREVIOUS}"],
              value_threshold=VALUE_THRESHOLD_TOP_RSI
            ), axis=1
        )
    X[f"{COLUMN_RSI}_{COLUMN_PROCESS_BOTTOM}"] = X.apply(
        lambda row:
            process_threshold_bottom(
             column_now=row[COLUMN_RSI],
             column_previous=row[f"{COLUMN_RSI}_{COLUMN_PREVIOUS}"],
             value_threshold=VALUE_THRESHOLD_BOTTOM_RSI
            ), axis=1
        )

    X[f"{COLUMN_BBANDS_PERC}_{COLUMN_PROCESS_TOP}"] = X.apply(
        lambda row:
            process_threshold_top(
                column_now=row[COLUMN_BBANDS_PERC],
                column_previous=row[
                f"{COLUMN_BBANDS_PERC}_{COLUMN_PREVIOUS}"],
                value_threshold=VALUE_THRESHOLD_TOP_BBANDS_PERC
            ), axis=1
        )
    X[f"{COLUMN_BBANDS_PERC}_{COLUMN_PROCESS_BOTTOM}"] = X.apply(
        lambda row:
            process_threshold_bottom(
                column_now=row[COLUMN_BBANDS_PERC],
                column_previous=row[
                 f"{COLUMN_BBANDS_PERC}_{COLUMN_PREVIOUS}"],
                value_threshold=VALUE_THRESHOLD_BOTTOM_BBANDS_PERC
            ), axis=1
        )
    return X.tail(1)
