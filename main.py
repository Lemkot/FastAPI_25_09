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
import requests
from bs4 import BeautifulSoup
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
        
        # Extract the most recent closing price
        last_SP = historical_data_SP['Close'][-1]
        last_10y_futures = historical_data_10y_futures['Close'][-1]
        last_3m_interest = historical_data_3m_interest['Close'][-1]
        last_10y_interest = historical_data_10y_interest['Close'][-1]
        last_vix_index = historical_data_vix_index['Close'][-1]
        
        
        # Extract 2-year US interest rate
        
        csv_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2023/all?field_tdr_date_value=2023&type=daily_treasury_yield_curve&page&_format=csv'

        req = requests.get(csv_url, verify=False)
        url_content = req.content

        csv_file = open('2023_rates.csv', 'wb')
        csv_file.write(url_content)
        csv_file.close()

        rates_2023 = pd.read_csv('2023_rates.csv')
        today_rates_all = rates_2023.head(1)
        today_rate_2y = today_rates_all['2 Yr'].iloc[0]
        
        # Extract 10-year German Bund price
        
        url = "https://www.marketwatch.com/investing/bond/tmbmkde-10y?countrycode=bx"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        yield_element = soup.find("bg-quote", class_="value")
        bund_value_str = yield_element.text.strip() if yield_element else "Not found"
        bund_value = float(bund_value_str)
        
        # Create a list of variable names and a list of values
        keys = ['S&P500 front month index futures prices', '10-year US Treasuries futures prices', 'US dollar 3-month interest rate', 'US dollar 10-year interest rate', 'VIX Index', 'US dollar 2-year interest rate', '10-year German Bund price']
        values = [last_SP , last_10y_futures, last_3m_interest, last_10y_interest, last_vix_index, today_rate_2y, bund_value]

        # Create a dictionary by pairing keys and values
        data_dict = dict(zip(keys, values))
        
        # Round the values in the dictionary to two decimal places
        data_dict_rounded = {key: round(value, 2) for key, value in data_dict.items()}
        
        return data_dict_rounded
    
    except Exception as e:
        return {"error": str(e)}
    

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload