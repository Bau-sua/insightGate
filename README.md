# InsightGape 🕵️‍♂️ Black Box Auditor

**CrewAI-powered CLI** for **stock narrative dissonance audits**. Scrapes financials + CEO quotes, flags spin (growth claims vs flat revenue?).

[![CrewAI](https://img.shields.io/badge/CrewAI-1.14.1-blue?logo=crewai)](https://crewai.com)
[![Python](https://img.shields.io/badge/Python-3.12-green)](https://python.org)

## 🎯 What it does

1. **Financials**: AlphaVantage → Quarterly revenue/R&D/debt (last 4Q).
2. **Sentiment**: Serper → Elon quotes on growth/innovation.
3. **Audit**: LLM flags ⚠️/🚨 mismatches.
4. **Report**: MD table + PDF + SQLite log.

**Example**: `insightgape TSLA` → `outputs/2026-04-17_TSLA_audit.md/pdf`.

## 🚀 Quickstart

```bash
git clone https://github.com/your/insightGape  # Or local
cd insightGape
uv sync

# Free API keys (.env)
ALPHA_VANTAGE_KEY=your_key.alphavantage.co
SERPER_API_KEY=serper_your_key
OPENAI_API_KEY=sk-...

# Demo
insightgape demo  # Non-interactive TSLA

# Interactive
insightgape  # 1 → TSLA → y
```

## 📁 Structure

```
.
├── src/insightgape/
│   ├── main.py      # Rich CLI + WeasyPrint PDF + SQLite
│   ├── crew.py      # @CrewBase sequential crew
│   └── tools/alpha_vantage_tool.py
├── config/
│   ├── agents.yaml  # 4 agents (scraper, analyst, auditor, reporter)
│   └── tasks.yaml   # Descriptions/expected outputs
├── outputs/         # MD/PDF audits
├── audits.db        # History
├── pyproject.toml   # uv deps (crewai, pandas, alpha-vantage)
└── README.md
```

## 🧪 Agents & Tasks

**Agents** (config/agents.yaml):
- Financial Data Scraper (AlphaVantage)
- Market Sentiment Analyst (SerperDevTool)
- Dissonance Auditor (gpt-4o, reasoning=True)
- Reporting Officer (markdown=True)

**Tasks** (sequential):
1. Scrape financials → JSON quarters.
2. Gather quotes → Array [quote/source/sentiment].
3. Audit → MD table | Flag | Metric | Evidence | % |.
4. Report → Full audit MD.

## 🔧 .env Required

```
OPENAI_API_KEY=sk-...  # gpt-4o
ALPHA_VANTAGE_KEY=demo_...  # 5/min free
SERPER_API_KEY=serper_...   # 2500/month free
```

**Check**: `insightgape` → 3 (status ✅/❌).

## 📊 History

- `insightgape` → 2 → Table: ID/Ticker/Date/MD/PDF.
- `sqlite3 audits.db "SELECT * FROM audits ORDER BY date DESC;"`.

## 🧪 Testing

```bash
crewai test -n 3  # Eval crew
crewai reset-memories -a  # Clear memory
```

## 🚀 Production Deploy (CrewAI AMP)

```bash
crewai login  # app.crewai.com
crewai deploy create  # GitHub + .env → API
crewai deploy status/logs
```

**Hosted API**:
```
POST /kickoff { "ticker": "AAPL" } → Report URL.
```

## 🔍 Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `pandas not found` | AlphaVantage | `uv add pandas openpyxl` |
| `403 embeddings` | memory=True | Edit crew.py: `memory=False` |
| `No key` | .env | Add ALPHA_VANTAGE_KEY etc. |
| Verbose=2 | Old API | `verbose=True` (bool) |
| PDF fail | WeasyPrint | `uv add weasyprint` |

**Version check**: `uv run python -c "import crewai; print(crewai.__version__)"`.

## 🤝 Contribute

1. `uv sync && insightgape demo` (test).
2. Tune `config/*.yaml`.
3. `git commit -m "feat: add NVDA support"`.
4. PR!

## 📄 License

MIT.

**Built with CrewAI 1.14.1 • April 2026**
