from stock import Stock

class RegularStock(Stock):
    def __init__(self, name="Regular Stock", risk_level="Medium", price=1500, industry="Technology", stock_type="Regular"):
        super().__init__(name, risk_level, price, industry, stock_type)

    def __str__(self):
        return super().__str__()

# Example usage:
if __name__ == "__main__":
    stock = RegularStock()
    print(stock)
