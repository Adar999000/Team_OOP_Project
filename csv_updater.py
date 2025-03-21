import yfinance as yf  # ספרייה לשליפת נתוני מניות ואגרות חוב בזמן אמת
import pandas as pd  # ספרייה לעבודה עם נתונים בפורמט טבלאי (DataFrame)
from datetime import datetime  # משמש לקבלת התאריך והשעה הנוכחיים
import pytz  # ספרייה לניהול אזורי זמן
import os  # משמש לניהול קבצים ותיקיות במערכת ההפעלה
from colorama import Fore, Style  # ספרייה לצביעת טקסטים במסוף (לא מנוצל בפועל בקובץ)

# הגדרת הנתיב של הספרייה שבה נמצא הקובץ, כך שניתן יהיה לגשת לקובצי הנתונים
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_stocks():
    """ פונקציה לשליפת נתוני מניות מעודכנים ושמירתם ברשימה 
    יוצרת את קובצי ה-CSV """
    
    # רשימה של 50 מניות מובילות לפי הסימול שלהן בבורסה
    stock_symbols = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "V", "JNJ",
        "WMT", "PG", "MA", "UNH", "HD", "BAC", "DIS", "ADBE", "CRM", "NFLX",
        "CSCO", "VZ", "INTC", "PFE", "KO", "PEP", "TMO", "ABT", "MRK", "ORCL",
        "AVGO", "ACN", "NKE", "DHR", "T", "WFC", "TXN", "QCOM", "UPS", "NEE",
        "PM", "MS", "RTX", "BMY", "AMGN", "LIN", "COST", "MDT", "HON", "IBM"
    ]
    
    try:
        # יצירת הנתיב המלא של קובץ ה-CSV שבו יישמרו הנתונים
        stocks_file = os.path.join(CURRENT_DIR, 'stocks.csv')

        # בדיקה אם הקובץ כבר קיים במערכת
        if os.path.exists(stocks_file):
            existing_df = pd.read_csv(stocks_file)  # טעינת הנתונים הקיימים מקובץ ה-CSV לתוך DataFrame
            existing_prices = dict(zip(existing_df['Ticker'], existing_df['Price']))  # יצירת מילון של מחירים ישנים
            existing_times = dict(zip(existing_df['Ticker'], existing_df['Update Time']))  # יצירת מילון של זמני עדכון קודמים
        else: 
            existing_prices = {}  # אם הקובץ לא קיים, ניצור מילון ריק עבור מחירי המניות
            existing_times = {}  # יצירת מילון ריק לזמני עדכון

        data = []  # רשימה ריקה לאחסון נתוני המניות החדשים
        current_time = datetime.now(pytz.timezone('Israel')).strftime('%Y-%m-%d %H:%M:%S')  # קביעת התאריך והשעה הנוכחיים לפי שעון ישראל

        for symbol in stock_symbols:  # לולאה העוברת על כל סימול מניה ברשימה
            try:
                stock = yf.Ticker(symbol)  # יצירת אובייקט מניה עבור הסימול הנוכחי
                info = stock.info  # שליפת המידע על המניה
                current_price = info.get('regularMarketPrice', 0)  # קבלת המחיר הנוכחי של המניה (אם לא נמצא, חוזר 0)

                # בדיקת שינוי במחיר לעומת המחיר הקודם שנשמר
                if symbol in existing_prices:
                    old_price = float(str(existing_prices[symbol]).replace('$', '').replace(',', ''))  # המרת מחיר ישן למספר
                    if abs(old_price - current_price) > 0.01:  # אם יש שינוי במחיר, מעדכן את זמן השינוי
                        update_time = current_time
                    else:
                        update_time = existing_times.get(symbol, current_time)  # אם אין שינוי, משאיר את זמן העדכון הקודם
                else:
                    update_time = current_time  # אם זו מניה חדשה, קובע את זמן העדכון להווה

                # הוספת הנתונים לרשימה
                data.append({
                    'Name': info.get('longName', symbol),  # שם החברה
                    'Ticker': symbol,  # סימול המניה
                    'Price': f"${current_price:.2f}",  # המחיר בפורמט דולר
                    'Industry': info.get('industry', 'N/A'),  # תחום פעילות החברה (אם קיים)
                    'Update Time': update_time  # זמן העדכון האחרון
                })
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")  # הדפסת שגיאה במקרה של כשל בשליפת הנתונים
                continue

        return pd.DataFrame(data)  # החזרת הנתונים כ-DataFrame
    except Exception as e:
        print(f"Error in fetch_stocks: {str(e)}")  # טיפול בשגיאות כלליות
        return pd.DataFrame()

