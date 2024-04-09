from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InsiderTrading

class TradingStrategy(Strategy):
    def __init__(self):
        # Specify the ticker for Aviation Archer
        self.ticker = "ACHR"  # Example ticker, replace with the actual ticker if different
        # Include InsiderTrading data for analysis
        self.data_list = [InsiderTrading(self.ticker)]

    @property
    def interval(self):
        # Define the interval for data fetching; daily intervals are common for insider activity analysis
        return "1day"

    @property
    def assets(self):
        # Return a list containing the ticker of interest
        return [self.ticker]

    @property
    def data(self):
        # Return the data sources (in this case, insider trading data)
        return self.data_list

    def run(self, data):
        # Initialize allocation; default to a neutral stance (e.g., 0.5 of the portfolio to this asset)
        allocation = 0.5

        # Extract the insider trading data for the specified ticker
        insider_activities = data[(InsiderTrading, self.ticker)]
        
        # Check the most recent insider activity, if available
        if insider_activities and len(insider_activities) > 0:
            latest_activity = insider_activities[-1] # Get the latest record

            if latest_activity['transactionType'] == 'Sale':
                # Insider selling detected; reduce allocation as it might indicate bearish outlook
                allocation *= 0.5  # Example reduction strategy, adjust based on your risk appetite
                
            elif latest_activity['transactionType'] == 'Purchase':
                # Insider buying detected; increase allocation as it might signal bullish outlook
                # Ensure the allocation does not exceed 1
                allocation = min(allocation * 1.5, 1)  # Example increase strategy, adjust as needed

        # Create and return the TargetAllocation object with the desired allocation
        return TargetAllocation({self.ticker: allocation})