from view1 import View
from model1 import Model
from chatbot import handle_conversation
import pandas as pd
from tabulate import tabulate

class Controller:
    def __init__(self):
        self.view = View()
        self.model = Model()
        self.portfolio = []  # רשימה ריקה במקום None

    def start(self):
        while True:
            choice = self.view.show_menu()
            if choice == "1":
                self.set_risk_level()
            elif choice == "2":
                security_type = self.view.choose_security_type()
                self.choose_action(security_type)
            elif choice == "3":
                self.sell_security()
            elif choice == "4":
                self.show_portfolio()
            elif choice == "5":
                self.consult_representative()
            elif choice == "6":
                print("Exiting the system.\n")
                break
            else:
                print("Invalid option, please try again.\n")

    def set_risk_level(self):
        try:
            new_risk_level = self.view.get_risk_level()
            if new_risk_level.lower() not in ["low", "medium", "high"]:
                self.view.show_invalid_risk_level()
                return
            self.model.update_risk_level(new_risk_level)
            self.view.show_risk_update_success()
        except Exception as e:
            self.view.show_error_setting_risk_level(e)

    def choose_action(self, security_type):
        while True:
            choice = self.view.show_buy_menu()

            if choice == "1":
                # הצגת הרשימה וקבלת בחירת המשתמש
                df = self.view.display_security_data(security_type)
                if df is not None and not df.empty:
                    idx = self.view.get_security_choice(len(df))
                    if idx is not None:
                        selected_security = df.iloc[idx]
                        
                        # המרת המחיר למספר
                        try:
                            price_str = selected_security['Price']
                            # הסרת סימן הדולר ופסיקים אם קיימים
                            price_str = str(price_str).replace('$', '').replace(',', '')
                            price = float(price_str)
                            
                            # חישוב אחוז מהתיק
                            portfolio_by_type = self.model.get_securities_by_type(security_type)
                            total_value = sum(s.price for s in portfolio_by_type)
                            share_percentage = (price / (total_value + price)) * 100 if total_value > 0 else 100
                            
                            # הוספת נייר הערך שנבחר
                            self.model.add_security(
                                stock_name=selected_security['Name'],
                                ticker=selected_security['Ticker'],
                                price=price,
                                share=share_percentage,
                                security_type=security_type.upper()
                            )
                            self.view.show_security_added_success()
                        except ValueError as e:
                            self.view.show_error(f"Invalid price format: {price_str}")
                        except Exception as e:
                            self.view.show_error(f"Error adding security: {str(e)}")
                break
            elif choice == "2":
                self.consult_representative()
                break
            elif choice == "3":
                self.view.display_security_data(security_type)
                break
            elif choice == "4":
                self.view.show_returning_to_main_menu()
                break
            else:
                self.view.show_invalid_choice()

    def sell_security(self):
        try:
            # קבלת הפורטפוליו העדכני
            self.portfolio = self.model.get_all_securities()
            
            # בדיקה אם הפורטפוליו ריק
            if not self.portfolio:
                self.view.show_empty_portfolio()
                return
                
            # הצגת הפורטפוליו הנוכחי
            self.view.print_portfolio(self.portfolio)
            
            # קבלת ID למכירה
            security_id = self.view.get_security_id_to_sell()
            if security_id is None:  # המשתמש ביטל
                return
                
            # מכירת נייר הערך
            if self.model.delete_security(security_id):
                self.view.show_security_sold_success()
                # עדכון הפורטפוליו המקומי
                self.portfolio = self.model.get_all_securities()
            else:
                self.view.show_error_selling_security(f"Security with ID {security_id} not found")
                
        except Exception as e:
            self.view.show_error_selling_security(str(e))

    def show_portfolio(self):
        choice = self.view.show_portfolio_menu()
        portfolio = None
        portfolio_type = None

        if choice in ["1", "2", "3"]:
            if choice == "1":
                portfolio_type = "STOCK"
                portfolio = self.model.get_securities_by_type(portfolio_type)
            elif choice == "2":
                portfolio_type = "BOND"
                portfolio = self.model.get_securities_by_type(portfolio_type)
            elif choice == "3":
                portfolio = self.model.get_all_securities()
            
            self.view.print_portfolio(portfolio, portfolio_type)
        
        elif choice == "4":
            if choice == "1":
                portfolio_type = "STOCK"
                portfolio = self.model.get_securities_by_type(portfolio_type)
            elif choice == "2":
                portfolio_type = "BOND"
                portfolio = self.model.get_securities_by_type(portfolio_type)
            else:
                portfolio = self.model.get_all_securities()
            self.view.save_portfolio_graph(portfolio, portfolio_type)
        
        elif choice == "5":
            if choice == "1":
                portfolio_type = "STOCK"
                portfolio = self.model.get_securities_by_type(portfolio_type)
            elif choice == "2":
                portfolio_type = "BOND"
                portfolio = self.model.get_securities_by_type(portfolio_type)
            else:
                portfolio = self.model.get_all_securities()
            self.view.export_to_excel(portfolio, portfolio_type)
        
        elif choice == "6":
            if choice == "1":
                portfolio_type = "STOCK"
                portfolio = self.model.get_securities_by_type(portfolio_type)
            elif choice == "2":
                portfolio_type = "BOND"
                portfolio = self.model.get_securities_by_type(portfolio_type)
            else:
                portfolio = self.model.get_all_securities()
            self.view.export_all(portfolio, portfolio_type)

    def consult_representative(self):
        handle_conversation()

    def check_portfolio(self):
        if not self.portfolio:
            self.view.show_empty_portfolio()