def fetch_bonds():
    """ פונקציה לשליפת נתוני אגרות חוב ושמירתם בקובץ CSV """

    # רשימה של 50 אגרות חוב מובילות לפי הסימול שלהן
    bond_symbols = [
        "AGG", "BND", "TLT", "IEF", "SHY", "LQD", "HYG", "JNK", "MUB", "TIP",
        "EMB", "BWX", "VCIT", "VCLT", "VCSH", "VGIT", "VGLT", "VGSH", "VMBS", "VTIP",
        "GOVT", "IAGG", "IEI", "PLW", "SCHO", "SCHR", "SCHZ", "SPTL", "SPTI", "SPTS",
        "USIG", "USTB", "VWOB", "WIP", "BNDX", "FBND", "FLTB", "FLRN", "GBIL", "GSY",
        "HYLB", "IGIB", "IGLB", "IGSB", "IUSB", "MINT", "NEAR", "PFFD", "SHYG", "SJNK"
    ]
    
    try:
        bonds_file = os.path.join(CURRENT_DIR, 'bonds.csv')  # יצירת הנתיב המלא של קובץ אגרות החוב

        # בדיקה אם הקובץ קיים
        if os.path.exists(bonds_file):
            existing_df = pd.read_csv(bonds_file)  # טעינת נתוני הקובץ
            existing_prices = dict(zip(existing_df['Ticker'], existing_df['Price']))  # מילון עם מחירים ישנים
            existing_times = dict(zip(existing_df['Ticker'], existing_df['Update Time']))  # מילון של זמני עדכון קודמים
        else:
            existing_prices = {}  # אם אין קובץ, יוצרים מילון ריק
            existing_times = {}

        data = []  # רשימה לאחסון הנתונים החדשים
        current_time = datetime.now(pytz.timezone('Israel')).strftime('%Y-%m-%d %H:%M:%S')  # הגדרת הזמן הנוכחי

        for symbol in bond_symbols:  # מעבר על כל אגרת חוב ברשימה
            try:
                bond = yf.Ticker(symbol)  # יצירת אובייקט עבור האגרת חוב
                info = bond.info  # שליפת המידע הקיים
                current_price = info.get('regularMarketPrice', 0)  # קבלת המחיר הנוכחי

                # בדיקת שינוי במחיר
                if symbol in existing_prices:
                    old_price = float(str(existing_prices[symbol]).replace('$', '').replace(',', ''))  # המרת המחיר למספר
                    if abs(old_price - current_price) > 0.01:  # אם יש שינוי משמעותי
                        update_time = current_time
                    else:
                        update_time = existing_times.get(symbol, current_time)
                else:
                    update_time = current_time

                # הוספת הנתונים לרשימה
                data.append({
                    'Name': info.get('longName', symbol),
                    'Ticker': symbol,
                    'Price': f"${current_price:.2f}",
                    'Industry': info.get('bondType', 'N/A'),
                    'Update Time': update_time
                })
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")  # טיפול בשגיאות והדפסתן
                continue

        return pd.DataFrame(data)  # החזרת הנתונים כ-DataFrame
    except Exception as e:
        print(f"Error in fetch_bonds: {str(e)}")  # טיפול בשגיאות כלליות
        return pd.DataFrame()
