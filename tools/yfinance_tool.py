from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yfinance as yf

class YFinanceStockAnalysisInput(BaseModel):
    ticker: str = Field(..., description="stock ticker symbol.")

class YFinanceStockAnalysisTool(BaseTool):
    name: str = "YFinance Stock Analysis Tool"
    description: str = "Fetch and analyze stock using yfinance"
    args_schema: Type[BaseModel] = YFinanceStockAnalysisInput

    def _run(self, ticker: str) -> dict:
        stock = yf.Ticker(ticker)
        info = stock.info
        history = stock.history(period='5d')  # Variation 5 jours pour le trader
        variation_5d = (history['Close'][-1] - history['Close'][0]) / history['Close'][0]
        week_52_high = history['High'].tail(260).max()
        week_52_low = history['Low'].tail(260).min()
        financials = stock.financials

        if not financials.empty and 'Total Revenue' in financials.index:
            revenue_5y = financials.loc['Total Revenue'].iloc[:5]  # les 5 dernières années
            if len(revenue_5y) >= 2:  # au moins un début et une fin
                start = revenue_5y.iloc[-1]   # 5 ans avant
                end = revenue_5y.iloc[0]      # plus récent
                years = len(revenue_5y) - 1
                try:
                    revenue_growth = (end / start) ** (1 / years) - 1
                except ZeroDivisionError:
                    revenue_growth = None
            else:
                revenue_growth = None
        else:
            revenue_growth = None

        return {
            "ticker symbol": ticker,
            "company name": info.get('longName', "N/A"),
            "current price": info.get('currentPrice', 'N/A'),
            "variation_5d_%": round(variation_5d * 100, 2),
            "52-week  high": round(week_52_high, 2),
            "52-week low": round(week_52_low, 2),
            "market cap": info.get('marketCap', 'N/A'),
            "P/E ratio": info.get('trailingPE', 'N/A'),
            "P/B ratio": info.get('priceToBook', 'N/A'),
            "Debt-to-equity ratio": info.get('debtToEquity', 'N/A'),
            "Current ratio": info.get('currentRatio', 'N/A'),
            "Dividend yield (%)": info.get('dividendYield', 'N/A'),
            "5-year revenue growth rate (%)": revenue_growth,
            "Free cash flow": info.get('freeCashflow', 'N/A'),
            "Profit margin": info.get('profitMargins', 'N/A'),
            "Operating margin": info.get('operatingMargins', 'N/A'),
            "Earning growth": info.get('earningsGrowth', 'N/A'),
            "Revenue growth": info.get('revenueGrowth', 'N/A'),
            "Analyst target price": info.get('targetMedianPrice', 'N/A'),
            "Beta": info.get('beta', 'N/A'),
            "5 year average return on equity (%)": info.get('returnOnEquity', 'N/A')
        }