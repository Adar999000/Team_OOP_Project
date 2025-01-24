# Team_OOP_Project
# Portfolio Management System

A comprehensive financial portfolio management system implemented in Python, allowing users to manage and track various financial instruments including stocks and bonds.

## Features

- Support for multiple security types:
  - Stocks (Regular and Preferred)
  - Bonds (Government and Corporate)
- Portfolio management and tracking
- Interactive chatbot assistance
- Data persistence using SQLite database
- CSV data import/export capabilities

## Project Structure

- [main.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/main.py:0:0-0:0) - Application entry point
- [controller.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/controller.py:0:0-0:0) - Main application controller
- [model1.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/model1.py:0:0-0:0) - Data model implementation
- [view1.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/view1.py:0:0-0:0) - User interface implementation
- [chatbot.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/chatbot.py:0:0-0:0) - Interactive chatbot functionality
- [portfolio.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/portfolio.py:0:0-0:0) - Portfolio management logic

### Security Classes
- [security.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/security.py:0:0-0:0) - Base security class
- [stock.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/stock.py:0:0-0:0) - Stock base class
- [regular_stock.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/regular_stock.py:0:0-0:0) - Regular stock implementation
- [preferred_stock.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/preferred_stock.py:0:0-0:0) - Preferred stock implementation
- [bond.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/bond.py:0:0-0:0) - Bond base class
- [government_bond.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/government_bond.py:0:0-0:0) - Government bond implementation
- [corporate_bond.py](cci:7://file:///c:/Users/adar0/Team_OOP_Project/verison1.2/corporate_bond.py:0:0-0:0) - Corporate bond implementation

## Requirements

- Python 3.x
- Required Python packages (recommend listing specific versions used)

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install required packages

## Usage

Run the application by executing:
```python
python main.py
