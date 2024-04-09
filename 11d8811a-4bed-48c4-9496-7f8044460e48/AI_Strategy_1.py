from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):

    def __init__(self):
        # Define the single asset we are interested in - Amazon (AMZN)
        self.ticker = "AMZN"
        # Option strike price buffer - a percentage above the current market price
        self.strike_price_buffer = 0.05
        # Moving average length
        self.ma_length = 20

    @property
    def assets(self):
        # Strategy is designed for Amazon
        return [self.ticker]

    @property
    def interval(self):
        # Use daily data for assessing conditions
        return "1day"

    def run(self, data):
        """
        The strategy logic checks if the 20-day SMA of AMZN's price is trending upwards.
        If the trend is positive, we prepare to sell a covered call by setting aside the
        equivalent cash necessary for 100 shares (standard option contract size).
        The call's strike price is set 5% above the current price.
        If the SMA is not trending upwards, no action is taken (i.e., no cash is set aside).
        """
        # Initialize allocation - none to begin with
        allocation = {self.ticker: 0}
        
        # Get the moving average of the Amazon stock
        sma = SMA(self.ticker, data["ohlcv"], self.ma_length)
        
        if len(sma) > 1 and sma[-1] > sma[-2]:
            # If the SMA is trending upwards, indicate potential for covered call
            log(f"Potential for covered call on {self.ticker}. SMA is trending upwards.")
            
            # Calculate the strike price for the covered call as a buffer above the current price
            current_price = data["ohlcv"][-1][self.ticker]["close"]
            strike_price = current_price * (1 + self.strike_price_buffer)
            log(f"Setting strike price for covered call at {strike_price}.")
            
            # Assume we're setting aside the equivalent cash for 100 shares as '1' allocation.
            # In practice, this step would involve selling a call option, but here we're just indicating readiness.
            allocation[self.ticker] = 1
        else:
            log(f"No action for {self.ticker}. SMA not trending upwards.")

        return TargetAllocation(allocation)