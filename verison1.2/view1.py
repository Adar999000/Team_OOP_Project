import pandas as pd
from tabulate import tabulate
import matplotlib
matplotlib.use('Agg')  # שימוש ב-Agg backend
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Patch
import pandas as pd
from tabulate import tabulate
import matplotlib
matplotlib.use('Agg')  # שימוש ב-Agg backend
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Patch
from colorama import Fore, Style  # ייבוא colorama להדפסה בצבעים

class View:
    def __init__(self):
        self.export_dir = "exports"
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def show_menu(self):
        print(Fore.GREEN + "\n====================")
        print(Fore.GREEN + "       Main Menu")
        print(Fore.GREEN + "\n====================")
        print(Fore.GREEN + "1) Set risk level")
        print(Fore.BLUE + "2) Buy security")
        print(Fore.BLUE + "3) Sell security")
        print(Fore.BLUE + "4) Show portfolio")
        print(Fore.BLUE + "5) Consult representative")
        print(Fore.BLUE + "6) Exit")
        print(Fore.GREEN + "====================")
        return input("Choose an option: ")

    def show_buy_menu(self):
        print(Fore.GREEN + "\n====================")
        print(Fore.GREEN + "       Buy Menu")
        print(Fore.GREEN + "====================")
        print(Fore.BLUE + "1) Buy a security")
        print(Fore.BLUE + "2) Talk to a representative")
        print(Fore.BLUE + "3) See the data for this security type")
        print(Fore.BLUE + "4) Back to main menu")
        print(Fore.GREEN + "====================")
        return self.get_input_with_validation("Choose an option: ", ["1", "2", "3", "4"])

    def get_risk_level(self):
        return self.get_input_with_validation("Enter risk level (low, medium, high): ", ["low", "medium", "high"])

    def choose_security_type(self):
        return self.get_input_with_validation("Choose security type (Stock/Bond): ", ["Stock", "Bond"], case_sensitive=False)

    def get_security_name(self):
        return input("Enter security name: ")

    def get_price(self):
        while True:
            try:
                price = float(input(Fore.BLUE + "Enter price: " + Style.RESET_ALL))
                if price <= 0:
                    raise ValueError("Price must be a positive number.")
                return price
            except ValueError as e:
                print(Fore.RED + f"Invalid input: {e}. Please try again." + Style.RESET_ALL)
                price = float(input("Enter price: "))


class View:
    def __init__(self):
        self.export_dir = "exports"
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def show_menu(self):
        print(Fore.GREEN + "\n====================")
        print(Fore.GREEN + "       Main Menu")
        print(Fore.GREEN + "\n====================")
        print(Fore.BLUE + "1) Set risk level")
        print(Fore.BLUE + "2) Buy security")
        print(Fore.BLUE + "3) Sell security")
        print(Fore.BLUE + "4) Show portfolio")
        print(Fore.BLUE + "5) Consult representative")
        print(Fore.BLUE + "6) Exit")
        print(Fore.GREEN + "====================")
        return input("Choose an option: ")

    def show_buy_menu(self):
        print(Fore.GREEN + "\n====================")
        print(Fore.GREEN + "       Buy Menu")
        print(Fore.GREEN + "====================")
        print(Fore.BLUE + "1) Buy a security")
        print(Fore.BLUE + "2) Talk to a representative")
        print(Fore.BLUE + "3) See the data for this security type")
        print(Fore.BLUE + "4) Back to main menu")
        print(Fore.GREEN + "====================")
        return self.get_input_with_validation("Choose an option: ", ["1", "2", "3", "4"])

    def get_risk_level(self):
        return self.get_input_with_validation("Enter risk level (low, medium, high): ", ["low", "medium", "high"])

    def choose_security_type(self):
        return self.get_input_with_validation("Choose security type (Stock/Bond): ", ["Stock", "Bond"], case_sensitive=False)

    def get_security_name(self):
        return input("Enter security name: ")

    def get_price(self):
        while True:
            try:
                price = float(input("Enter price: "))
                if price <= 0:
                    raise ValueError("Price must be a positive number.")
                return price
            except ValueError as e:
                print(Fore.BLUE + f"Invalid input: {e}. Please try again.")

    def get_industry(self):
        return input("Enter industry (e.g., Technology, Healthcare, Finance): ")

    def display_portfolio(self, portfolio):
        if not portfolio:
            print(Fore.BLUE + "The portfolio is empty.")
            return
            
        while True:
            display_choice = self.show_portfolio_menu()
            if display_choice == "1":
                self.print_portfolio(portfolio, "Stocks")
                break
            elif display_choice == "2":
                self.print_portfolio(portfolio, "Bonds")
                break
            elif display_choice == "3":
                self.print_portfolio(portfolio)
                break
            elif display_choice == "4":
                self.save_portfolio_graph(portfolio)
                break
            elif display_choice == "5":
                self.export_to_excel(portfolio)
                break
            elif display_choice == "6":
                self.export_all(portfolio)
                break
            elif display_choice == "7":
                break

    def _create_portfolio_df(self, portfolio):
        try:
            data = []
            for p in portfolio:
                data.append({
                    'ID': p.id,
                    'Stock Name': p.stock_name,
                    'Ticker': p.ticker,
                    'Price': p.price,
                    'Share': p.share,
                    'Type': p.type
                })
            return pd.DataFrame(data)
        except Exception as e:
            print(Fore.BLUE + f"Error creating DataFrame: {str(e)}")
            return None

    def save_portfolio_graph(self, portfolio, portfolio_type=None):
        try:
            if not portfolio:
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty.")
                return

            # סינון לפי סוג התיק אם צוין
            if portfolio_type:
                portfolio = [p for p in portfolio if p.type == portfolio_type]
                if not portfolio:
                    print(Fore.BLUE + f"\nYour {portfolio_type} portfolio is empty.")
                    return

            df = self._create_portfolio_df(portfolio)
            if df is None:
                return

            # יצירת הגרף
            plt.figure(figsize=(12, 6))
            
            # Set colors based on security type
            colors = ['blue' if p.type == 'STOCK' else 'orange' for p in portfolio]
            bars = plt.bar(df['Stock Name'], df['Price'], color=colors)
            
            plt.xticks(rotation=45, ha='right')
            plt.xlabel('Securities')
            plt.ylabel('Price ($)')
            title = "Portfolio Securities Prices"
            if portfolio_type:
                title = f"{portfolio_type} {title}"
            plt.title(title)
            
            # Add legend
            legend_elements = [Patch(facecolor='blue', label='Stocks'),
                             Patch(facecolor='orange', label='Bonds')]
            plt.legend(handles=legend_elements)
            
            # הוספת ערכים מעל העמודות
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'${height:,.0f}',
                        ha='center', va='bottom')
            
            # התאמת הגרף לחלון
            plt.tight_layout()
            
            # יצירת תיקיית הייצוא אם לא קיימת
            if not os.path.exists(self.export_dir):
                os.makedirs(self.export_dir)
            
            # שמירת הגרף
            filename = f"portfolio_graph_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            if portfolio_type:
                filename += f"_{portfolio_type.lower()}"
            filename += ".png"
            save_path = os.path.join(self.export_dir, filename)
            
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(Fore.BLUE + f"\nGraph saved to: {os.path.abspath(save_path)}")
            
            # פתיחת הקובץ
            os.startfile(save_path)
            
        except Exception as e:
            print(Fore.BLUE + f"Error saving graph: {str(e)}")
        finally:
            plt.close()  # וידוא שהגרף נסגר בכל מקרה

    def export_to_excel(self, portfolio, portfolio_type=None):
        try:
            if not portfolio:
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty.")
                return None

            # סינון לפי סוג התיק אם צוין
            if portfolio_type:
                portfolio = [p for p in portfolio if p.type == portfolio_type]
                if not portfolio:
                    print(Fore.BLUE + f"\nYour {portfolio_type} portfolio is empty.")
                    return None

            df = self._create_portfolio_df(portfolio)
            if df is None:
                return None
            
            # יצירת שם קובץ עם נתיב מלא
            filename = f"portfolio_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            if portfolio_type:
                filename += f"_{portfolio_type.lower()}"
            filename += ".xlsx"
            filepath = os.path.join(self.export_dir, filename)
            
            # יצירת Writer של אקסל
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # שמירת הטבלה העיקרית
                excel_df = df.copy()
                excel_df['Price'] = excel_df['Price'].apply(lambda x: f"${x:,.2f}")
                excel_df['Share'] = excel_df['Share'].apply(lambda x: f"{x:.2f}%")
                excel_df.to_excel(writer, sheet_name='Portfolio', index=False)
                
                # יצירת גיליון סיכום
                total_value = df['Price'].sum()
                summary_data = {
                    'Metric': ['Total Value', 'Number of Securities'],
                    'Value': [f"${total_value:,.2f}", len(df)]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                
                # יצירת גיליון התפלגות לפי סוג
                distribution = df['Type'].value_counts().reset_index()
                distribution.columns = ['Type', 'Count']
                distribution.to_excel(writer, sheet_name='Distribution', index=False)
            
            print(Fore.BLUE + f"\nExcel file saved to: {os.path.abspath(filepath)}")
            return filepath
            
        except Exception as e:
            print(Fore.BLUE + f"Error exporting to Excel: {e}")
            return None

    def export_all(self, portfolio, portfolio_type=None):
        # ייצוא לאקסל
        excel_path = self.export_to_excel(portfolio, portfolio_type)
        if excel_path:
            # שמירת גרף
            self.save_portfolio_graph(portfolio, portfolio_type)

    def print_portfolio(self, portfolio, portfolio_type=None):
        try:
            if not portfolio:
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty.")
                return
                
            # סינון לפי סוג התיק אם צוין
            if portfolio_type:
                portfolio = [p for p in portfolio if p.type == portfolio_type]
                if not portfolio:
                    print(Fore.BLUE + f"\nYour {portfolio_type} portfolio is empty.")
                    return

            df = self._create_portfolio_df(portfolio)
            if df is None:
                return
            
            # מיון לפי ID
            df = df.sort_values('ID')
            
            # יצירת עותק לתצוגה עם פורמט מחירים
            display_df = df.copy()
            display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:,.2f}")
            display_df['Share'] = display_df['Share'].apply(lambda x: f"{x:.2f}%")
            
            # הצגת הטבלה בפורמט יפה
            title = "Your"
            if portfolio_type:
                title += f" {portfolio_type}"
            title += " Portfolio:"
            
            print(Fore.BLUE + f"\n{title}")
            print(Fore.BLUE + "=" * 80)
            print(Fore.BLUE + tabulate(display_df, 
                         headers='keys', 
                         tablefmt='fancy_grid', 
                         showindex=False))
            
            # חישוב וצגת סיכום
            total_value = df['Price'].sum()
            num_securities = len(df)
            print(Fore.BLUE + f"\nPortfolio Summary:")
            print(Fore.BLUE + f"Total Value: ${total_value:,.2f}")
            print(Fore.BLUE + f"Number of Securities: {num_securities}")

        except Exception as e:
            print(Fore.BLUE + f"Error displaying portfolio: {str(e)}")
            print(Fore.BLUE + f"Portfolio data: {portfolio}")

    def show_portfolio_menu(self):
        print(Fore.GREEN + "\n====================")
        print(Fore.GREEN + "   Portfolio Menu")
        print(Fore.GREEN + "====================")
        print(Fore.BLUE + "1) View Stocks Portfolio")
        print(Fore.BLUE + "2) View Bonds Portfolio")
        print(Fore.BLUE + "3) View All Portfolio")
        print(Fore.BLUE + "4) Save Portfolio Graph")
        print(Fore.BLUE + "5) Export to Excel")
        print(Fore.BLUE + "6) Export All (Excel + Graph)")
        print(Fore.BLUE + "7) Back to main menu")
        print(Fore.GREEN + "====================")
        return self.get_input_with_validation("Choose an option: ", ["1", "2", "3", "4", "5", "6", "7"])

    def print_menu(self, title, options):
        print(Fore.BLUE + "\n====================")
        print(Fore.BLUE + f"       {title}")
        print(Fore.BLUE + "====================")
        for i, option in enumerate(options, 1):
            print(Fore.BLUE + f"{i}) {option}")
        print(Fore.BLUE + "====================")

    def get_input_with_validation(self, prompt, valid_options, case_sensitive=True):
        while True:
            user_input = input(prompt).strip()
            if not case_sensitive:
                user_input = user_input.capitalize()
            if user_input in valid_options:
                return user_input
            print(Fore.BLUE + f"Invalid input. Please choose from {', '.join(valid_options)}.")

    def get_security_id(self):
        return input("Enter security ID to sell: ")

    def show_message(self, message):
        print(Fore.BLUE + message)

    def show_risk_update_success(self):
        print(Fore.BLUE + "Risk level updated successfully.")

    def show_empty_portfolio(self):
        """הצגת הודעה כשהפורטפוליו ריק"""
        print(Fore.BLUE + "\n=== Portfolio is Empty ===")
        print(Fore.BLUE + "You don't have any securities to sell.")
        print(Fore.BLUE + "Please add some securities first.")
        
    def get_security_id_to_sell(self):
        """קבלת ID של נייר ערך למכירה"""
        while True:
            try:
                print(Fore.BLUE + "\nEnter the ID of the security you want to sell (or press Enter to cancel):")
                user_input = input().strip()
                
                if not user_input:  # המשתמש לחץ Enter
                    print(Fore.BLUE + "Operation cancelled.")
                    return None
                    
                security_id = int(user_input)
                if security_id < 1:
                    print(Fore.BLUE + "ID must be a positive number.")
                    continue
                    
                return security_id
                
            except ValueError:
                print(Fore.BLUE + "Please enter a valid number.")
                
    def show_security_sold_success(self):
        """הצגת הודעת הצלחה במכירת נייר ערך"""
        print(Fore.BLUE + "\n=== Security Sold Successfully ===")
        print(Fore.BLUE + "The security has been removed from your portfolio.")
        
    def show_error_selling_security(self, error_msg):
        """הצגת שגיאה במכירת נייר ערך"""
        print(Fore.BLUE + "\n=== Error Selling Security ===")
        print(Fore.BLUE + f"An error occurred: {error_msg}")
        
    def display_security_data(self, security_type):
        try:
            # קביעת הקובץ המתאים לפי סוג נייר הערך
            filename = "stocks.csv" if security_type.lower() == "stock" else "bonds.csv"
            
            # Get the absolute path to the CSV file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, filename)
            
            # קריאת הקובץ
            df = pd.read_csv(file_path)
            
            # הצגת הנתונים בטבלה מסודרת
            if not df.empty:
                # בחירת העמודות הרלוונטיות והצגתן
                display_df = df[['Name', 'Ticker', 'Price', 'Update Time']]
                display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:,.2f}")
                
                print(Fore.BLUE + "\nAvailable Securities:")
                print(Fore.BLUE + "=" * 80)  # קו מפריד קצר יותר
                
                # הוספת אינדקס המתחיל מ-1
                display_df.index = range(1, len(display_df) + 1)
                print(Fore.BLUE + tabulate(display_df, headers='keys', tablefmt='simple', showindex=True))
                return df
            else:
                print(Fore.BLUE + "No data available.")
                return None
                
        except Exception as e:
            print(Fore.BLUE + f"Error displaying security data: {str(e)}")
            return None

    def get_security_choice(self, max_choice):
        while True:
            try:
                choice = int(input(f"\nChoose a security (1-{max_choice}): "))
                if 1 <= choice <= max_choice:
                    return choice - 1
                print(Fore.BLUE + f"Please enter a number between 1 and {max_choice}")
            except ValueError:
                print(Fore.BLUE + "Please enter a valid number")

    def show_invalid_risk_level(self):
        print(Fore.BLUE + "Invalid risk level. Please enter 'low', 'medium', or 'high'.")

    def show_error_setting_risk_level(self, error):
        print(Fore.BLUE + f"Error setting risk level: {error}")

    def show_security_added_success(self):
        print(Fore.BLUE + "Security added successfully.")

    def show_returning_to_main_menu(self):
        print(Fore.BLUE + "Returning to main menu...")

    def show_invalid_choice(self):
        print(Fore.BLUE + "Invalid choice. Please try again.")

    def show_security_not_found(self):
        print(Fore.BLUE + "Security not found. Please try again.")

    def show_invalid_input(self):
        print(Fore.BLUE + "Invalid input. Security ID must be a number.")

