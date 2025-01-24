from tabulate import tabulate


class Portfolio:
    def __init__(self, id: int, stock_name: str, ticker: str, price: float, share: float, type: str):
        self._id = id
        self._stock_name = stock_name
        self._ticker = ticker
        self._price = price
        self._share = share
        self._type = type.upper()  # STOCK או BOND

    @property
    def id(self) -> int:
        return self._id

    @property
    def stock_name(self) -> str:
        return self._stock_name

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    @property
    def share(self) -> float:
        return self._share

    @share.setter
    def share(self, value: float):
        if not 0 <= value <= 100:
            raise ValueError("Share percentage must be between 0 and 100")
        self._share = value

    @property
    def type(self) -> str:
        return self._type

    def _format_table(self, headers, data):
        """Helper method to format data as a table"""
        # Calculate column widths
        widths = [len(str(h)) for h in headers]
        for row in data:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        
        # Create format string for rows
        format_str = "  ".join(f"{{:<{w}}}" for w in widths)
        
        # Create the table string
        table = [format_str.format(*headers)]
        table.append("-" * (sum(widths) + 2 * (len(widths) - 1)))
        
        for row in data:
            table.append(format_str.format(*[str(cell) for cell in row]))
        
        return "\n".join(table)

    def to_string(self):
        """Convert portfolio item to string representation"""
        headers = ['ID', 'Name', 'Ticker', 'Price ($)', 'Share (%)', 'Type']
        data = [[
            self.id,
            self.stock_name,
            self.ticker,
            f"{self.price:,.2f}",
            f"{self.share:.2f}%",
            self.type
        ]]
        return self._format_table(headers, data)

    def __str__(self):
        """String representation of the portfolio item"""
        return self.to_string()

    @staticmethod
    def display_portfolios(portfolios: list["Portfolio"]) -> str:
        headers = ['ID', 'Name', 'Ticker', 'Price ($)', 'Share (%)', 'Type']
        data = [[
            p.id,
            p.stock_name,
            p.ticker,
            f"{p.price:,.2f}",
            f"{p.share:.2f}%",
            p.type
        ] for p in portfolios]
        
        # שימוש ב-tabulate להצגת הטבלה בפורמט "fancy_grid"
        return tabulate(data, headers, tablefmt="fancy_grid", stralign="center")

