from crew import TradingDeskCrew
from rich.console import Console
from rich.markdown import Markdown

def main():
    # Inputs for trading Agents
    inputs = {
        "stock_symbol": "ETH",             # ie: BTC, UBS, NVDA, Apple : AAPL, Microsoft : MSFT, Google : GOOGL, Amazon : AMZN, Tesla : TSLA
        "order_size": "50 shares",   # size of the order
        "max_risk": "moderate"        # risk tolerance level
    }
    return TradingDeskCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    print("📈 Welcome to your Trading Multi-Agent System")
    print('---------------------------------------------')
    result = main()
    print("\n\n############################")
    print("## 🧐 Final Multi-Agent Report")
    print("############################\n\n")

    # Save in markdown
    with open("outputs/trading_results.md", "w", encoding="utf-8") as f:
        f.write(result.raw)

    # print in the terminal
    console = Console()
    md = Markdown(result.raw)
    console.print(md)

    