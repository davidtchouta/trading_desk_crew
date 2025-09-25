# 🏗️ System Architecture - Trading Desk Crew

This section details the architecture of the **multi-agent trading desk**.

---

## High-Level Overview

![Agent Architecture](screenshots/achi_trading_agent.png)


---

## Data Flow
1. **Trader Agent** fetches data (YFinance).  
2. **Risk Manager** validates size, volatility, beta.  
3. **Compliance Agent** enforces policy docs (PDFSearchTool).  
4. **Summary Agent** aggregates into a final recommendation.  

---

## Tech Stack
- **Agents Framework**: [CrewAI](https://github.com/joaomdmoura/crewai)  
- **Vector DB / RAG**: ChromaDB  
- **LLM**: Ollama (`llama2`)  
- **Embeddings**: OpenAI or Ollama (`nomic-embed-text`)  
- **Tools**: 
  - YFinanceStockAnalysisTool
  - PDFSearchTool  

---


## 📂 Folder Structure
```
├── crew.py                # CrewBase class, agents & tasks orchestrator
├── main.py                # entrypoint
├── config/agents.yaml     # agents descriptions
├── config/tasks.yaml      # task descriptions
├── src/services/
│   ├── compliance_rules.pdf
│   └── risk_management_rules.pdf
├── tests/
│   ├── test_trader.py
│   ├── test_risk.py
│   └── test_compliance.py
└── docs/
    ├── agents.md
    ├── architecture.md
    └── screenshots/
```

# Production Architecture 

Coming soon !

