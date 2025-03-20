####        על חלק זה ארז ארנון עבד        ####



#1  ייבוא מחלקת התצוגה
from view1 import View

#2  ייבוא מחלקת המודל
from model1 import Model


#3 ייבוא ספריית הצ'אטבוט לייעוץ
from chatbot import handle_conversation

#4 ספריות לעבודה עם טבלאות נתונים
import pandas as pd
from tabulate import tabulate

#5 ספריה לעבודה עם בסיס הנתונים
import sqlite3


class Controller:
    def __init__(self):  # 1
        """אתחול המחלקה - יצירת אובייקטים של תצוגה ומודל"""

        self.view = View()    ## יצירת אובייקט מסוג תצוגה
        self.model = Model()  ## יצירת אובייקט מסוג מודל
        self.portfolio = []   ## רשימה ריקה


    def start(self): # 2 (פונקציה מרכזית)
        """הפונקציה הראשית שמפעילה את התוכנית, ומנהלת את התפריט הראשי"""

        while True: ## REPL סגנון
            choice = self.view.show_menu() ## view הצגת התפריט הראשי מ

            if choice == "1":
                self.handle_risk_level_menu() ## רמת סיכון - הפוקנציה בהמשך

            elif choice == "2":
                security_type = self.view.choose_security_type()  ## View תפריט מ
                self.choose_action(security_type) ## תהליך הקנייה - הפונקציה בהמשך
            elif choice == "3":
                self.sell_security() ## תהליך המכירה - הפונקציה בהמשך

            elif choice == "4":
                self.show_portfolio()  ## ניהול התצוגה של תיק ההקשעות  - 2 הפונקציות בהמשך 

            elif choice == "5":
                self.consult_representative()  ##  ייעוץ עם עוזר חכם - הפונקציה בהמשך

            elif choice == "6":
                print("Exiting the system.\n")  ## יציאה מהמערכת
                break ## עצירה של הלולאה

            else:
                self.view.show_invalid_option() ## שגיאה - אופציה לא תקינה


    def set_risk_level(self): # 3
        """ מנהלת את תהליך עדכון רמת הסיכון (אופציה 2,1)"""

        try:
            new_risk_level = self.view.get_risk_level()   ## view  תצוגה לבחירת רמת סיכון ב
            

            self.model.update_risk_level(new_risk_level)
            ## שמירה בזיכרון

            self.view.show_risk_update_success()
            ## הודעה שהעדכון בוצע בהצלחה

            self.model._load_settings()
            self.view.show_current_risk_level(self.model.risk_level)
        except Exception as e:
            self.view.show_error_setting_risk_level(e) ## הצגת הודעת שגיאה בנוגע לעדכון רמת הסיכון


    def handle_risk_level_menu(self): # 4
        """ מנהלת את תהליך רמת הסיכון (אופציה 1)"""

        while True: ## REPL גם כן מבוסס

            choice = self.view.show_risk_level_menu()  ## view התפריט מ

            if choice == "1":
                self.model._load_settings()  ## טוען את רמת הסיכון מהדאטאבייס
                self.view.show_current_risk_level(self.model.risk_level)  ## מציג את רמת הסיכון הנוכחית

            elif choice == "2":
                self.set_risk_level() ##  פוקנציה מספר 3 בקובץ זה , עדכון רמת הסיכון

            elif choice == "3":
                break ## יציאה מהתפריט המשני


