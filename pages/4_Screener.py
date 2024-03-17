import pandas as pd
import streamlit as st

from findashboard.constants import DEFAULT_COLUMN_CONFIG
from findashboard.generator_streamlit import cron_run_indicators
from findashboard.constants import COLUMN_RSI, COLUMN_BBANDS_PERC, COLUMN_PROCESS_TOP, COLUMN_PROCESS_BOTTOM
from findashboard.constants import COLUMN_STOCK_NAME


with st.container(
    **DEFAULT_COLUMN_CONFIG
):
    st.header("Put stock name to screen here")
    df = pd.DataFrame([
        {COLUMN_STOCK_NAME: "VOO"},
        {COLUMN_STOCK_NAME: "QQQ"},
        {COLUMN_STOCK_NAME: "O"}
    ])

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True
    )

with st.container(
    **DEFAULT_COLUMN_CONFIG
):
    st.header("Screening with BB and RSI will automatically happen here")
    name_stock_uniques = edited_df[COLUMN_STOCK_NAME].tolist()

    df = pd.concat([cron_run_indicators(name_stock) for name_stock in name_stock_uniques])
    df["name_stock"] = name_stock_uniques

    df_display = df[
        df[[f"{COLUMN_RSI}_{COLUMN_PROCESS_TOP}",
            f"{COLUMN_RSI}_{COLUMN_PROCESS_BOTTOM}",
            f"{COLUMN_BBANDS_PERC}_{COLUMN_PROCESS_TOP}",
            f"{COLUMN_BBANDS_PERC}_{COLUMN_PROCESS_BOTTOM}"
          ]].any(axis=1)
    ]

    st.dataframe(
        df_display
    )
