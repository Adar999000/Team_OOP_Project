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

    def __str__(self) -> str:
        data = [[self._id, self._stock_name, self._ticker, f"${self._price:.2f}", f"{self._share:.2f}%", self._type]]
        headers = ["ID", "Stock Name", "Ticker", "Price", "Share", "Type"]
        return tabulate(data, headers=headers, tablefmt="grid")

    @staticmethod
    def display_portfolios(portfolios: list["Portfolio"]) -> str:
        data = [[p.id, p.stock_name, p.ticker, f"${p.price:.2f}", f"{p.share:.2f}%", p.type] for p in portfolios]
        headers = ["ID", "Stock Name", "Ticker", "Price", "Share", "Type"]
        return tabulate(data, headers=headers, tablefmt="grid")
