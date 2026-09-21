from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evidence_model import load_evidence, load_scenarios, score_markets, annual_energy_mwh

df = load_evidence()
scenarios = load_scenarios()

assert set(df["market"]) == {"PJM", "ERCOT", "MISO"}
assert round(annual_energy_mwh(300, 0.90), 0) == 2365200

for name, weights in scenarios.items():
    assert abs(sum(weights.values()) - 1.0) < 1e-9
    scored = score_markets(df, weights)
    assert scored["screening_score"].between(0, 100).all()

print("All Speed-to-Power evidence model checks passed.")
