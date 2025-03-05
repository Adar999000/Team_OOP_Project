from enum import Enum
from typing import List, Dict, Union, Optional
from dataclasses import dataclass
import pandas as pd

class SecurityType(Enum):
    STOCK = "Stock"
    CORPORATE_BOND = "Corporate Bond"
    GOVERNMENT_BOND = "Government Bond"

class Sector(Enum):
    TECHNOLOGY = "Technology"
    REAL_ESTATE = "Real Estate"
    FINANCE = "Finance"
    INDUSTRY = "Industry"
    HEALTHCARE = "Healthcare"
    TRANSPORTATION = "Transportation"
    CONSUMER_GOODS = "Consumer Goods"

    @staticmethod
    def map_industry(industry: str) -> 'Sector':
        """Map detailed industry to basic sector"""
        industry_mapping = {
            # Technology
            'Consumer Electronics': Sector.TECHNOLOGY,
            'Software': Sector.TECHNOLOGY,
            'Internet': Sector.TECHNOLOGY,
            'Semiconductors': Sector.TECHNOLOGY,
            'Communication Equipment': Sector.TECHNOLOGY,
            'Information Technology Services': Sector.TECHNOLOGY,
            'Telecom Services': Sector.TECHNOLOGY,
            
            # Finance
            'Banks': Sector.FINANCE,
            'Credit Services': Sector.FINANCE,
            'Capital Markets': Sector.FINANCE,
            
            # Healthcare
            'Drug Manufacturers': Sector.HEALTHCARE,
            'Healthcare Plans': Sector.HEALTHCARE,
            'Medical Devices': Sector.HEALTHCARE,
            'Diagnostics & Research': Sector.HEALTHCARE,
            
            # Industry
            'Auto Manufacturers': Sector.INDUSTRY,
            'Aerospace & Defense': Sector.INDUSTRY,
            'Conglomerates': Sector.INDUSTRY,
            'Specialty Chemicals': Sector.INDUSTRY,
            'Utilities': Sector.INDUSTRY,
            
            # Consumer Goods
            'Retail': Sector.CONSUMER_GOODS,
            'Entertainment': Sector.CONSUMER_GOODS,
            'Beverages': Sector.CONSUMER_GOODS,
            'Household Products': Sector.CONSUMER_GOODS,
            'Footwear': Sector.CONSUMER_GOODS,
            'Tobacco': Sector.CONSUMER_GOODS,
            
            # Transportation
            'Freight': Sector.TRANSPORTATION,
            'Logistics': Sector.TRANSPORTATION,
        }
        
        # חיפוש חלקי אם אין התאמה מדויקת
        if industry not in industry_mapping:
            for key in industry_mapping:
                if key.lower() in industry.lower():
                    return industry_mapping[key]
        
        return industry_mapping.get(industry, Sector.INDUSTRY)  # ברירת מחדל - תעשייה

class Volatility(Enum):
    LOW = "Low"
    HIGH = "High"

class RiskLevel:
    LOW = (0.1, 2.5)
    MEDIUM = (2.51, 4.5)
    HIGH = (4.51, float('inf'))

    @staticmethod
    def get_level(risk_value: float) -> str:
        if RiskLevel.LOW[0] <= risk_value <= RiskLevel.LOW[1]:
            return "Low"
        elif RiskLevel.MEDIUM[0] <= risk_value <= RiskLevel.MEDIUM[1]:
            return "Medium"
        elif risk_value >= RiskLevel.HIGH[0]:
            return "High"
        return "Unknown"

@dataclass
class Security:
    name: str
    security_type: SecurityType
    sector: Sector
    volatility: Volatility
    weight: float  # As percentage (0-100)

class RiskCalculator:
    def __init__(self):
        # Base risk values
        self.LOW_VOLATILITY_RISK = 1.0
        self.HIGH_VOLATILITY_RISK = 2.0
        
        # Risk multipliers
        self.TECH_FINANCE_MULTIPLIER = 1.5
        self.OTHER_STOCK_MULTIPLIER = 1.0
        self.CORPORATE_BOND_MULTIPLIER = 0.5
        self.GOVERNMENT_BOND_RISK = 0.2

    def calculate_security_risk(self, security_data: dict) -> float:
        """חישוב סיכון לנייר ערך בודד"""
        base_risk = self.HIGH_VOLATILITY_RISK if security_data.get('volatility', 'LOW') == 'HIGH' else self.LOW_VOLATILITY_RISK
        
        if security_data['type'] == 'STOCK':
            # חישוב סיכון למניות
            if security_data['industry'] in ['Technology', 'Finance']:
                return base_risk * self.TECH_FINANCE_MULTIPLIER * security_data['share'] / 100
            return base_risk * self.OTHER_STOCK_MULTIPLIER * security_data['share'] / 100
            
        elif security_data['type'] == 'BOND':
            # חישוב סיכון לאג"ח
            industry_risk = self.TECH_FINANCE_MULTIPLIER if security_data['industry'] in ['Technology', 'Finance'] else self.OTHER_STOCK_MULTIPLIER
            if security_data.get('bond_type') == 'Government':
                # אג"ח ממשלתי - 50% מרמת הסיכון בענף
                return base_risk * industry_risk * 0.5 * security_data['share'] / 100
            else:
                # אג"ח קונצרני - 10% מרמת הסיכון בענף
                return base_risk * industry_risk * 0.1 * security_data['share'] / 100

    def validate_portfolio(self, portfolio: List[Dict]) -> bool:
        """Validate that portfolio weights sum to 100%"""
        total_weight = sum(security['share'] for security in portfolio)
        return abs(total_weight - 100.0) < 0.01

    def normalize_weights(self, portfolio: List[Dict]) -> List[Dict]:
        """Normalize portfolio weights to sum to 100%"""
        total_weight = sum(security['share'] for security in portfolio)
        for security in portfolio:
            security['share'] = (security['share'] / total_weight) * 100
        return portfolio

    def calculate_portfolio_risk(self, portfolio: List[Dict]) -> Dict[str, Union[float, str, List[Dict]]]:
        """Calculate total portfolio risk and return detailed analysis"""
        if not self.validate_portfolio(portfolio):
            portfolio = self.normalize_weights(portfolio)

        security_risks = []
        total_risk = 0.0

        for security in portfolio:
            risk = self.calculate_security_risk(security)
            total_risk += risk
            
            security_risks.append({
                "name": security['name'],
                "type": security['type'],
                "industry": security.get('industry'),
                "volatility": security.get('volatility'),
                "share": round(security['share'], 2),
                "risk_contribution": round(risk, 3)
            })

        return {
            "total_risk": round(total_risk, 2),
            "risk_level": RiskLevel.get_level(total_risk),
            "security_breakdown": security_risks
        }

    def is_security_allowed(self, security: Dict, target_risk_level: str) -> bool:
        """Check if a security is allowed based on target risk level"""
        security_risk = self.calculate_security_risk(security)
        
        if target_risk_level == "Low":
            return security_risk <= 0.5
        elif target_risk_level == "Medium":
            return security_risk <= 1.0
        return True  # High risk level allows all securities

def create_security(
    name: str,
    security_type: str,
    industry: str,
    volatility: str,
    share: float
) -> Security:
    """Create a Security object from raw data"""
    return Security(
        name=name,
        security_type=SecurityType[security_type],
        sector=Sector.map_industry(industry),
        volatility=Volatility[volatility],
        weight=share
    )