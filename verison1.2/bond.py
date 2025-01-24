from security import Security

class Bond(Security):
    def __init__(self, name, risk_level, price, industry, bond_type):
        super().__init__(name, risk_level, price, industry)
        self.bond_type = bond_type  # סוג האג"ח

    def __str__(self):
        return f"Bond(name: {self.name}, industry: {self.industry}, risk: {self.risk_level}, price: {self.price}, type: {self.bond_type})"