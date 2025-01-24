class Security:
    def __init__(self, name, risk_level, price, industry):  # אתחול אובייקט של נייר ערך
        self.name = name  # שם נייר הערך
        self.risk_level = risk_level  # רמת סיכון
        self.price = price  # מחיר נייר הערך
        self.industry = industry  # ענף תעשייה

    def get_risk(self):  # החזרת רמת הסיכון של נייר הערך
        return self.risk_level

    def __str__(self):  # הצגת פרטי נייר הערך כטקסט
        return f"{self.name} (Industry: {self.industry}, Risk: {self.risk_level}, Price: {self.price})"