"""Evidence-based screening model for Speed-to-Power v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def minmax(series: pd.Series, higher_is_better: bool) -> pd.Series:
    lo = float(series.min())
    hi = float(series.max())
    if hi == lo:
        return pd.Series([50.0] * len(series), index=series.index)
    out = (series.astype(float) - lo) / (hi - lo) * 100.0
    if not higher_is_better:
        out = 100.0 - out
    return out


def load_evidence() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data" / "evidence_v1.csv")


def load_scenarios() -> Dict[str, Dict[str, float]]:
    return json.loads((ROOT / "config" / "scenario_weights.json").read_text())


def score_markets(df: pd.DataFrame, weights: Dict[str, float]) -> pd.DataFrame:
    required = {
        "industrial_price_cents_per_kwh",
        "anticipated_reserve_margin_2029_pct",
        "lolh_2029_hours",
        "summer_peak_cagr_2026_2035_pct",
        "large_load_process_maturity_score",
        "flexibility_maturity_score",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("Weights must sum to 1.0")

    out = df.copy()

    out["cost_score"] = minmax(out["industrial_price_cents_per_kwh"], False)
    out["reserve_margin_score"] = minmax(out["anticipated_reserve_margin_2029_pct"], True)
    out["lolh_score"] = minmax(out["lolh_2029_hours"], False)
    out["resource_adequacy_score"] = (
        out["reserve_margin_score"] + out["lolh_score"]
    ) / 2.0
    out["growth_pressure_score"] = minmax(
        out["summer_peak_cagr_2026_2035_pct"], False
    )

    out["screening_score"] = sum(out[col] * weight for col, weight in weights.items())
    out["screening_score"] = out["screening_score"].round(2)

    return out


def annual_energy_mwh(load_mw: float, load_factor: float) -> float:
    return load_mw * load_factor * 8760.0


def annual_cost_proxy_usd(
    load_mw: float, load_factor: float, cents_per_kwh: float
) -> float:
    mwh = annual_energy_mwh(load_mw, load_factor)
    return mwh * 1000.0 * cents_per_kwh / 100.0


if __name__ == "__main__":
    df = load_evidence()
    scenarios = load_scenarios()
    for name, weights in scenarios.items():
        scored = score_markets(df, weights)
        print(f"\n{name}")
        print(scored[["market", "screening_score"]].sort_values("screening_score", ascending=False).to_string(index=False))
