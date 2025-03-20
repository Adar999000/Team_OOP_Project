####        על חלק זה ארז ארנון עבד        ####

#1 ספריות לעבודה עם טבלאות נתונים
import pandas as pd

#2 ספריה להצגה של טבלאות ונתונים
from tabulate import tabulate



#3 ספריות ליצירת גרפים והצגתם
import matplotlib
matplotlib.use('Agg')  # שימוש ב-Agg backend
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


#4 ספריה לעבודה עם תיקיות וקבצים
import os

#5 ספריה להדפסה צבעונית בטרמינל
from colorama import Fore, Style

#6 ספריה ליצירת מספרים אקראיים
import random

class View:   
    def __init__(self): # 1
        """אתחול תיקיית הייצוא: לגרפים וקבצי אקסל"""

        self.export_dir = r"C:\Users\User\OneDrive\Desktop\oop_project_final\export"     ## תיקיית הייצוא
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def show_menu(self): # 2
        """מציגה את התפריט הראשי"""

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
        return self.get_input_with_validation(Fore.BLUE + "Choose an option: " + Style.RESET_ALL, ["1", "2", "3", "4", "5", "6"])

    def get_risk_level(self): # 3
        """ משמשת בעדכון רמת הסיכון - מבקשת מהמשתמש להזין רמת סיכון (נמוך/בינוני/גבוה) ומוודאת שהקלט תקין"""

        print(Fore.GREEN + "\n=== Set Risk Level ===" + Style.RESET_ALL)
        print(Fore.BLUE + "Available risk levels:" + Style.RESET_ALL)

        print(Fore.GREEN + "1. LOW" + Style.RESET_ALL)
        print(Fore.YELLOW + "2. MEDIUM" + Style.RESET_ALL)
        print(Fore.RED + "3. HIGH" + Style.RESET_ALL)

        print(Fore.GREEN + "===================" + Style.RESET_ALL)
        
        choice = self.get_input_with_validation(Fore.BLUE + "Choose risk level (1/2/3): " + Style.RESET_ALL, ["1", "2", "3"])
        risk_levels = {"1": "low", "2": "medium", "3": "high"}
        return risk_levels[choice]


    def choose_security_type(self): # 4
        """  לפני תהליך הקנייה - מבקשת מהמשתמש לבחור מנייה או אגרת חוב ומוודאת שהקלט תקין"""

        user_input = input(Fore.BLUE + "Choose security type (Stock/Bond): " + Style.RESET_ALL).strip().lower() ## פונקציית הקטנה לתווים
        while user_input not in ["stock", "bond"]: 
            print(Fore.YELLOW + "Invalid input. Please enter 'Stock' or 'Bond'." + Style.RESET_ALL) ## מצב לא תקין - invalid

            user_input = input(Fore.BLUE + "Choose security type (Stock/Bond): " + Style.RESET_ALL).strip().lower() 
        return user_input ## מצב תקין


