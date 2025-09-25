# 📊 AI-Powered Trading Desk Crew

Professional-grade **multi-agent system** simulating a trading desk with Trader, Risk Manager, and Compliance functions.

**Screenshot**:  
![Agent Architecture](./docs/screenshots/archi_trading_agent.png)

---

## 🚀 Features
- **Trader Agent**: Generates trade proposals using live market data (`yfinance`).
- **Risk Manager**: Validates volatility, exposure, leverage constraints.
- **Compliance Agent**: Enforces professional regulations from official PDF policies.
- **Summary Agent**: Produces a consolidated trading decision.
- **Modular architecture** with CrewAI + Ollama LLM.
- **Structured Outputs** via Pydantic models (JSON reports).
- **Directly usable in enterprise contexts**.

---

## 🏗️ Architecture Diagram for production on AWS
![Architecture Overview](./docs/screenshots/achi_trading_prod.png)

---

## 📂 Folder Structure
```
.
├── crew.py                        # CrewBase class, agents & tasks orchestrator
├── main.py                        # Project entrypoint
├── config/
│   ├── agents.yaml                # Agents descriptions (roles, goals, backstory)
│   └── tasks.yaml                 # Task descriptions (task flow definitions)
├── src/
│   └── services/
│       ├── compliance_rules.pdf   # Compliance documentation
│       └── risk_management_rules.pdf  # Risk management documentation
├── tools/
│   └── yfinance_tool.py           # Custom tool fetching and analyzing stock data
├── tests/
│   ├── test_trader.py             # Unit tests for Trader agent
│   ├── test_risk.py               # Unit tests for Risk Manager
│   └── test_compliance.py         # Unit tests for Compliance Manager
├── docs/
│   ├── agents.md                  # Documentation for each agent
│   ├── architecture.md            # System architecture (diagrams + explanations)
│   └── images/                    # Diagrams/illustrations
│       └── agents_workflow.png
├── notebooks/                     # Jupyter notebooks (exploration, prototyping)
│   └── analysis.ipynb
├── infra/                         # Infrastructure & deployment scripts
│   ├── docker-compose.yml         # Local container setup
│   └── k8s/
│       └── deployment.yaml        # Kubernetes deployment example
├── .env                           # Private environment variables (not committed)
├── .env.example                   # Public example env file (reference only)
├── .gitignore                     # Git ignore rules (.env, .venv, cache etc.)
├── pyproject.toml                 # Project dependencies & build configuration
├── LICENSE                        # Open-source license (MIT, Apache, etc.)
```


---

Outputs are written into `outputs/` in structured JSON + human-readable summaries.

---

## 👔 Enterprise Notes
- **Compliance & Risk docs** are stored as PDF and versioned in `/src/services/`.  
- **Auditability**: every agent produces JSON outputs with explicit rule references.  
- **Extendability**:
  - Add new PDF docs to cover other desks (e.g. FX, commodities).
  - Replace `llama2` with larger models (Mixtral, finetuned finance LLMs).  

---


## Getting Started

### Prerequisites
- Python 3.12
- [uv](https://github.com/astral-sh/uv) package manager
- Optional: Docker & Terraform for infra

### Install Dependencies
```bash
uv sync
```

---

Ensure **Ollama is running**:
```bash
# for local developement
ollama serve
ollama pull llama2
ollama pull nomic-embed-text

---

## Run Locally
```bash
uv run python main.py
```
---

## Development
### Linting

We use Ruff for linting:

```bash
ruff check . --fix
```
---

## Tests

We use pytest for unit testing:

```bash
uv run pytest
# or 
pytest -v
```
---

## Docker Support

The project includes a Dockerfile to containerize the app.

Build the Docker image:

```bash
docker build -t trading_multiagent -f infra/Dockerfile .
```

Run it :

```bash
docker run --rm trading_multiagent
```
---

## Infrastructure (Terraform)
Infrastructure is codified under terraform/ for AWS deployment with ECS Fargate & Application Load Balancer.

Steps:

- Build & push Docker image to ECR.
- Configure variables in terraform/environments/dev.tfvars.
- Deploy:

```bash
cd infra/terraform
terraform init
terraform apply -var-file=environments/dev.tfvars
```
Output:

```bash
alb_dns_name = trading_multi_agent-alb-xxxx.eu-west-1.elb.amazonaws.com
```
---

## Documentation
Additional docs are available under the docs/ directory:

- agents.md → Detailed description of each Agent
- architecture.md → Architecture overview & diagram
- screenshots/ → Illustrations & sample outputs

---

## Contributing
We welcome contributions! Please fork the repo, create a feature branch, and submit a pull request.
Before committing, run linting and tests:
```bash
ruff check . --fix
uv run pytest
```

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

--- 

Author
Developed by [David TCHATCHOUA](https://frenchtechacademie.fr/tchatchoua) — AI Engineer - AI Agents Builder.