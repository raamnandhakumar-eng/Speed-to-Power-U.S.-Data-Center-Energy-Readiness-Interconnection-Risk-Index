# Speed-to-Power

## U.S. Data Center Energy Readiness & Interconnection Risk

**Version:** Evidence v1  
**Updated:** September 21, 2026

### Core question

Where can a 100–500 MW data center obtain reliable power fastest, at acceptable cost and regulatory risk?

### What is working now

- PJM / ERCOT / MISO evidence dataset
- EIA June 2026 industrial electricity-price proxies
- NERC 2026–2035 demand and 2029 reliability metrics
- Current large-load process status
- Transparent process/flexibility scoring rubric
- Balanced, speed-first, cost-first, and reliability-first scenarios
- 100–500 MW scenario controls
- Annual electricity-cost proxy
- Phased energization table
- Streamlit dashboard
- Source register
- Working-paper draft

### Default 300 MW scenario

- Full load: 300 MW
- Load factor: 90%
- Annual energy: 2.365 TWh
- Phases: 50 → 125 → 225 → 300 MW

### Current evidence snapshot

| Market | Price proxy | 2029 ARM | 2029 LOLH | 2026–35 demand CAGR |
|---|---:|---:|---:|---:|
| PJM | 9.31¢/kWh | 18.9% | 9.97 h/yr | 3.14% |
| ERCOT | 6.58¢/kWh | 30.8% | 3.64 h/yr | 5.56% |
| MISO | 10.65¢/kWh | 8.6% | 6.61 h/yr | 1.38% |

**Important:** the price is a representative state industrial retail-price proxy, not a data-center tariff.

### Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Repository structure

```text
speed-to-power/
├── app.py
├── README.md
├── RUN.md
├── methodology.md
├── research_questions.md
├── requirements.txt
├── analysis/
│   └── results_v1.md
├── config/
│   ├── scenario_weights.json
│   ├── scoring_rubric.md
│   └── weights.json
├── data/
│   ├── evidence_v1.csv
│   ├── scenario_scores_v1.csv
│   ├── annual_cost_proxy_300mw.csv
│   ├── market_seed.csv
│   ├── regulatory_seed.csv
│   └── source_register.csv
├── paper/
│   ├── draft_v1.md
│   └── outline.md
└── src/
    ├── evidence_model.py
    ├── scoring_engine.py
    └── scenarios.py
```

### Interpretation rule

This is a **screening model**.

Do not translate an RTO/ISO score into a guaranteed energization date. The next layer must evaluate utility territory, transmission zone, point of interconnection, substation capacity, tariff, and network upgrades.
