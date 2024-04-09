from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initializing the ticker for the strategy
        self.ticker = "ACHR"

    @property
    def assets(self):
        # Returning a list containing the asset this strategy will focus on
        return [self.ticker]

    @property
    def interval(self):
        # Defining the interval for which data is needed, here it's daily
        return "1day"

    def run(self, data):
        # Accessing the RSI data for the specified ticker
        rsi_values = RSI(self.ticker, data['ohlcv'], 14)

        allocation = 0  # Default allocation is 0, meaning no investment
        
        if rsi_values is not None and len(rsi_values) > 0:
            current_rsi = rsi_values[-1]  # Getting the most recent RSI value
            
            log(f"Current RSI for {self.ticker}: {current_rsi}")
            
            # RSI strategy:
            # - Buy (100% of allocated funds to this asset) if RSI is below 30 (oversold)
            # - Sell (0% allocation, i.e., fully exit position) if RSI is above 70 (overbought)
            if current_rsi < 30:
                allocation = 1  # Signaling to buy/hold the asset
            elif current_rsi > 70:
                allocation = 0  # Signaling to sell the asset
                
        return TargetAllocation({self.ticker: allocation})