######################################################################################################################################   2

    def show_empty_portfolio_message(self): # 5
        """מציגה הודעה כאשר תיק ההשקעות ריק"""

        print(Fore.BLUE + "\nThe portfolio is empty." + Style.RESET_ALL)


    def _create_portfolio_df(self, portfolio): # 6
        """ יצירת טבלת דאטה פריים של תיק ההשקעות"""

        try:
            data = []
            for p in portfolio:
                data.append({
                    'ID': p.id, ## מספר זהות
                    'Stock Name': p.stock_name,  ## שם המניה
                    'Ticker': p.ticker, 
                    'Price': p.price, ## מחיר
                    'Share': p.share, ## אחוז מהתיק 
                    'Type': p.type    ## סוג
                })
            return pd.DataFrame(data)
        except Exception as e:
            print(Fore.RED + f"Error creating DataFrame: {str(e)}" + Style.RESET_ALL)
            return None


    def save_portfolio_graph(self, portfolio, portfolio_type=None): # 7
        """ תצוגה גרפית של תיק המניות (אופציה 4,4)"""

        try:
            if not portfolio:
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty." + Style.RESET_ALL) ## כאשר ריק
                return

            ## נעזרים בנתונים הבאים
            df = pd.DataFrame([{
                'Name': p.stock_name,
                'Type': p.type,
                'Price': p.price,
                'Quantity': p.share
            } for p in portfolio])
            
            if portfolio_type:
                df = df[df['Type'] == portfolio_type]
                if df.empty:
                    print(Fore.BLUE + f"\nYour {portfolio_type} portfolio is empty." + Style.RESET_ALL) ## כאשר ריק
                    return

            ## חישוב ותצוגה של הערך הכולל של סוג המניה
            df['Total Value'] = df['Price'] * df['Quantity']
            grouped_df = df.groupby('Name').agg({
                'Total Value': 'sum',
                'Type': 'first'
            }).reset_index()
            
            ## חישוב ותצוגה באחוזים של סוג המנייה
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
            
            ##  הוספת תוויות של דולרים ושל אחוזים לשם התצוגה 
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
            print(Fore.RED + f"Error saving graph: {str(e)}" + Style.RESET_ALL) ## כאשר יש שגיאה
        finally:
            plt.close()



    def export_to_excel(self, portfolio, portfolio_type=None): # 8
        """מייצאת את תיק ההשקעות לקובץ אקסל 
        (אופציה 5,4) ושומרת בתיקיית הייצוא"""

        try:
            if not portfolio:
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty." + Style.RESET_ALL) ## כאשר ריק
                return None

            ## נעזרים בנתונים הבאים (כמו בפונקציה 7 - יצירת גרף)
            df = pd.DataFrame([{
                'Name': p.stock_name,
                'Type': p.type,
                'Price': p.price,
                'Quantity': p.share
            } for p in portfolio])
            
            if portfolio_type:
                df = df[df['Type'] == portfolio_type]
                if df.empty:
                    print(Fore.BLUE + f"\nYour {portfolio_type} portfolio is empty." + Style.RESET_ALL) ## כאשר ריק
                    return None

            ## חישוב ותצוגה של הערך הכולל של סוג המניה (כמו בפוקנציה 7)
            df['Total Value'] = df['Price'] * df['Quantity']
            grouped_df = df.groupby('Name').agg({
                'Total Value': 'sum',
                'Type': 'first'
            }).reset_index()
            
            ## חישוב ותצוגה באחוזים של סוג המנייה (כמו בפונקציה 7)
            total_portfolio_value = grouped_df['Total Value'].sum()
            grouped_df['Share'] = (grouped_df['Total Value'] / total_portfolio_value * 100)
            grouped_df = grouped_df.sort_values('Share', ascending=False)



            ## יצירת קובץ אקסל, ושמירתו בתיקיית הייצוא
            filename = f"portfolio_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            if portfolio_type:
                filename += f"_{portfolio_type.lower()}"
            filename += ".xlsx"
            filepath = os.path.join(self.export_dir, filename)
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                grouped_df.to_excel(writer, sheet_name='Portfolio', index=False)
                total_value = grouped_df['Total Value'].sum()
                num_securities = len(grouped_df)
                summary_data = {
                    'Metric': ['Total Value', 'Number of Securities'],
                    'Value': [f"${total_value:,.2f}", num_securities]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                distribution = grouped_df['Type'].value_counts().reset_index()
                distribution.columns = ['Type', 'Count']
                distribution.to_excel(writer, sheet_name='Distribution', index=False)
            
            print(Fore.GREEN + f"\nExcel file saved to: {os.path.abspath(filepath)}" + Style.RESET_ALL) ## הודעת הצלחה שקובץ האקסל נוצר + כתובתו במחשב
            return filepath
            
        except Exception as e:
            print(Fore.RED + f"Error exporting to Excel: {e}" + Style.RESET_ALL) ## כאשר יש שגיאה ביצירת קובץ אקסל
            return None



    def export_all(self, portfolio, portfolio_type=None): # 9
        """ מייצאת את תיק ההשקעות לקובץ אקסל + גרף (אופציה 6,4)"""

        ## ייצוא לאקסל
        excel_path = self.export_to_excel(portfolio, portfolio_type) ## שימוש בפונקציה מספר 8
        if excel_path:
            ## שמירת גרף
            self.save_portfolio_graph(portfolio, portfolio_type) ## שימוש בפוקנציה מספר 7

#############################################################################################################################################   3

    def print_portfolio(self, portfolio, portfolio_type=None): # (פונקציה מרכזית) 10
        """ מציגה את תיק ההשקעות של המשתמש כאשר הוא בוחר למכור את מניותיו"""

        try:
            if not portfolio:
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty." + Style.RESET_ALL) ## כאשר ריק
                return

           ## נתונים שנעזרים בהם (בדומה לפוקציות 7 ו-8)
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
                print(Fore.BLUE + f"\nYour{' ' + portfolio_type if portfolio_type else ''} portfolio is empty." + Style.RESET_ALL) ## כאשר ריק
                return

            ## חישוב אחוזים של סוג המנייה (בדומה לפונקציות 7 ו-8)
            df = pd.DataFrame(data)
            total_portfolio_value = df['Total Value'].sum()
            df['Share'] = (df['Total Value'] / total_portfolio_value * 100)
            

            ## %% מיון לפי אחוזים בסדר יורד
            df = df.sort_values('Share', ascending=False)


            ## הוספת תווים של דולר ושל אחוז לשם התצוגה
            display_df = df.copy()
            display_df['Price'] = display_df['Price'].map('${:.2f}'.format)
            display_df['Total Value'] = display_df['Total Value'].map('${:.2f}'.format)
            display_df['Share'] = display_df['Share'].map('{:.2f}%'.format)

            print(f"\n{Fore.GREEN}Your Portfolio:{Style.RESET_ALL}")
            print(Fore.BLUE + "=" * 80 + Style.RESET_ALL)
            print(Fore.BLUE + tabulate(display_df, headers='keys', tablefmt='fancy_grid', showindex=False) + Style.RESET_ALL)
            

            ## הצגת סיכום המידע
            print(f"\n{Fore.GREEN}Portfolio Summary:{Style.RESET_ALL}")
            print(Fore.BLUE + f"Total Portfolio Value: ${total_portfolio_value:.2f}" + Style.RESET_ALL)
            
        except Exception as e:
            print(Fore.RED + f"Error displaying portfolio: {str(e)}" + Style.RESET_ALL)  ## כאשר יש שגיאה


    def show_portfolio_menu(self): # 11
        """ הצגת תפריט אפשרויות תצוגה של הפורטפוליו (אופציה 4)"""

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


    def print_menu(self, title, options): # 12 (פונקציה כללית)
        """ תוספות לתצוגת התפריטים """

        print(Fore.GREEN + "\n====================" + Style.RESET_ALL)
        print(Fore.GREEN + f"       {title}" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)
        for i, option in enumerate(options, 1):
            print(Fore.BLUE + f"{i}) {option}" + Style.RESET_ALL)
        print(Fore.GREEN + "====================" + Style.RESET_ALL)


        ######################################################################################################################################  4

    def get_input_with_validation(self, prompt, valid_options, case_sensitive=True): # 13 (פונקציה כללית)
        """מקבלת קלט מהמשתמש ומוודאת שהוא תקין"""

        while True:
            user_input = input(prompt).strip()
            
            if not case_sensitive:
                user_input = user_input.lower()  ## פונקציית הקטנה לתווים
                valid_options = [opt.lower() for opt in valid_options]
            if user_input in valid_options:
                return user_input
            print(Fore.YELLOW + f"Invalid input. Please choose from {', '.join(valid_options)}." + Style.RESET_ALL) ## הודעת שגיאה כאשר הקלט לא תקין

    def get_security_id_to_sell(self): # 14
        """ הזנת מספר זהות לשם מכירה (פונקציית מכירה שנייה)"""

        while True:
            try:
                print(Fore.BLUE + "\nEnter the ID of the security you want to sell (or press Enter to cancel):" + Style.RESET_ALL) ## מה שמוצג למשתמש
                user_input = input().strip()
                
                if not user_input:  
                    print(Fore.YELLOW + "Operation cancelled." + Style.RESET_ALL) ## כאשר בוחרים לבטל
                    return None
                    
                security_id = int(user_input)
                if security_id < 1:
                    print(Fore.YELLOW + "ID must be a positive number." + Style.RESET_ALL) ## שגיאה כאשר המספר שלילי
                    continue
                    
                return security_id
                
            except ValueError:
                print(Fore.YELLOW + "Please enter a valid number." + Style.RESET_ALL) ## שגיאה כאשר המספר לא תקין
                

    def show_security_sold_success(self): # 15
        """מציגה הודעת הצלחה למכירת נייר ערך"""

        print(Fore.GREEN + "\n=== Security Sold Successfully ===" + Style.RESET_ALL)
        print(Fore.GREEN + "✅ The security has been removed from your portfolio." + Style.RESET_ALL)

    def show_error_selling_security(self, error_msg): # 16
        """מציגה הודעת שגיאה למכירת נייר ערך"""

        print(Fore.RED + "\n=== Error Selling Security ===" + Style.RESET_ALL)
        print(Fore.RED + f"An error occurred: {error_msg}" + Style.RESET_ALL)




    def display_security_data(self, security_type): # 17 (פוקנציה מרכזית)
        """ מציגה את נתוני ניירות הערך (שימושי בתהליך הקנייה)"""

    ### חמישים מניות / אגרות חוב ממויינות בסדר יורד לפי *המחיר* ומוצגות כך

        try:
            filename = "stocks.csv" if security_type.lower() == "stock" else "bonds.csv" ## נעזרים בקבצי סי אס וי המיובאים 
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, filename)
            df = pd.read_csv(file_path)
            
            ## הוספת תווים של דולר לשם תצוגה
            df['Price'] = df['Price'].astype(str).str.replace('$', '').astype(float)
            df = df.sort_values('Price', ascending=False) ## ממיינים לפי מחיר בסדר יורד
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
            print(Fore.RED + f"\nNo {security_type}s data file found." + Style.RESET_ALL) ## כאשר אין קובץ סי אס וי (לא קורה בפרוייקט)
            return None
        except Exception as e:
            print(Fore.RED + f"Error displaying security data: {str(e)}" + Style.RESET_ALL) ## כאשר יש שגיאה בתצוגה
            return None

