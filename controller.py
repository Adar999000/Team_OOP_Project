from view1 import View
from model1 import Model
from chatbot import handle_conversation
import pandas as pd
from tabulate import tabulate
import sqlite3

class Controller:
    def __init__(self):
        self.view = View()
        self.model = Model()
        self.portfolio = []  # רשימה ריקה במקום None

    def start(self):
        while True:
            choice = self.view.show_menu()
            if choice == "1":
                self.handle_risk_level_menu()
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
                self.view.show_invalid_option()

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

    def handle_risk_level_menu(self):
        while True:
            choice = self.view.show_risk_level_menu()
            if choice == "1":
                self.view.show_current_risk_level(self.model.risk_level)
            elif choice == "2":
                self.set_risk_level()
            elif choice == "3":
                break

    def choose_action(self, security_type):
        """בחירת פעולה לביצוע"""
        try:
            if security_type.upper() == "STOCK":
                # טיפול במניות
                from csv_updater import fetch_stocks
                stocks_df = fetch_stocks()
                if not stocks_df.empty:
                    self.view.update_prices(security_type)
                    stocks_df = self.view.display_security_data(security_type)
                    while True:
                        try:
                            choice = input("\nEnter the number of the stock you want to buy (1-50), or 0 to cancel: ")
                            if choice == "0":
                                return
                            choice = int(choice)
                            if 1 <= choice <= 50:
                                break
                            print("Please enter a number between 1 and 50.")
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    # Get quantity
                    while True:
                        try:
                            quantity = float(input("Enter the quantity you want to buy: "))
                            if quantity > 0:
                                break
                            print("Please enter a positive number.")
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    # Get the selected stock from the displayed DataFrame
                    selected_stock = stocks_df.iloc[choice - 1]
                    
                    # Check if adding this security would exceed risk level
                    if not self.model.can_add_security({
                        'type': "STOCK",
                        'share': quantity,
                        'industry': 'Technology'
                    }):
                        print("\nWarning: Cannot add this security - it would exceed your defined risk level.")
                        return
                    
                    # Add to portfolio
                    self.model.add_security(
                        stock_name=selected_stock['Name'],
                        ticker=selected_stock['Ticker'],
                        price=float(selected_stock['Price'].replace('$', '')),
                        share=quantity,
                        security_type="STOCK"
                    )
                    print(f"\nSuccessfully bought {quantity} stocks of {selected_stock['Name']}")
            
            else:
                # טיפול באגרות חוב
                from csv_updater import fetch_bonds
                bonds_df = fetch_bonds()
                if not bonds_df.empty:
                    self.view.update_prices(security_type)
                    bonds_df = self.view.display_security_data(security_type)
                    while True:
                        try:
                            choice = input("\nEnter the number of the bond you want to buy (1-50), or 0 to cancel: ")
                            if choice == "0":
                                return
                            choice = int(choice)
                            if 1 <= choice <= 50:
                                break
                            print("Please enter a number between 1 and 50.")
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    # Get quantity
                    while True:
                        try:
                            quantity = float(input("Enter the quantity you want to buy: "))
                            if quantity > 0:
                                break
                            print("Please enter a positive number.")
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    # Get the selected bond from the displayed DataFrame
                    selected_bond = bonds_df.iloc[choice - 1]
                    
                    # Check if adding this security would exceed risk level
                    if not self.model.can_add_security({
                        'type': "BOND",
                        'share': quantity,
                        'industry': 'Finance'
                    }):
                        print("\nWarning: Cannot add this security - it would exceed your defined risk level.")
                        return
                    
                    # Add to portfolio
                    self.model.add_security(
                        stock_name=selected_bond['Name'],
                        ticker=selected_bond['Ticker'],
                        price=float(selected_bond['Price'].replace('$', '')),
                        share=quantity,
                        security_type="BOND"
                    )
                    print(f"\nSuccessfully bought {quantity} bonds of {selected_bond['Name']}")
        
        except Exception as e:
            print(f"Error: {str(e)}")

    def sell_security(self):
        try:
            while True:
                # Get current portfolio
                self.portfolio = self.model.get_all_securities()
                
                if not self.portfolio:
                    self.view.show_empty_portfolio()
                    return
                
                # Show current portfolio
                self.view.print_portfolio(self.portfolio)
                
                # Group securities by name and sum quantities
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
                
                # Get security to sell
                print("\nAvailable securities to sell:")
                for idx, row in grouped_df.iterrows():
                    print(f"{idx + 1}. {row['Name']} - Quantity: {row['Quantity']}")
                
                try:
                    choice = input("\nChoose security to sell (or 0 to cancel): ")
                    if choice == "0":
                        return
                        
                    choice = int(choice)
                    if 1 <= choice <= len(grouped_df):
                        selected_security = grouped_df.iloc[choice - 1]
                        
                        # Get quantity to sell
                        while True:
                            try:
                                sell_quantity = float(input(f"Enter quantity to sell (max {selected_security['Quantity']}): "))
                                if sell_quantity <= 0:
                                    print("Quantity must be positive.")
                                elif sell_quantity > selected_security['Quantity']:
                                    print(f"Cannot sell more than available quantity ({selected_security['Quantity']}).")
                                else:
                                    # Find securities to sell
                                    security_ids = securities_df[securities_df['Name'] == selected_security['Name']]['ID'].tolist()
                                    remaining_to_sell = sell_quantity
                                    
                                    for sec_id in security_ids:
                                        sec = next((p for p in self.portfolio if p.id == sec_id), None)
                                        if sec and remaining_to_sell > 0:
                                            if sec.share <= remaining_to_sell:
                                                # Sell entire position
                                                self.model.remove_security(sec_id)
                                                remaining_to_sell -= sec.share
                                            else:
                                                # Partially sell position
                                                new_share = sec.share - remaining_to_sell
                                                # עדכון הכמות בדאטהבייס
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
                                    
                                    # רענון הפורטפוליו
                                    self.portfolio = self.model.get_all_securities()
                                    self.view.show_security_sold_success()
                                    
                                    # הצג את הפורטפוליו המעודכן
                                    if self.portfolio:
                                        self.view.print_portfolio(self.portfolio)
                                    else:
                                        print("\nYour portfolio is now empty.")
                                    
                                    break
                            except ValueError:
                                print("Please enter a valid number.")
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Please enter a valid number.")
                    
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
