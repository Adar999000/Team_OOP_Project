from security import Security

class Stock(Security):
    def __init__(self, name, risk_level, price, industry, stock_type):
        super().__init__(name, risk_level, price, industry)
        self.stock_type = stock_type  # סוג המניה

    def __str__(self):
        return f"Stock(name: {self.name}, industry: {self.industry}, risk: {self.risk_level}, price: {self.price}, type: {self.stock_type})"