######################################################################################################################################   5


    def update_prices(self, security_type): # 18
        """ מסייע לפונקציה 17 - הצגת מחירים מעודכנים (שימושי בתהליך הקנייה)"""

        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            if security_type.upper() == "STOCK":
                file_path = os.path.join(current_dir, "stocks.csv") ## נעזר בסי אס וי של המניות
                security_name = "stocks"
            else:
                file_path = os.path.join(current_dir, "bonds.csv") ## נעזר בסי אס וי של אגרות החוב
                security_name = "bonds"
                
            if not os.path.exists(file_path):
                print(Fore.RED + f"Error: {security_name}.csv file not found" + Style.RESET_ALL) ## כאשר אין סי אס וי (לא קורה בפרויקט)
                return
                
            df = pd.read_csv(file_path)
            if df.empty:
                print(Fore.YELLOW + f"Warning: No {security_name} data found" + Style.RESET_ALL)  ## כאשר אין מידע לגבי נייר הערך
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
            print(Fore.RED + f"Error updating {security_type} prices: {str(e)}" + Style.RESET_ALL) ## כאשר שגיאה


    def get_security_choice(self, max_choice): # 19
        """ מבקשת מהמשתמש לבחור נייר ערך לפי מספר זהות (שימושי בתהליך הקנייה)"""

        while True:
            try:
                choice = int(input(Fore.BLUE + f"\nChoose a security (1-{max_choice}): " + Style.RESET_ALL))
                if 1 <= choice <= max_choice:
                    return choice - 1
                print(Fore.YELLOW + f"Please enter a number between 1 and {max_choice}" + Style.RESET_ALL) ## בחירה לפי מספר זהות
            except ValueError:
                print(Fore.YELLOW + "Please enter a valid number" + Style.RESET_ALL) ## כאשר מספר הזהות לא תקין


    def show_error_setting_risk_level(self, error): # 20
        """מציגה הודעת שגיאה לעדכון רמת סיכון"""

        #+ תרחיש ההצלחה הוא בפונקציה מספר 27


        print(Fore.RED + f"Error setting risk level: {error}" + Style.RESET_ALL)



    def show_security_added_success(self): # 21
        """מציגה הודעת הצלחה להוספת נייר ערך"""

        print(Fore.GREEN + "\n✅ Security added successfully." + Style.RESET_ALL)


