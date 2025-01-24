from stock import Stock

class PreferredStock(Stock):
    def __init__(self, name="Preferred Stock", risk_level="Low", price=2000, industry="Energy", stock_type="Preferred"):
        super().__init__(name, risk_level, price, industry, stock_type)

    def __str__(self):
        return super().__str__()

# Example usage:
if __name__ == "__main__":
    stock = PreferredStock()
    print(stock)
