# Run the MVP

From the project folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The dashboard currently exposes verified price benchmarks and the regulatory-process snapshot.
It deliberately withholds a composite readiness score until the remaining variables have sourced data.
