# # TODO: Technical Indicators: RSI, Bollinger Bands, MA/EMA
#
# import streamlit as st
# import streamlit.components.v1 as components
# from datetime import datetime
#
# from findashboard.constants import HTML_TV_CHART, COLUMN_1_HEIGHT, DEFAULT_COLUMN_CONFIG
#
# with st.container(
#         **DEFAULT_COLUMN_CONFIG
# ):
#     st.sidebar.title("Stock Data")
#
#     name_stock = st.sidebar.text_input(
#         value="NYSE:O",
#         label="Stock Name",
#         max_chars=16,
#         help="Yahoo Finance stock name of the target company"
#     )
#
#     name_stock_tv = name_stock.split(".")[0]
#     name_stock_yf = name_stock.split(":")[-1]
#
#     date_start = st.sidebar.date_input(
#         value=datetime(year=datetime.now().year-5, month=1, day=1),
#         label="Start Date",
#         max_value=datetime.now().date(),
#         help="Left-bound date of the dividend history search"
#     )
#
#     date_end = st.sidebar.date_input(
#         value=datetime.now().date(),
#         label="End Date",
#         help="Right-bound date of the dividend history search"
#     )
#
# # TradingView Realtime
# with st.container(
#         **DEFAULT_COLUMN_CONFIG
# ):
#     st.header("Tradingview Chart")
#     components.html(
#         HTML_TV_CHART.format(
#             height=COLUMN_1_HEIGHT-15,
#             name_stock_tv=name_stock_tv
#         ),
#         height=COLUMN_1_HEIGHT
#     )
#
#
