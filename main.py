# -*- coding: utf-8 -*-
"""
API finance
"""

# 1. Library imports
import uvicorn
from fastapi import FastAPI
#import numpy as np
import json5
from fastapi.logger import logger
#from fastapi.responses import PlainTextResponse
import yfinance as yf
import pandas as pd
import numpy as np
#from statsmodels.tsa.arima.model import ARIMA

# 2. Create the app object
app = FastAPI()

@app.get('/')
async def price():
    try:        
        
        # Create a Yahoo Finance ticker objects
        stock_SP = yf.Ticker('ES=F')
        stock_10y_futures = yf.Ticker('ZNZ23.CBT')
        stock_3m_interest = yf.Ticker('^IRX')
        stock_10y_interest = yf.Ticker('^TNX')
        stock_vix_index = yf.Ticker('^VIX')
        
        # Fetch historical data for the stocks
        historical_data_SP = stock_SP.history(period='1y')
        historical_data_10y_futures = stock_10y_futures.history(period='1y')
        historical_data_3m_interest = stock_3m_interest.history(period='1y')
        historical_data_10y_interest = stock_10y_interest.history(period='1y')
        historical_data_vix_index = stock_vix_index.history(period='1y')
        
        # Extract the closing prices for 1 year
        prices_SP = historical_data_SP['Close']
        prices_10y_futures = historical_data_10y_futures['Close']
        prices_3m_interest = historical_data_3m_interest['Close']
        prices_10y_interest = historical_data_10y_interest['Close']
        prices_vix_index = historical_data_vix_index['Close']
        
        # Extract the most recent closing prices
        last_SP = historical_data_SP['Close'][-1]
        last_10y_futures = historical_data_10y_futures['Close'][-1]
        last_3m_interest = historical_data_3m_interest['Close'][-1]
        last_10y_interest = historical_data_10y_interest['Close'][-1]
        last_vix_index = historical_data_vix_index['Close'][-1]
        
        # Create a list of variable names and a list of values
        keys = ['S&P500 front month index futures prices', '10-year US Treasuries futures prices', 'US dollar 3-month interest rate', 'US dollar 10-year interest rate', 'VIX Index']
        values = [last_SP , last_10y_futures, last_3m_interest, last_10y_interest, last_vix_index]

        # Create a dictionary by pairing keys and values
        data_dict = dict(zip(keys, values))
        
        return data_dict
    
    except Exception as e:
        return {"error": str(e)}
    

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload