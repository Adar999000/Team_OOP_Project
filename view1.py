import pandas as pd
from tabulate import tabulate
import matplotlib
matplotlib.use('Agg')  # שימוש ב-Agg backend
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Patch
from colorama import Fore, Style  # ייבוא colorama להדפסה בצבעים
import random

class View:
    def __init__(self):
        self.export_dir = r"C:\Users\adar0\Desktop\oop_project_final\exports"
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def show_menu(self):
        print(Fore.GREEN + "\n====================" + Style.RESET_ALL)
        print(Fore.GREEN + "       Main Menu" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)
        print(Fore.BLUE + "1) 📊 Risk level" + Style.RESET_ALL)
        print(Fore.BLUE + "2) 💰 Buy security" + Style.RESET_ALL)
        print(Fore.BLUE + "3) 💸 Sell security" + Style.RESET_ALL)
        print(Fore.BLUE + "4) 📂 Show portfolio" + Style.RESET_ALL)
        print(Fore.BLUE + "5) 🤖 Consult AI representative" + Style.RESET_ALL)
        print(Fore.BLUE + "6) 🚪 Exit" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)
        return input(Fore.BLUE + "Choose an option: " + Style.RESET_ALL)

    def show_buy_menu(self):
        print(Fore.GREEN + "\n====================" + Style.RESET_ALL)
        print(Fore.GREEN + "       Buy Menu" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)
        print(Fore.BLUE + "1) 💹 Buy a security" + Style.RESET_ALL)
        print(Fore.BLUE + "2) 🤖 Talk to an AI representative" + Style.RESET_ALL)
        print(Fore.BLUE + "3) 🔙 Back to main menu" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)
        return self.get_input_with_validation(Fore.BLUE + "Choose an option: " + Style.RESET_ALL, ["1", "2", "3"])

    def get_risk_level(self):
        while True:
            user_input = input(Fore.BLUE + "Enter risk level (low, medium, high): " + Style.RESET_ALL).strip().lower()
            if user_input in ["low", "medium", "high"]:
                return user_input
            print(Fore.YELLOW + "Invalid input. Please choose from low, medium, high." + Style.RESET_ALL)

    def choose_security_type(self):
        user_input = input(Fore.BLUE + "Choose security type (Stock/Bond): " + Style.RESET_ALL).strip().lower()
        while user_input not in ["stock", "bond"]:
            print(Fore.YELLOW + "Invalid input. Please enter 'Stock' or 'Bond'." + Style.RESET_ALL)
            user_input = input(Fore.BLUE + "Choose security type (Stock/Bond): " + Style.RESET_ALL).strip().lower()
        return user_input

    def get_security_name(self):
        return input(Fore.BLUE + "Enter security name: " + Style.RESET_ALL)

    def get_price(self):
        while True:
            try:
                price = float(input(Fore.BLUE + "Enter price: " + Style.RESET_ALL))
                if price <= 0:
                    raise ValueError("Price must be a positive number.")
                return price
            except ValueError as e:
                print(Fore.YELLOW + f"Invalid input: {e}. Please try again." + Style.RESET_ALL)

    def get_industry(self):
        return input(Fore.BLUE + "Enter industry (e.g., Technology, Healthcare, Finance): " + Style.RESET_ALL)

    def display_portfolio(self, portfolio):
        if not portfolio:
            print(Fore.BLUE + "\nThe portfolio is empty." + Style.RESET_ALL)
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
            print(Fore.RED + f"Error creating DataFrame: {str(e)}" + Style.RESET_ALL)
            return None

    def save_portfolio_graph(self, portfolio, portfolio_type=None):
        try:
            if not portfolio:
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty." + Style.RESET_ALL)
                return

            # Group by security name and sum quantities
            df = pd.DataFrame([{
                'Name': p.stock_name,
                'Type': p.type,
                'Price': p.price,
                'Quantity': p.share
            } for p in portfolio])
            
            if portfolio_type:
                df = df[df['Type'] == portfolio_type]
                if df.empty:
                    print(Fore.BLUE + f"\nYour {portfolio_type} portfolio is empty." + Style.RESET_ALL)
                    return

            # Group by security name and calculate total value
            df['Total Value'] = df['Price'] * df['Quantity']
            grouped_df = df.groupby('Name').agg({
                'Total Value': 'sum',
                'Type': 'first'
            }).reset_index()
            
            # Calculate total portfolio value for percentage
            total_portfolio_value = grouped_df['Total Value'].sum()
            grouped_df['Share'] = (grouped_df['Total Value'] / total_portfolio_value * 100)

            plt.figure(figsize=(12, 6))
            colors = ['blue' if t == 'STOCK' else 'orange' for t in grouped_df['Type']]
            bars = plt.bar(grouped_df['Name'], grouped_df['Share'], color=colors)
            
            plt.xticks(rotation=45, ha='right')
            plt.xlabel('Securities')
            plt.ylabel('Portfolio Share (%)')
            title = "Portfolio Distribution"
            if portfolio_type:
                title = f"{portfolio_type} {title}"
            plt.title(title)
            
            legend_elements = [Patch(facecolor='blue', label='Stocks'),
                             Patch(facecolor='orange', label='Bonds')]
            plt.legend(handles=legend_elements)
            
            # Add percentage and dollar value labels
            for bar in bars:
                height = bar.get_height()
                value = height / 100 * total_portfolio_value
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%\n${value:,.2f}',
                        ha='center', va='bottom')
            
            plt.tight_layout()
            
            filename = f"portfolio_graph_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            if portfolio_type:
                filename += f"_{portfolio_type.lower()}"
            filename += ".png"
            save_path = os.path.join(self.export_dir, filename)
            
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(Fore.GREEN + f"\nGraph saved to: {os.path.abspath(save_path)}" + Style.RESET_ALL)
            os.startfile(save_path)
            
        except Exception as e:
            print(Fore.RED + f"Error saving graph: {str(e)}" + Style.RESET_ALL)
        finally:
            plt.close()

    def export_to_excel(self, portfolio, portfolio_type=None):
        try:
            if not portfolio:
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty." + Style.RESET_ALL)
                return None

            # Group by security name and sum quantities
            df = pd.DataFrame([{
                'Name': p.stock_name,
                'Type': p.type,
                'Price': p.price,
                'Quantity': p.share
            } for p in portfolio])
            
            if portfolio_type:
                df = df[df['Type'] == portfolio_type]
                if df.empty:
                    print(Fore.BLUE + f"\nYour {portfolio_type} portfolio is empty." + Style.RESET_ALL)
                    return None

            # Group by security name and calculate total value
            df['Total Value'] = df['Price'] * df['Quantity']
            grouped_df = df.groupby('Name').agg({
                'Total Value': 'sum',
                'Type': 'first'
            }).reset_index()
            
            # Calculate total portfolio value for percentage
            total_portfolio_value = grouped_df['Total Value'].sum()
            grouped_df['Share'] = (grouped_df['Total Value'] / total_portfolio_value * 100)
            
            # Sort by Share percentage in descending order
            grouped_df = grouped_df.sort_values('Share', ascending=False)

            # Create Excel file
            filename = f"portfolio_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            if portfolio_type:
                filename += f"_{portfolio_type.lower()}"
            filename += ".xlsx"
            filepath = os.path.join(self.export_dir, filename)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                grouped_df.to_excel(writer, sheet_name='Portfolio', index=False)
                
                # Create summary sheet
                total_value = grouped_df['Total Value'].sum()
                num_securities = len(grouped_df)
                summary_data = {
                    'Metric': ['Total Value', 'Number of Securities'],
                    'Value': [f"${total_value:,.2f}", num_securities]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                
                # Create distribution sheet
                distribution = grouped_df['Type'].value_counts().reset_index()
                distribution.columns = ['Type', 'Count']
                distribution.to_excel(writer, sheet_name='Distribution', index=False)
            
            print(Fore.GREEN + f"\nExcel file saved to: {os.path.abspath(filepath)}" + Style.RESET_ALL)
            return filepath
            
        except Exception as e:
            print(Fore.RED + f"Error exporting to Excel: {e}" + Style.RESET_ALL)
            return None

    def export_all(self, portfolio, portfolio_type=None):
        # Export to Excel
        excel_path = self.export_to_excel(portfolio, portfolio_type)
        if excel_path:
            # Save graph
            self.save_portfolio_graph(portfolio, portfolio_type)

    def print_portfolio(self, portfolio, portfolio_type=None):
        try:
            if not portfolio:
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty." + Style.RESET_ALL)
                return

            # Create DataFrame
            data = []
            for p in portfolio:
                if portfolio_type and p.type != portfolio_type:
                    continue
                data.append({
                    'Name': p.stock_name,
                    'Type': p.type,
                    'Price': p.price,
                    'Quantity': p.share,
                    'Total Value': p.price * p.share
                })
            
            if not data:
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty." + Style.RESET_ALL)
                return

            # Create DataFrame and calculate shares
            df = pd.DataFrame(data)
            total_portfolio_value = df['Total Value'].sum()
            df['Share'] = (df['Total Value'] / total_portfolio_value * 100)
            
            # Sort by Share percentage in descending order
            df = df.sort_values('Share', ascending=False)

            # Format display values
            display_df = df.copy()
            display_df['Price'] = display_df['Price'].map('${:.2f}'.format)
            display_df['Total Value'] = display_df['Total Value'].map('${:.2f}'.format)
            display_df['Share'] = display_df['Share'].map('{:.2f}%'.format)

            # Display portfolio
            print(f"\n{Fore.GREEN}Your Portfolio:{Style.RESET_ALL}")
            print(Fore.BLUE + "=" * 80 + Style.RESET_ALL)
            print(Fore.BLUE + tabulate(display_df, headers='keys', tablefmt='fancy_grid', showindex=False) + Style.RESET_ALL)
            
            # Display summary
            print(f"\n{Fore.GREEN}Portfolio Summary:{Style.RESET_ALL}")
            print(Fore.BLUE + f"Total Portfolio Value: ${total_portfolio_value:.2f}" + Style.RESET_ALL)
            
        except Exception as e:
            print(Fore.RED + f"Error displaying portfolio: {str(e)}" + Style.RESET_ALL)

    def show_portfolio_menu(self):
        print(Fore.GREEN + "\n====================" + Style.RESET_ALL)
        print(Fore.GREEN + "   Portfolio Menu" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)
        print(Fore.BLUE + "1) 📈 View Stocks Portfolio" + Style.RESET_ALL)
        print(Fore.BLUE + "2) 📉 View Bonds Portfolio" + Style.RESET_ALL)
        print(Fore.BLUE + "3) 📊 View All Portfolio" + Style.RESET_ALL)
        print(Fore.BLUE + "4) 🖼️  Save Portfolio Graph" + Style.RESET_ALL)
        print(Fore.BLUE + "5) 📄 Export to Excel" + Style.RESET_ALL)
        print(Fore.BLUE + "6) 📁 Export All (Excel + Graph)" + Style.RESET_ALL)
        print(Fore.BLUE + "7) 🔙 Back to main menu" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)
        return self.get_input_with_validation(Fore.BLUE + "Choose an option: " + Style.RESET_ALL, ["1", "2", "3", "4", "5", "6", "7"])

    def print_menu(self, title, options):
        print(Fore.GREEN + "\n====================" + Style.RESET_ALL)
        print(Fore.GREEN + f"       {title}" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)
        for i, option in enumerate(options, 1):
            print(Fore.BLUE + f"{i}) {option}" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)

    def get_input_with_validation(self, prompt, valid_options, case_sensitive=True):
        while True:
            user_input = input(prompt).strip()
            if not case_sensitive:
                user_input = user_input.lower()
                valid_options = [opt.lower() for opt in valid_options]
            if user_input in valid_options:
                return user_input
            print(Fore.YELLOW + f"Invalid input. Please choose from {', '.join(valid_options)}." + Style.RESET_ALL)

    def get_security_id(self):
        return input(Fore.BLUE + "Enter security ID to sell: " + Style.RESET_ALL)

    def show_message(self, message):
        print(Fore.BLUE + message + Style.RESET_ALL)

    def show_risk_update_success(self):
        print(Fore.GREEN + "\n✅ Risk level updated successfully." + Style.RESET_ALL)

    def show_empty_portfolio(self):
        print(Fore.BLUE + "\n=== Portfolio is Empty ===" + Style.RESET_ALL)
        print(Fore.BLUE + "You don't have any securities to sell." + Style.RESET_ALL)
        print(Fore.BLUE + "Please add some securities first." + Style.RESET_ALL)
        
    def get_security_id_to_sell(self):
        while True:
            try:
                print(Fore.BLUE + "\nEnter the ID of the security you want to sell (or press Enter to cancel):" + Style.RESET_ALL)
                user_input = input().strip()
                
                if not user_input:  # המשתמש לחץ Enter
                    print(Fore.YELLOW + "Operation cancelled." + Style.RESET_ALL)
                    return None
                    
                security_id = int(user_input)
                if security_id < 1:
                    print(Fore.YELLOW + "ID must be a positive number." + Style.RESET_ALL)
                    continue
                    
                return security_id
                
            except ValueError:
                print(Fore.YELLOW + "Please enter a valid number." + Style.RESET_ALL)
                
    def show_security_sold_success(self):
        print(Fore.GREEN + "\n=== Security Sold Successfully ===" + Style.RESET_ALL)
        print(Fore.GREEN + "✅ The security has been removed from your portfolio." + Style.RESET_ALL)

    def show_error_selling_security(self, error_msg):
        print(Fore.RED + "\n=== Error Selling Security ===" + Style.RESET_ALL)
        print(Fore.RED + f"An error occurred: {error_msg}" + Style.RESET_ALL)

    def display_security_data(self, security_type):
        try:
            filename = "stocks.csv" if security_type.lower() == "stock" else "bonds.csv"
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, filename)
            
            df = pd.read_csv(file_path)
            
            # Clean up the Price column and sort by price descending
            df['Price'] = df['Price'].astype(str).str.replace('$', '').astype(float)
            df = df.sort_values('Price', ascending=False)
            df['Price'] = df['Price'].apply(lambda x: f"${x:.2f}")
            
            if not df.empty:
                display_df = df[['Name', 'Ticker', 'Price', 'Update Time']]
                
                print(Fore.BLUE + "\nAvailable Securities:" + Style.RESET_ALL)
                print(Fore.BLUE + "=" * 80 + Style.RESET_ALL)
                
                display_df.index = range(1, len(display_df) + 1)
                print(Fore.BLUE + tabulate(display_df, headers='keys', tablefmt='simple', showindex=True) + Style.RESET_ALL)
                return df
            else:
                print(Fore.YELLOW + f"\nNo {security_type}s data available." + Style.RESET_ALL)
                return None
                
        except FileNotFoundError:
            print(Fore.RED + f"\nNo {security_type}s data file found." + Style.RESET_ALL)
            return None
        except Exception as e:
            print(Fore.RED + f"Error displaying security data: {str(e)}" + Style.RESET_ALL)
            return None

    def update_prices(self, security_type):
        """Update security prices with random variations"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            if security_type.upper() == "STOCK":
                file_path = os.path.join(current_dir, "stocks.csv")
                security_name = "stocks"
            else:
                file_path = os.path.join(current_dir, "bonds.csv")
                security_name = "bonds"
                
            if not os.path.exists(file_path):
                print(Fore.RED + f"Error: {security_name}.csv file not found" + Style.RESET_ALL)
                return
                
            df = pd.read_csv(file_path)
            if df.empty:
                print(Fore.YELLOW + f"Warning: No {security_name} data found" + Style.RESET_ALL)
                return
                
            df = df.head(50)
            
            df['Price'] = df['Price'].astype(str).str.replace('$', '').astype(float)
            df['Price'] = df['Price'].apply(lambda x: round(random.uniform(x * 0.9, x * 1.1), 2))
            
            df = df.sort_values('Price', ascending=False)
            
            df['Update Time'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            
            df['Price'] = df['Price'].apply(lambda x: f"${x:.2f}")
            
            df.to_csv(file_path, index=False)
            print(Fore.GREEN + f"\n✅ Successfully updated {len(df)} {security_name}" + Style.RESET_ALL)
            
        except Exception as e:
            print(Fore.RED + f"Error updating {security_type} prices: {str(e)}" + Style.RESET_ALL)

    def get_security_choice(self, max_choice):
        while True:
            try:
                choice = int(input(Fore.BLUE + f"\nChoose a security (1-{max_choice}): " + Style.RESET_ALL))
                if 1 <= choice <= max_choice:
                    return choice - 1
                print(Fore.YELLOW + f"Please enter a number between 1 and {max_choice}" + Style.RESET_ALL)
            except ValueError:
                print(Fore.YELLOW + "Please enter a valid number" + Style.RESET_ALL)

    def show_invalid_risk_level(self):
        print(Fore.YELLOW + "Invalid risk level. Please enter 'low', 'medium', or 'high'." + Style.RESET_ALL)

    def show_error_setting_risk_level(self, error):
        print(Fore.RED + f"Error setting risk level: {error}" + Style.RESET_ALL)

    def show_security_added_success(self):
        print(Fore.GREEN + "\n✅ Security added successfully." + Style.RESET_ALL)

    def show_returning_to_main_menu(self):
        print(Fore.BLUE + "Returning to main menu..." + Style.RESET_ALL)

    def show_invalid_choice(self):
        print(Fore.YELLOW + "Invalid choice. Please try again." + Style.RESET_ALL)

    def show_security_not_found(self):
        print(Fore.YELLOW + "Security not found. Please try again." + Style.RESET_ALL)

    def show_invalid_input(self):
        print(Fore.YELLOW + "Invalid input. Security ID must be a number." + Style.RESET_ALL)

    def show_risk_level_menu(self):
        print(Fore.GREEN + "\n====================" + Style.RESET_ALL)
        print(Fore.GREEN + "    Risk Level Menu" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)
        print(Fore.BLUE + "1) 📊 Show portfolio risk level" + Style.RESET_ALL)
        print(Fore.BLUE + "2) ⚙️  Set risk level" + Style.RESET_ALL)
        print(Fore.BLUE + "3) 🔙 Back to main menu" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)
        return self.get_input_with_validation(Fore.BLUE + "Choose an option: " + Style.RESET_ALL, ["1", "2", "3"])

    def show_current_risk_level(self, risk_level):
        if risk_level:
            print(Fore.BLUE + f"\nCurrent portfolio risk level: {risk_level}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Risk level has not been set yet." + Style.RESET_ALL)
