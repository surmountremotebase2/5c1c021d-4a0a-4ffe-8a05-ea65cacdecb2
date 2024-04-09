from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.asset = "BTC-USD"  # Let's assume we're trading Bitcoin

    @property
    def assets(self):
        return [self.asset]

    @property
    def interval(self):
        return "1day"  # Daily intervals for our analysis

    def run(self, data):
        # Fetching the EMA for 10 days (short-term) and 50 days (long-term)
        ema_short = EMA(self.asset, data['ohlcv'], length=10)
        ema_long = EMA(self.asset, data['ohlcv'], length=50)

        # Fetching the RSI with a 14-day window
        rsi = RSI(self.asset, data['ohlcv'], length=14)

        # Initialization with no allocation
        allocation = 0

        if not ema_short or not ema_long or not rsi:
            # Insufficient data to compute indicators
            log("Insufficient data for EMA or RSI calculations.")
            return TargetAllocation({self.asset: allocation})

        # Trading logic (enter or exit trade)
        if ema_short[-1] > ema_long[-1] and rsi[-1] < 30:
            # We have a buy signal when short-term EMA is above long-term EMA and RSI is below 30
            allocation = 1  # Fully allocate to this asset
        elif ema_short[-1] < ema_long[-1] and rsi[-1] > 70:
            # We have a sell signal, moving to cash (0 allocation to asset) if the conditions are reversed
            allocation = 0

        # Logging the decision for review
        log(f"Allocating {allocation*100}% to {self.asset}")

        return TargetAllocation({self.asset: allocation})