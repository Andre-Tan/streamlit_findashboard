import streamlit as st
import streamlit.components.v1 as components

from datetime import datetime

from findashboard.generator_streamlit import generate_dividend_yieldpct, generate_close_returnpctchange, generate_dict_news
from findashboard.constants import FORMAT_PERCENTAGE
from findashboard.constants import formats_dividend_yieldpct

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    st.set_page_config(layout="wide")

    # Sidebar
    with st.container():

        st.sidebar.title("Stock Data")

        name_stock = st.sidebar.text_input(
            value="HEXA.JK",
            label="Stock Name",
            max_chars=16,
            help="Yahoo Finance stock name of the target company"
        )

        date_start = st.sidebar.date_input(
            value=datetime(year=2016, month=1, day=1),
            label="Start Date",
            max_value=datetime.now().date(),
            help="Left-bound date of the dividend history search"
        )

        date_end = st.sidebar.date_input(
            value=datetime(year=2022, month=12, day=31),
            label="End Date",
            help="Right-bound date of the dividend history search"
        )

    #TODO: refactor TradingView components
    col1, col2 = st.columns([3, 1])

    with col1:

        # TradingView Realtime
        with st.container():
            components.html(
                """
                    <!-- TradingView Widget BEGIN -->
                    <div class="tradingview-widget-container">
                      <div id="tradingview_38e3d"></div>
                      <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">Chart by TradingView</span></a></div>
                      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                      <script type="text/javascript">
                      new TradingView.widget(
                      {{
                      "width": 1050,
                      "height": 600,
                      "symbol": "IDX:{ticker}",
                      "interval": "D",
                      "timezone": "Etc/UTC",
                      "theme": "dark",
                      "style": "1",
                      "locale": "en",
                      "toolbar_bg": "#f1f3f6",
                      "enable_publishing": true,
                      "withdateranges": true,
                      "hide_side_toolbar": false,
                      "allow_symbol_change": true,
                      "studies": [
                        "BB@tv-basicstudies",
                        "RSI@tv-basicstudies"
                      ],
                      "container_id": "tradingview_38e3d"
                    }}
                      );
                      </script>
                    </div>
                    <!-- TradingView Widget END -->
                """.format(ticker=name_stock.split(".")[0]),
                width=1050,
                height=600,
            )

    with col2:

        # TradingView Fundamental
        with st.container():

            components.html(
                """
                    <!-- TradingView Widget BEGIN -->
                    <div class="tradingview-widget-container">
                      <div class="tradingview-widget-container__widget"></div>
                      <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/financials-overview/" rel="noopener" target="_blank"><span class="blue-text">Chart by TradingView</span></a></div>
                      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-financials.js" async>
                      {{
                      "symbol": "IDX:{ticker}",
                      "colorTheme": "dark",
                      "isTransparent": false,
                      "largeChartUrl": "",
                      "displayMode": "regular",
                      "width": 380,
                      "height": 600,
                      "locale": "en"
                    }}
                      </script>
                    </div>
                    <!-- TradingView Widget END -->
                """.format(ticker=name_stock.split(".")[0]),
                width=380,
                height=600
            )

    col3, col4 = st.columns([3, 1])

    with col4:
        # Recent News
        with st.container():
            st.header("Recent News")

            dict_news = generate_dict_news(
                query=name_stock.split(".")[0],
                limit=6
            )

            for values in dict_news.values():
                st.markdown("##### {} [link]({})".format(values["title"], values["url"]))
                st.caption(values["recency"])

    with col3:

        # TODO: Daily Closing Price
        # TODO: Fundamental Reports
        # TODO: Technical Indicators: RSI, Bollinger Bands, MA/EMA

        # Month-Yearly Returns
        with st.container():
            st.header("Close Price Difference Grouped By Year-Month")

            st.table(
                generate_close_returnpctchange(
                    name_stock=name_stock,
                    date_start=date_start,
                    date_end=date_end,
                    datetime_grouper="M"
                ) \
                    .style \
                    .applymap(lambda x: "background-color: #d65f5f" if x < 0 else "background-color: #5fba7d") \
                    .format(FORMAT_PERCENTAGE)
            )

        # Dividend Yields; Put this at the end because sometimes Yahoo do not have date in df_price
        with st.container():
            st.header("Dividend Yield History")

            st.table(
                generate_dividend_yieldpct(
                    name_stock=name_stock,
                    date_start=date_start,
                    date_end=date_end,
                    days_adjust=0
                ) \
                    .style.format(formats_dividend_yieldpct)
            )