######################################################################################################################################### 2


    def choose_action(self, security_type): # 5
        """  מנהלת את תהליך קניית נייר הערך (מנייה או אגרת חוב) , אופציה 2"""

        try:
            if security_type.upper() == "STOCK":  ## במצב של מניות

                from csv_updater import fetch_stocks ## מעודכן csv ייבוא
                stocks_df = fetch_stocks()
                if not stocks_df.empty:
                    self.view.update_prices(security_type) ## מציג מחירים מעודכנים
                    stocks_df = self.view.display_security_data(security_type)  ## מראה רשימה של 50 מניות ממויינות בסדר יורד לפי המחיר
                    while True:
                        try:
                            choice = input("\nEnter the number of the stock you want to buy (1-50), or 0 to cancel: ") ## בחירה לפי מספר זהות

                            if choice == "0": 
                                return ## בחירה לביטול
                            
                            choice = int(choice)  
                            if 1 <= choice <= 50: ## בחירת סוג לפי מספר מזהה בין 1 ל50
                                break
                            print("Please enter a number between 1 and 50.")
                        except ValueError:
                            print("Please enter a valid number.") ## מספר לא תקין
                    
                    # Get quantity
                    while True:
                        try:
                            quantity = int(input("Enter the quantity you want to buy: ")) ## בחירת כמות מניות לפי הסוג שנבחר
                            if quantity > 0:
                                break
                            print("Please enter a positive number.") ## שגיאה - מספר שלילי
                        except ValueError:
                            print("Please enter a valid number.")  ## שגיאה - מספר לא תקין
                    
                    
                    selected_stock = stocks_df.iloc[choice - 1]
                   
                    if not self.model.can_add_security({  ## בדיקה שאין חריגה מרמת הסיכון המוגדרת 
                        'type': "STOCK",
                        'share': quantity,
                        'industry': 'Technology'
                    }):
                        print("\nWarning: Cannot add this security - it would exceed your defined risk level.")  ## הודעת אזהרה
                        return
                    
                    
                    self.model.add_security(                ## הוספה לתיק ההשקעות
                        stock_name=selected_stock['Name'],
                        ticker=selected_stock['Ticker'],
                        price=float(selected_stock['Price'].replace('$', '')),
                        share=quantity,
                        security_type="STOCK"
                    )
                    print(f"\nSuccessfully bought {quantity} stocks of {selected_stock['Name']}")
            


            else: ## במצב של אגרות חוב 
                from csv_updater import fetch_bonds  ##  מעודכן csv ייבוא
                bonds_df = fetch_bonds()
                if not bonds_df.empty:
                    self.view.update_prices(security_type) ## מציג מחירים מעודכנים
                    bonds_df = self.view.display_security_data(security_type)  ## מראה רשימה של 50 אגרות חוב ממויינות בסדר יורד לפי המחיר
                    while True:
                        try:
                            choice = input("\nEnter the number of the bond you want to buy (1-50), or 0 to cancel: ") ## בחירה לפי מספר זהות

                            if choice == "0": 
                                return ## בחירה לביטול
                            
                            choice = int(choice)
                            if 1 <= choice <= 50: ## בחירת סוג לפי מספר מזהה בין 1 ל-50
                                break
                            print("Please enter a number between 1 and 50.")
                        except ValueError:
                            print("Please enter a valid number.") ## מספר לא תקין
                    
                    # Get quantity
                    while True:
                        try:
                            quantity = int(input("Enter the quantity you want to buy: "))  ## בחירת כמות אגרות החוב לפי הסוג שנבחר
                            if quantity > 0:
                                break
                            print("Please enter a positive number.") ## שגיאה - מספר שלילי
                        except ValueError:
                            print("Please enter a valid number.") ## שגיאה - מספר לא תקין
                    
                    
                    selected_bond = bonds_df.iloc[choice - 1]

                    if not self.model.can_add_security({   ##  בדיקה שאין חריגה מרמת הסיכון המוגדרת
                        'type': "BOND",
                        'share': quantity,
                        'industry': 'Finance'
                    }):
                        print("\nWarning: Cannot add this security - it would exceed your defined risk level.") ## הודעת אזהרה
                        return
                    

                    self.model.add_security(       ## הוספה לתיק ההשקעות 
                        stock_name=selected_bond['Name'],
                        ticker=selected_bond['Ticker'],
                        price=float(selected_bond['Price'].replace('$', '')),
                        share=quantity,
                        security_type="BOND"
                    )
                    print(f"\nSuccessfully bought {quantity} bonds of {selected_bond['Name']}")
        
        except Exception as e:
            print(f"Error: {str(e)}")

