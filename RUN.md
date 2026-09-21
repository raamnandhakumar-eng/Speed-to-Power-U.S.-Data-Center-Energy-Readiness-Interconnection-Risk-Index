# Run the MVP

From the project folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tests/smoke_test.py
streamlit run app.py
```

The dashboard includes:

- PJM, ERCOT, and MISO evidence inputs
- configurable balanced, speed-first, cost-first, and reliability-first weights
- comparative screening scores
- resource-adequacy and demand-growth indicators
- a 100–500 MW load scenario
- annual electricity-cost proxies
- phased energization
- large-load process status
- the primary-source register

The readiness score is a comparative screening output. It is not a guaranteed energization date or a substitute for utility-, transmission-zone-, substation-, tariff-, or point-of-interconnection due diligence.
