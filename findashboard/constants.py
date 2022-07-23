FORMAT_PERCENTAGE = '{:,.2%}'
FORMAT_CURRENCY = "{:,.2f}"
FORMAT_DATETIME = '%d %B %Y'

URL_NEWS = "https://www.kontan.co.id/search/?search={}"

column_priceclose = "Close"
column_dividendamt = "value"
column_yieldpct = "yield_pct"

formats_dividend_yieldpct = {
    "Dividend Amount": FORMAT_CURRENCY,
    "Closing Price": FORMAT_CURRENCY,
    column_yieldpct: FORMAT_PERCENTAGE
}

# WAYSCRIPT

rsi_length = 14
bb_length, bb_std, bb_offset = 20, 2, 0

COLUMN_CLOSE = "Close"
COLUMN_RSI = f"RSI_{rsi_length}"
COLUMN_BBANDS_PERC = f"BBP_{bb_length}_{bb_std}.{bb_offset}"
COLUMN_PREVIOUS = "previous"
COLUMN_PROCESS_TOP = "process_top"
COLUMN_PROCESS_BOTTOM = "process_bottom"

VALUE_HIT = 1
VALUE_RECOVER = -1
VALUE_NEUTRAL = 0

VALUE_THRESHOLD_BOTTOM_RSI = 30
VALUE_THRESHOLD_TOP_RSI = 70
VALUE_THRESHOLD_BOTTOM_BBANDS_PERC = 0
VALUE_THRESHOLD_TOP_BBANDS_PERC = 1