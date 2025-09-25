from pydantic import BaseModel, Field
from typing import Optional
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
import os

from tools.yfinance_tool import YFinanceStockAnalysisTool
from crewai_tools import PDFSearchTool

# Load environment variables from .env
load_dotenv()  

# === LLM Configuration === 
# llm = LLM(
#     model=os.getenv("MODEL", "ollama/qwen2.5:7b"),
#     base_url=os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
# )



llm = LLM(
    model="openai/gpt-4o", # call model by provider/model_name
)


# ---------- OUTPUT MODELS (like MealPlanner, but for trading) ----------
class TradeOrder(BaseModel):
    """Represents an order proposed by the Trader"""
    ticker: str = Field(description="Stock ticker (e.g. AAPL, MSFT)")
    action: str = Field(description="BUY, SELL, HOLD")
    justification: str = Field(description="Why this order is recommended")
    suggested_size: Optional[str] = Field(default="standard", description="Order size (e.g. 100 shares)")


class RiskAssessment(BaseModel):
    """Evaluation by the Risk Manager"""
    ticker: str
    risk_level: str = Field(description="Low, Medium, High")
    volatility: float = Field(description="Estimated annualized volatility")
    comment: str = Field(description="Justification of the risk level")


class ComplianceReport(BaseModel):
    """Validation by the Compliance Manager"""
    ticker: str
    compliant: bool = Field(description="True if the order is valid")
    issues: Optional[str] = Field(default="None", description="Compliance issues detected")


# ----------------------------------------------------------------------
#                     CREW CREATION
# ----------------------------------------------------------------------
@CrewBase
class TradingDeskCrew():
    """Simulates a trading desk with trader, risk manager, and compliance managers"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # --- Trader Agent ---
    @agent
    def trader_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['trader_agent'],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def trading_task(self) -> Task:
        return Task(
            config=self.tasks_config['trading_task'],
            tools=[YFinanceStockAnalysisTool()],
            agent=self.trader_agent(),
            output_pydantic=TradeOrder,   # expected = structured order
            output_file='outputs/trade_order.json'
        )

    # --- Risk Manager Agent ---
    @agent
    def risk_manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['risk_manager_agent'],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def risk_manager_task(self) -> Task:
        return Task(
            config=self.tasks_config['risk_manager_task'],
            agent=self.risk_manager_agent(),
            tools=[PDFSearchTool(pdf="src\\services\\risk_rules.pdf")],
            depends_on=[self.trading_task()],
            output_pydantic=RiskAssessment,
            output_file='outputs/risk_report.json'
        )

    # --- Compliance Manager Agent ---
    @agent
    def compliance_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['compliance_agent'],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def compliance_task(self) -> Task:
        return Task(
            config=self.tasks_config['compliance_task'],
            agent=self.compliance_agent(),
            tools=[PDFSearchTool(pdf="src\\services\\compliance_rules.pdf")], 
            depends_on=[self.trading_task(), self.risk_manager_task()],
            output_pydantic=ComplianceReport,
            output_file='outputs/compliance_report.json'
        )
    

    @agent
    def summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summary_agent'],
            llm=llm,
            allow_delegation=False,
                verbose=True
        )
    
    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['summary_task'],
            agent=self.summary_agent(),
            depends_on=[self.trading_task(), self.risk_manager_task(), self.compliance_task()],
            verbose=True
        )

    # --- Crew Orchestration ---
    @crew
    def crew(self) -> Crew:
        """Assembles the agents (Trader, Risk Manager, Compliance)"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            tracing=True  # <<--- activated logs for debugging
        )