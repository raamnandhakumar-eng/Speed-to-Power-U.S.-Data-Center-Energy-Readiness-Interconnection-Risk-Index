"""Northern Virginia transmission-development readiness model for V3.

The V3 index measures documented project-development maturity.
It does NOT estimate unused substation capacity, available MW, or a guaranteed
energization date.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

WEIGHTS = {
    "stage_score": 0.40,
    "regulatory_score": 0.30,
    "schedule_score": 0.15,
    "load_linkage_score": 0.15,
}

DP_CAP_MW = 300.0
LARGE_LOAD_THRESHOLD_MW = 100.0


def transmission_development_readiness(
    stage_score: float,
    regulatory_score: float,
    schedule_score: float,
    load_linkage_score: float,
) -> float:
    """Return the documented-maturity score on a 0-100 scale."""
    values = {
        "stage_score": stage_score,
        "regulatory_score": regulatory_score,
        "schedule_score": schedule_score,
        "load_linkage_score": load_linkage_score,
    }
    for name, value in values.items():
        if not 0 <= value <= 100:
            raise ValueError(f"{name} must be between 0 and 100")

    return round(
        sum(values[key] * weight for key, weight in WEIGHTS.items()),
        2,
    )


def required_delivery_points(load_mw: float, cap_mw: float = DP_CAP_MW) -> int:
    """Minimum number of Dominion delivery-point requests implied by the DP cap."""
    if load_mw <= 0:
        raise ValueError("load_mw must be positive")
    if cap_mw <= 0:
        raise ValueError("cap_mw must be positive")
    return math.ceil(load_mw / cap_mw)


def is_large_load_queue_scenario(load_mw: float) -> bool:
    """Whether a scenario meets the approximately 100 MW queue threshold."""
    if load_mw <= 0:
        raise ValueError("load_mw must be positive")
    return load_mw >= LARGE_LOAD_THRESHOLD_MW


def queue_scenario(load_mw: float) -> dict:
    """Summarize the public-rule implications for a hypothetical requested load."""
    return {
        "load_mw": load_mw,
        "meets_large_load_threshold": is_large_load_queue_scenario(load_mw),
        "minimum_delivery_points": required_delivery_points(load_mw),
        "delivery_point_cap_mw": DP_CAP_MW,
        "formal_large_load_threshold_mw": LARGE_LOAD_THRESHOLD_MW,
    }


def load_projects() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data" / "nova_transmission_projects_v3.csv")


def load_nodes() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data" / "nova_load_nodes_v3.csv")


def verify_project_scores(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Recalculate TDRI from raw component scores and verify stored values."""
    if df is None:
        df = load_projects()

    out = df.copy()
    out["tdri_recalculated"] = out.apply(
        lambda row: transmission_development_readiness(
            row["stage_score"],
            row["regulatory_score"],
            row["schedule_score"],
            row["load_linkage_score"],
        ),
        axis=1,
    )
    out["score_matches"] = (
        out["tdri_recalculated"].round(2) == out["tdri_score"].round(2)
    )
    return out


if __name__ == "__main__":
    projects = verify_project_scores()
    print(
        projects[
            ["project", "tdri_score", "tdri_recalculated", "score_matches"]
        ].to_string(index=False)
    )
    for load in (100, 300, 500):
        print(load, queue_scenario(load))