##########################################################################################################################################   6


    def show_returning_to_main_menu(self): # 22
        """מציגה הודעה על חזרה לתפריט הראשי"""

        print(Fore.BLUE + "Returning to main menu..." + Style.RESET_ALL)



    def show_invalid_choice(self): # 23 (פונקציה כללית)
        """מציגה הודעת שגיאה לבחירה לא תקינה"""

        print(Fore.YELLOW + "Invalid choice. Please try again." + Style.RESET_ALL)

    def show_invalid_input(self): # 24
        """ מציגה הודעת שגיאה כאשר יש קלט לא תקין היכן שקולטים מספר זהות"""

        print(Fore.YELLOW + "Invalid input. Security ID must be a number." + Style.RESET_ALL)



    def show_risk_level_menu(self): # 25
        """ מציגה את תפריט רמת הסיכון. אופציה 1 בתפריט הראשי"""

        options = {
            "1": "Show current risk level",
            "2": "Set risk level",
            "3": "Return to main menu"
        }
        print(Fore.GREEN + "\n=== Risk Level Menu ===" + Style.RESET_ALL)
        for key, value in options.items():
            print(Fore.BLUE + f"{key}) {value}" + Style.RESET_ALL)
        print(Fore.GREEN + "======================" + Style.RESET_ALL)
        return self.get_input_with_validation(Fore.BLUE + "Choose an option: " + Style.RESET_ALL, list(options.keys()))


    def show_current_risk_level(self, risk_level): # 26
        """ מציגה את רמת הסיכון הנוכחית (אופציה 1,1)"""

        print(Fore.GREEN + "\n=== Current Risk Level ===" + Style.RESET_ALL)
        if risk_level:
            risk_color = {
                'low': Fore.GREEN,
                'medium': Fore.YELLOW,
                'high': Fore.RED
            }.get(risk_level.lower(), Fore.BLUE)
            print(risk_color + f"Current portfolio risk level: {risk_level.upper()}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "\nRisk level has not been set yet." + Style.RESET_ALL) ## כאשר לא נבחרה עדיין רמת סיכון
        print(Fore.GREEN + "===========================" + Style.RESET_ALL)



    def show_risk_update_success(self): # 27
        """מציגה הודעת הצלחה לעדכון רמת סיכון"""

        print(Fore.GREEN + "\n✅ Risk level updated successfully!" + Style.RESET_ALL)
