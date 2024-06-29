import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_nifty_data(nifty_symbols):
    # Define Nifty 50 symbols (you can extend this list with more symbols)
   
    # Set the period for historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 year of data
   
    # Fetch historical data for all symbols
    data = {}
    for symbol in nifty_symbols:
        data[symbol] = yf.download(symbol, start=start_date, end=end_date)
   
    return data

def calculate_momentum(data):
    # Calculate 6-month returns as a measure of momentum
    momentum_scores = {}
    for symbol, df in data.items():
        try:
            df['6M_Return'] = df['Adj Close'].pct_change(periods=126)  # Approx. 6 months (252 trading days in a year)
            momentum_scores[symbol] = df['6M_Return'].iloc[-1]
        except:
            momentum_scores[symbol] = np.nan  # Handle cases where data is insufficient
   
    # Rank stocks by their 6-month returns
    momentum_stocks = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
    return momentum_stocks

def find_value_stocks(data):
    # Fetch current P/E ratios for value investing
    pe_ratios = {}
    for symbol in data.keys():
        ticker = yf.Ticker(symbol)
        try:
            pe_ratios[symbol] = ticker.info['trailingPE']
        except KeyError:
            pe_ratios[symbol] = np.nan  # Handle missing data
   
    # Rank stocks by their P/E ratio (lower P/E suggests better value)
    value_stocks = sorted(pe_ratios.items(), key=lambda x: x[1])
    return value_stocks