import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crew import RiskAssessment

def test_risk_volatility():
    # Charger le JSON produit par l'agent Risk Manager
    result = RiskAssessment.parse_file("outputs/risk_report.json")

    # Vérifie que volatility est bien un nombre (float)
    assert isinstance(result.volatility, (float, int)), f"❌ Volatility is not numeric: {result.volatility}"

    # Vérifie que volatility est positive
    assert result.volatility >= 0, f"❌ Volatility must be >= 0, got {result.volatility}"

    # Affiche le résultat pendant le test (si lancé avec pytest -s)
    print(f"📊 Risk assessment for {result.ticker}: volatility={result.volatility}, level={result.risk_level}")