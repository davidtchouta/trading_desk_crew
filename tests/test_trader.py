import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crew import TradeOrder

def test_trader_suggested_size():
    # Charger le JSON produit par l'agent Trader
    result = TradeOrder.parse_file("outputs/trade_order.json")

    # Vérifie que suggested_size est bien défini
    assert result.suggested_size is not None

    # Vérifie que le format contient bien un nombre (par ex: "100 shares")
    try:
        order_size = int(str(result.suggested_size).split()[0])
    except Exception:
        order_size = 0

    assert order_size > 0, f"❌ Invalid suggested size: {result.suggested_size}"

    # Affiche le résultat pendant le test (si lancé avec pytest -s)
    print(f"📊 Trader suggested size for {result.ticker}: {result.suggested_size}")