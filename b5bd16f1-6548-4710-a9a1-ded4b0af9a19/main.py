from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AMZN"]  # Ticker for the asset we're interested in

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Analyzing data on a daily basis
        return "1day"

    def run(self, data):
        """
        Executes the trading strategy, analyzing the RSI to determine
        overbought or oversold conditions and sets allocations accordingly.
        
        :param data: The data made available to the strategy for analysis
        :return: TargetAllocation object specifying how to allocate investments
        """
        # Default allocation is 0 (no investment)
        allocation_dict = {ticker: 0 for ticker in self.tickers}
        
        # Calculate the RSI for "ACHR"
        rsi_values = RSI("ACHR", data["ohlcv"], length=14)
        
        if rsi_values is None or len(rsi_values) == 0:
            # If no RSI data available, do not invest
            return TargetAllocation(allocation_dict)
        
        # Get the most recent RSI value
        latest_rsi = rsi_values[-1]
        
        log(f"Latest RSI for ACHR: {latest_rsi}")
        
        # RSI thresholds for overbought and oversold conditions
        oversold_threshold, overbought_threshold = 30, 70
        
        # If RSI indicates oversold conditions, allocate 100% to "ACHR"
        if latest_rsi < oversold_threshold:
            allocation_dict["ACHR"] = 1.0
        
        # If RSI indicates overbought conditions, keep allocation at 0 (no action needed here)
        
        return TargetAllocation(allocation_dict)