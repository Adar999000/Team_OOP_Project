import os
import sqlite3
import pandas as pd
from portfolio import Portfolio

class Model:
    def __init__(self):
        self.risk_level = None
        self.securities = []
        self.next_id = 1
        self.db_file = "portfolio.db"
        self._init_db()
        self._load_settings()
        self.load_portfolio()

    def _init_db(self):
        """יצירת טבלאות במסד הנתונים אם הן לא קיימות"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # יצירת טבלת פורטפוליו אם לא קיימת
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY,
                stock_name TEXT NOT NULL,
                ticker TEXT NOT NULL,
                price REAL NOT NULL,
                share REAL NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        
        # יצירת טבלת הגדרות אם לא קיימת
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()

    def update_risk_level(self, risk_level):
        """עדכון רמת הסיכון בזיכרון ובמסד הנתונים"""
        risk_level = risk_level.lower()
        self.risk_level = risk_level
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value)
                VALUES ('risk_level', ?)
            ''', (risk_level,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def add_security(self, stock_name, ticker, price, share, security_type):
        """הוספת נייר ערך לפורטפוליו"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            # הוספת הנייר ערך למסד הנתונים
            cursor.execute('''
                INSERT INTO portfolio (stock_name, ticker, price, share, type)
                VALUES (?, ?, ?, ?, ?)
            ''', (stock_name, ticker, float(price), float(share), security_type.upper()))
            
            # קבלת ה-ID שנוצר
            security_id = cursor.lastrowid
            
            # יצירת אובייקט Portfolio
            security = Portfolio(
                id=security_id,
                stock_name=stock_name,
                ticker=ticker,
                price=float(price),
                share=float(share),
                type=security_type
            )
            
            self.securities.append(security)
            conn.commit()
            return security
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_all_securities(self):
        """קבלת כל ניירות הערך מהפורטפוליו"""
        self.load_portfolio()  # רענון הרשימה ממסד הנתונים
        return self.securities

    def get_securities_by_type(self, security_type):
        """קבלת ניירות ערך מסוג מסוים"""
        self.load_portfolio()  # רענון הרשימה ממסד הנתונים
        return [s for s in self.securities if s.type.upper() == security_type.upper()]

    def remove_security(self, security_id):
        """הסרת נייר ערך מהפורטפוליו"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM portfolio WHERE id = ?', (security_id,))
            conn.commit()
            self.securities = [s for s in self.securities if s.id != security_id]
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_security_by_id(self, security_id):
        """קבלת נייר ערך לפי ID"""
        for security in self.securities:
            if security.id == security_id:
                return security
        return None

    def load_portfolio(self):
        """טעינת הפורטפוליו ממסד הנתונים"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM portfolio')
            rows = cursor.fetchall()
            
            self.securities = []
            for row in rows:
                security = Portfolio(
                    id=row[0],
                    stock_name=row[1],
                    ticker=row[2],
                    price=float(row[3]),
                    share=float(row[4]),
                    type=row[5]
                )
                self.securities.append(security)
                
            # עדכון ה-next_id
            if self.securities:
                self.next_id = max(s.id for s in self.securities) + 1
            else:
                self.next_id = 1
                
        except Exception as e:
            print(f"Error loading portfolio: {e}")
            self.securities = []
            self.next_id = 1
        finally:
            conn.close()

    def update_security_shares(self):
        """עדכון אחוזי ההחזקה בתיק"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            # חישוב הסכום הכולל לכל סוג נייר ערך
            cursor.execute('''
                SELECT type, SUM(price) as total
                FROM portfolio
                GROUP BY type
            ''')
            totals = dict(cursor.fetchall())
            
            # עדכון האחוזים לכל נייר ערך
            for security in self.securities:
                total = totals.get(security.type, 0)
                if total > 0:
                    share = (security.price / total) * 100
                    cursor.execute('''
                        UPDATE portfolio
                        SET share = ?
                        WHERE id = ?
                    ''', (share, security.id))
                    security.share = share
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _load_settings(self):
        """טעינת הגדרות ממסד הנתונים"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT value FROM settings WHERE key = ?', ('risk_level',))
            result = cursor.fetchone()
            if result:
                self.risk_level = result[0]
        finally:
            conn.close()