import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
import os
from colorama import Fore, Style

# Define the directory path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_stocks():
    # List of 50 major company stock symbols
    stock_symbols = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "V", "JNJ",
        "WMT", "PG", "MA", "UNH", "HD", "BAC", "DIS", "ADBE", "CRM", "NFLX",
        "CSCO", "VZ", "INTC", "PFE", "KO", "PEP", "TMO", "ABT", "MRK", "ORCL",
        "AVGO", "ACN", "NKE", "DHR", "T", "WFC", "TXN", "QCOM", "UPS", "NEE",
        "PM", "MS", "RTX", "BMY", "AMGN", "LIN", "COST", "MDT", "HON", "IBM"
    ]
    
    try:
        # Read existing CSV if it exists
        stocks_file = os.path.join(CURRENT_DIR, 'stocks.csv')
        if os.path.exists(stocks_file):
            existing_df = pd.read_csv(stocks_file)
            existing_prices = dict(zip(existing_df['Ticker'], existing_df['Price']))
            existing_times = dict(zip(existing_df['Ticker'], existing_df['Update Time']))
        else:
            existing_prices = {}
            existing_times = {}

        data = []
        current_time = datetime.now(pytz.timezone('Israel')).strftime('%Y-%m-%d %H:%M:%S')

        for symbol in stock_symbols:
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                current_price = info.get('regularMarketPrice', 0)
                
                # Check if price has changed
                if symbol in existing_prices:
                    old_price = float(str(existing_prices[symbol]).replace('$', '').replace(',', ''))
                    if abs(old_price - current_price) > 0.01:  # Changed condition to update time when price changes
                        update_time = current_time
                    else:
                        update_time = existing_times.get(symbol, current_time)
                else:
                    update_time = current_time

                data.append({
                    'Name': info.get('longName', symbol),
                    'Ticker': symbol,
                    'Price': f"${current_price:.2f}",
                    'Industry': info.get('industry', 'N/A'),
                    'Update Time': update_time
                })
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")
                continue

        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error in fetch_stocks: {str(e)}")
        return pd.DataFrame()

def fetch_bonds():
    # List of 50 bond symbols (using ETFs and bond funds as proxies)
    bond_symbols = [
        "AGG", "BND", "TLT", "IEF", "SHY", "LQD", "HYG", "JNK", "MUB", "TIP",
        "EMB", "BWX", "VCIT", "VCLT", "VCSH", "VGIT", "VGLT", "VGSH", "VMBS", "VTIP",
        "GOVT", "IAGG", "IEI", "PLW", "SCHO", "SCHR", "SCHZ", "SPTL", "SPTI", "SPTS",
        "USIG", "USTB", "VWOB", "WIP", "BNDX", "FBND", "FLTB", "FLRN", "GBIL", "GSY",
        "HYLB", "IGIB", "IGLB", "IGSB", "IUSB", "MINT", "NEAR", "PFFD", "SHYG", "SJNK"
    ]
    
    try:
        # Read existing CSV if it exists
        bonds_file = os.path.join(CURRENT_DIR, 'bonds.csv')
        if os.path.exists(bonds_file):
            existing_df = pd.read_csv(bonds_file)
            existing_prices = dict(zip(existing_df['Ticker'], existing_df['Price']))
            existing_times = dict(zip(existing_df['Ticker'], existing_df['Update Time']))
        else:
            existing_prices = {}
            existing_times = {}

        data = []
        current_time = datetime.now(pytz.timezone('Israel')).strftime('%Y-%m-%d %H:%M:%S')

        for symbol in bond_symbols:
            try:
                bond = yf.Ticker(symbol)
                info = bond.info
                current_price = info.get('regularMarketPrice', 0)
                
                # Check if price has changed
                if symbol in existing_prices:
                    old_price = float(str(existing_prices[symbol]).replace('$', '').replace(',', ''))
                    if abs(old_price - current_price) > 0.01:  # Changed condition to update time when price changes
                        update_time = current_time
                    else:
                        update_time = existing_times.get(symbol, current_time)
                else:
                    update_time = current_time

                data.append({
                    'Name': info.get('longName', symbol),
                    'Ticker': symbol,
                    'Price': f"${current_price:.2f}",
                    'Industry': info.get('bondType', 'N/A'),  # Changed Type to Industry to match stocks
                    'Update Time': update_time
                })
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")
                continue

        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error in fetch_bonds: {str(e)}")
        return pd.DataFrame()

# Fetch and save data
try:
    security_type = "stock"
    # Fetch data
    if security_type.lower() == "stock":
        stocks = fetch_stocks()
        if not stocks.empty:
            stocks_file = os.path.join(CURRENT_DIR, 'stocks.csv')
            stocks.to_csv(stocks_file, index=False)
            
    else:
        bonds = fetch_bonds()
        if not bonds.empty:
            bonds_file = os.path.join(CURRENT_DIR, 'bonds.csv')
            bonds.to_csv(bonds_file, index=False)
            

except Exception as e:
    print(f"Error updating market data: {str(e)}")