from risk_calculator import SecurityType, Sector, Volatility, RiskCalculator

class Security:
    # מחלקה בסיסית שמתארת נייר ערך עם מאפיינים כלליים
    def __init__(self, name, risk_level, price, industry):
        self.name = name
        self.risk_level = risk_level
        self.price = price
        self.industry = industry
        self._risk_calculator = RiskCalculator()
        self.volatility = Volatility.HIGH if risk_level == "High" else Volatility.LOW

    def get_risk(self):
        return self.risk_level

    def calculate_risk_contribution(self, weight):
        """חישוב תרומת הסיכון של נייר הערך לתיק"""
        security_obj = {
            'Symbol': self.name,
            'Type': self._get_security_type().value,
            'Share': weight,
            'Industry': self.industry,
            'Volatility': self.volatility.value
        }
        return self._risk_calculator.calculate_security_risk(security_obj)

    def _get_security_type(self):
        """מחזיר את סוג נייר הערך - יורש על ידי המחלקות הבנות"""
        return SecurityType.STOCK

    def __str__(self):
        return f"{self.name} (Industry: {self.industry}, Risk: {self.risk_level}, Price: {self.price})"

class Stock(Security):
    # תת-מחלקה של Security שמתארת סוג ספציפי של נייר ערך – מניה
    def __init__(self, name, risk_level, price, industry, stock_type):
        super().__init__(name, risk_level, price, industry)
        self.stock_type = stock_type

    def __str__(self):
        return f"{super().__str__()}, Stock Type: {self.stock_type}"

    def _get_security_type(self):
        return SecurityType.STOCK

class PreferredStock(Stock):
    # תת-מחלקה של Stock שמתארת מניה מועדפת
    def __init__(self, name, risk_level, price, industry, stock_type):
        super().__init__(name, risk_level, price, industry, stock_type)

    def __str__(self):
        return super().__str__()

class RegularStock(Stock):
    # תת-מחלקה של Stock שמתארת מניה רגילה
    def __init__(self, name, risk_level, price, industry, stock_type):
        super().__init__(name, risk_level, price, industry, stock_type)

    def __str__(self):
        return super().__str__()

############################################

class Bond(Security):
    # תת-מחלקה של Security שמתארת נייר ערך מסוג אג"ח
    def __init__(self, name, risk_level, price, industry, bond_type):
        super().__init__(name, risk_level, price, industry)
        self.bond_type = bond_type

    def _get_security_type(self):
        return SecurityType.CORPORATE_BOND

    def __str__(self):
        return f"Bond(name: {self.name}, industry: {self.industry}, risk: {self.risk_level}, price: {self.price}, type: {self.bond_type})"

class GovernmentBond(Bond):
    # תת-מחלקה של Bond שמתארת אג"ח ממשלתי
    def __init__(self, name, risk_level, price, industry='Government', bond_type='Fixed'):
        super().__init__(name, risk_level, price, industry, bond_type)

    def _get_security_type(self):
        return SecurityType.GOVERNMENT_BOND

    def __str__(self):
        return super().__str__()

class CorporateBond(Bond):
    # תת-מחלקה של Bond שמתארת אג"ח קונצרני
    def __init__(self, name, risk_level, price, industry, bond_type):
        super().__init__(name, risk_level, price, industry, bond_type)

    def __str__(self):
        return super().__str__()
