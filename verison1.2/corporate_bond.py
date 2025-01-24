from bond import Bond

class CorporateBond(Bond):
    def __init__(self, name="Corporate Bond", risk_level="Medium", price=1200, industry="Corporate", bond_type="Corporate"):
        super().__init__(name, risk_level, price, industry, bond_type)

    def __str__(self):
        return super().__str__()

# Example usage:
if __name__ == "__main__":
    bond = CorporateBond()
    print(bond)
