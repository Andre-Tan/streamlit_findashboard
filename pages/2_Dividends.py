# import streamlit as st
# from datetime import datetime
#
# from findashboard.generator_streamlit import generate_dividend_yieldpct, generate_close_returnpctchange
# from findashboard.constants import FORMAT_PERCENTAGE, DEFAULT_COLUMN_CONFIG
# from findashboard.constants import formats_dividend_yieldpct
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
#
# # Month-Yearly Returns
# with st.container(
#         **DEFAULT_COLUMN_CONFIG
# ):
#     st.header("Close Price Difference Grouped By Year-Month")
#
#     st.dataframe(
#         generate_close_returnpctchange(
#             name_stock=name_stock_yf,
#             date_start=date_start,
#             date_end=date_end,
#             datetime_grouper="M"
#         ) \
#             .style \
#             .applymap(lambda x: "background-color: #d65f5f" if x < 0 else "background-color: #5fba7d") \
#             .format(FORMAT_PERCENTAGE),
#         use_container_width=True
#     )
#
# # Dividend Yields; Put this at the end because sometimes Yahoo do not have date in df_price
# with st.container(
#         **DEFAULT_COLUMN_CONFIG
# ):
#     st.header("Dividend Yield History")
#
#     st.dataframe(
#         generate_dividend_yieldpct(
#             name_stock=name_stock_yf,
#             date_start=date_start,
#             date_end=date_end
#         ) \
#             .style.format(formats_dividend_yieldpct),
#         use_container_width=True
#     )
