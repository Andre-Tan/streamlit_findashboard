FORMAT_PERCENTAGE = '{:,.1%}'
FORMAT_CURRENCY = "{:,.1f}"
FORMAT_DATETIME = '%d %B %Y'

URL_NEWS = "https://www.kontan.co.id/search/?search={}"

column_priceclose = "Close"
column_dividendamt = "Dividends"
column_yieldpct = "% Yield"

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

COLUMN_STOCK_NAME = "Stock Name"

VALUE_HIT = 1
VALUE_RECOVER = -1
VALUE_NEUTRAL = 0

VALUE_THRESHOLD_BOTTOM_RSI = 30
VALUE_THRESHOLD_TOP_RSI = 70
VALUE_THRESHOLD_BOTTOM_BBANDS_PERC = 0
VALUE_THRESHOLD_TOP_BBANDS_PERC = 1

COLUMN_1_HEIGHT = 600

DEFAULT_COLUMN_CONFIG = {
    "border": True
}

HTML_TV_CHART = """
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
        <div id="tradingview_38e3d"></div>
        <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">Chart by TradingView</span></a></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget(
        {{            
        "width": "100%",
        "height": {height},
        "symbol": "{name_stock_tv}",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "details": true,
        "calendar": true,
        "enable_publishing": false,
        "withdateranges": true,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "range": "60M",
        "studies": [
            "STD;Bollinger_Bands",
            "STD;RSI"
          ],
        "container_id": "tradingview_38e3d"
    }}
        );
    </script>
    </div>
    <!-- TradingView Widget END -->
"""