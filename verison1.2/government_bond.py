from bond import Bond

class GovernmentBond(Bond):
    def __init__(self, name="Government Bond", risk_level="Low", price=1000, industry="Government", bond_type="Government"):
        super().__init__(name, risk_level, price, industry, bond_type)

    def __str__(self):
        return super().__str__()

# Example usage:
if __name__ == "__main__":
    bond = GovernmentBond()
    print(bond)
