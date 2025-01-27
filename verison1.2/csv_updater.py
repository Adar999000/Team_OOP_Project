import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

def fetch_stocks():
    """Fetch real stock data for 50 major companies"""
    stock_tickers = [
        # Technology
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'AVGO', 'ORCL', 'CSCO',
        # Financial
        'JPM', 'BAC', 'WFC', 'GS', 'MS', 'BLK', 'C', 'SPGI', 'AXP', 'V',
        # Healthcare
        'JNJ', 'UNH', 'PFE', 'MRK', 'ABBV', 'LLY', 'TMO', 'ABT', 'DHR', 'BMY',
        # Consumer
        'PG', 'KO', 'PEP', 'WMT', 'HD', 'MCD', 'NKE', 'DIS', 'COST', 'SBUX',
        # Industrial
        'XOM', 'CVX', 'LIN', 'RTX', 'HON', 'CAT', 'UPS', 'BA', 'GE', 'MMM'
    ]
    
    try:
        # Download data for all stocks at once
        data = yf.download(stock_tickers, period='1d', group_by='ticker')
        
        # Process each stock's data
        stocks_list = []
        update_time = datetime.now(pytz.timezone('Asia/Jerusalem')).strftime('%Y-%m-%d %H:%M:%S')
        for ticker in stock_tickers:
            if ticker in data.columns.levels[0]:
                stock_data = data[ticker]
                if not stock_data.empty:
                    # Get company info
                    try:
                        company = yf.Ticker(ticker)
                        name = company.info.get('longName', ticker)
                        industry = company.info.get('industry', 'Technology' if ticker in stock_tickers[:10] else
                                                'Financial' if ticker in stock_tickers[10:20] else
                                                'Healthcare' if ticker in stock_tickers[20:30] else
                                                'Consumer' if ticker in stock_tickers[30:40] else
                                                'Industrial')
                    except:
                        name = ticker
                        industry = 'Unknown'
                    
                    # Create stock entry
                    stocks_list.append({
                        'Name': name[:40] if name else ticker,  
                        'Ticker': ticker,
                        'Price': round(stock_data['Close'].iloc[-1], 2),  
                        'Update Time': update_time
                    })
        
        return pd.DataFrame(stocks_list) if stocks_list else pd.DataFrame()
    except Exception as e:
        print(f"Error fetching stocks: {str(e)}")
        return pd.DataFrame()

def fetch_bonds():
    """Fetch real bond data including government and corporate bonds"""
    bond_tickers = [
        # US Treasury Bond ETFs
        'TLT', 'IEF', 'SHY', 'GOVT', 'VGIT', 'VGLT', 'SCHO', 'SCHR', 'VGSH',
        # Corporate Bond ETFs
        'LQD', 'HYG', 'JNK', 'VCIT', 'VCSH', 'VCLT', 'AGG', 'BND',
        # International Bond ETFs
        'BWX', 'EMB', 'IGOV', 'IAGG',
        # Inflation Protected
        'TIP', 'VTIP', 'STIP', 'SCHP',
        # Municipal Bond ETFs
        'MUB', 'TFI', 'CMF', 'NYF',
        # Mortgage Bond ETFs
        'MBB', 'VMBS', 'GNMA',
        # Convertible Bond ETFs
        'CWB', 'ICVT',
        # High Yield Corporate
        'USHY', 'SHYG', 'FALN',
        # Investment Grade Corporate
        'IGIB', 'IGLB', 'USIG',
        # Short Term Corporate
        'IGSB', 'SLQD', 'SPSB',
        # Broad Market
        'SPAB', 'FBND', 'BNDS',
        # Bank Loan
        'BKLN', 'SRLN', 'FTSL'
    ]
    
    # Define bond categories
    bond_categories = {
        'TLT': 'US Treasury', 'IEF': 'US Treasury', 'SHY': 'US Treasury', 
        'GOVT': 'US Treasury', 'VGIT': 'US Treasury', 'VGLT': 'US Treasury', 
        'SCHO': 'US Treasury', 'SCHR': 'US Treasury', 'VGSH': 'US Treasury',
        'LQD': 'Corporate', 'HYG': 'Corporate', 'JNK': 'Corporate', 
        'VCIT': 'Corporate', 'VCSH': 'Corporate', 'VCLT': 'Corporate', 
        'AGG': 'Corporate', 'BND': 'Corporate',
        'BWX': 'International', 'EMB': 'International', 'IGOV': 'International', 
        'IAGG': 'International',
        'TIP': 'Inflation Protected', 'VTIP': 'Inflation Protected', 
        'STIP': 'Inflation Protected', 'SCHP': 'Inflation Protected',
        'MUB': 'Municipal', 'TFI': 'Municipal', 'CMF': 'Municipal', 'NYF': 'Municipal',
        'MBB': 'Mortgage', 'VMBS': 'Mortgage', 'GNMA': 'Mortgage',
        'CWB': 'Convertible', 'ICVT': 'Convertible',
        'USHY': 'High Yield Corporate', 'SHYG': 'High Yield Corporate', 
        'FALN': 'High Yield Corporate',
        'IGIB': 'Investment Grade', 'IGLB': 'Investment Grade', 'USIG': 'Investment Grade',
        'IGSB': 'Short Term', 'SLQD': 'Short Term', 'SPSB': 'Short Term',
        'SPAB': 'Broad Market', 'FBND': 'Broad Market', 'BNDS': 'Broad Market',
        'BKLN': 'Bank Loan', 'SRLN': 'Bank Loan', 'FTSL': 'Bank Loan'
    }
    
    try:
        bonds_data = {}
        update_time = datetime.now(pytz.timezone('Asia/Jerusalem')).strftime('%Y-%m-%d %H:%M:%S')
        for ticker in bond_tickers:
            try:
                bond = yf.Ticker(ticker)
                hist = bond.history(period='1d')
                if not hist.empty:
                    bonds_data[ticker] = {
                        'Name': bond.info.get('longName', ticker)[:40],  
                        'Ticker': ticker,
                        'Price': round(hist['Close'].iloc[-1], 2),  
                        'Update Time': update_time
                    }
            except:
                continue
                
        bonds_df = pd.DataFrame(bonds_data.values())
        return bonds_df if not bonds_df.empty else pd.DataFrame()
    except Exception as e:
        print(f"Error fetching bonds: {str(e)}")
        return pd.DataFrame()

# Fetch and save data
try:
    # Fetch data
    stocks = fetch_stocks()
    bonds = fetch_bonds()
    
    if not stocks.empty:
        stocks.to_csv('stocks.csv', index=False)
        print(f"Successfully updated {len(stocks)} stocks")
    
    if not bonds.empty:
        bonds.to_csv('bonds.csv', index=False)
        print(f"Successfully updated {len(bonds)} bonds")

except Exception as e:
    print(f"Error updating market data: {str(e)}")