######################################################################################################################################  3

    def sell_security(self): # 6
        """ מנהלת את תהליך מכירת נייר הערך (אופציה 3)"""

        try:
            while True: ## REPL מבוסס
                self.portfolio = self.model.get_all_securities()   ##1 טוען את התיק הנוכחי
                
                if not self.portfolio:  ## אם אין נתונים
                    self.view.show_empty_portfolio()   ## מציג הודעה למשתמש (כי התיק ריק)
                    return
                
                
                self.view.print_portfolio(self.portfolio)   ## מציג את התיק הנוכחי
                securities_df = pd.DataFrame([{
                    'Name': p.stock_name,
                    'Type': p.type,
                    'Price': p.price,
                    'Quantity': p.share,
                    'ID': p.id
                } for p in self.portfolio])
                
                grouped_df = securities_df.groupby('Name').agg({
                    'Quantity': 'sum',
                    'Type': 'first',
                    'Price': 'first'
                }).reset_index()
                
            
                print("\nAvailable securities to sell:")  ## תצוגה של ניירות הערך שניתן למכור (לפי סוג וכמות)
                for idx, row in grouped_df.iterrows():
                    print(f"{idx + 1}. {row['Name']} - Quantity: {row['Quantity']}")
                


                try:
                    choice = input("\nChoose security to sell (or 0 to cancel): ") ## בחירת סוג נייר ערך למכירה לפי מספר זהות

                    if choice == "0":
                        return  ## בחירה לביטול
                        
                    choice = int(choice)
                    if 1 <= choice <= len(grouped_df):    ## בחירה לפי מספר זהות (מ1 עד למספר כמות הסוגים שנקנתה)
                        selected_security = grouped_df.iloc[choice - 1]
                        
                        
                        while True:
                            try:
                                sell_quantity = int(input(f"Enter quantity to sell (max {selected_security['Quantity']}): ")) ## בחירת כמות למכירה

                                if sell_quantity <= 0:
                                    print("Quantity must be positive.") ## כאשר מספר שלילי
                                elif sell_quantity > selected_security['Quantity']:
                                    print(f"Cannot sell more than available quantity ({selected_security['Quantity']}).")  ## כאשר חורג מהמספר המקסימלי
                                


                                else:  ## כאשר תקין
                                    security_ids = securities_df[securities_df['Name'] == selected_security['Name']]['ID'].tolist() 
                                    remaining_to_sell = sell_quantity
                                    
                                    for sec_id in security_ids:
                                        sec = next((p for p in self.portfolio if p.id == sec_id), None)
                                        if sec and remaining_to_sell > 0:
                                            if sec.share <= remaining_to_sell:

                                                ## מכירת כל הכמות
                                                self.model.remove_security(sec_id)
                                                remaining_to_sell -= sec.share ## החסרה

                                            else:
                                                ## מכירת חלק מהכמות
                                                new_share = sec.share - remaining_to_sell ## החסרה (בדרך שונה)

                                                
                                                ## עדכון הכמות בדאטה בייס
                                                conn = sqlite3.connect(self.model.db_file)
                                                cursor = conn.cursor()
                                                cursor.execute('''
                                                    UPDATE portfolio
                                                    SET share = ?
                                                    WHERE id = ?
                                                ''', (new_share, sec_id))
                                                conn.commit()
                                                conn.close()
                                                sec.share = new_share
                                                remaining_to_sell = 0
                                    
                                    self.portfolio = self.model.get_all_securities() ##2 רענון הפורטפוליו
                                    self.view.show_security_sold_success() ## תצוגה שהמכירה בוצעה בהצלחה
                                    
                                    ##  הצגת הפורטפוליו (המעודכן) 
                                    if self.portfolio:
                                        self.view.print_portfolio(self.portfolio)
                                    else:
                                        print("\nYour portfolio is now empty.")  ## במידה והפורטפוליו (המעודכן) ריק
                                    
                                    break
                            except ValueError:
                                print("Please enter a valid number.") ## שגיאת קלט
                    else:
                        print("Invalid choice.") ## שגיאת קלט
                except ValueError:
                    print("Please enter a valid number.")


        except Exception as e:
            self.view.show_error_selling_security(str(e))  ## תצוגה של שגיאה במקרה של מכירה 


####################################################################################################################################  4

    def show_portfolio(self): # 7
        """  מנהלת את תהליך תצוגת הפורטפוליו (אופציה 4)"""
        try:
            choice = self.view.show_portfolio_menu() ## view הצגת תפריט אופציות תצוגה מ
            
            if choice == "7":  
                return  ## בחירה לביטול
                
            portfolio = None
            portfolio_type = None
            
            
            if choice in ["1", "2"]:   ## שליפה מהזיכרון (מהמודל) לפי סוג נייר הערך
                portfolio_type = "STOCK" if choice == "1" else "BOND"
                portfolio = self.model.get_securities_by_type(portfolio_type)
            else: ## כאשר הבחירה היא 3
                portfolio = self.model.get_all_securities()
            
            ## view חלק זה מבוצע בעיקרו על ידי פונקציות מ
            if choice in ["1", "2", "3"]:
                self.view.print_portfolio(portfolio, portfolio_type) ##  הצגת פורטפוליו: מניות / אגרות חוב / מניות וגם אגרות חוב

            elif choice == "4":
                self.view.save_portfolio_graph(portfolio, portfolio_type) ## תצוגה גרפית של תיק ההשקעות

            elif choice == "5":
                self.view.export_to_excel(portfolio, portfolio_type) ## ייצוא לאקסל של תיק ההשקעות 

            elif choice == "6":
                self.view.export_all(portfolio, portfolio_type) ## תצוגה גרפית של תיק ההשקעות + ייצוא לאקסל של תיק ההשקעות
                
        except Exception as e:
            print(f"Error displaying portfolio: {str(e)}")  ## שגיאה



    def consult_representative(self): # 8
        """ שיחה עם צ'אטבוט לייעוץ (אופציה 5)"""

        handle_conversation()



    def check_portfolio(self): # 9
        # פונקציה כללית הבודקת האם תיק ההשקעות ריק #

        if not self.portfolio:
            self.view.show_empty_portfolio() ## הודעה במידה והתיק ריק
