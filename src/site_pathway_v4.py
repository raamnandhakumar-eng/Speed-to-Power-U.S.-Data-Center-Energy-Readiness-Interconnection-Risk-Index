"""Northern Virginia V4 candidate-pathway model.

V4 compares PUBLIC DEVELOPMENT PATHWAY EVIDENCE.

It does not identify an available parcel, estimate unused substation capacity,
or predict a guaranteed energization date.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Optional

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DP_CAP_MW = 300.0

WEIGHTS = {
    "load_fit_score": 0.30,
    "delivery_point_fit_score": 0.15,
    "transmission_maturity_score": 0.25,
    "schedule_alignment_score": 0.20,
    "bridge_ratio_score": 0.05,
    "evidence_completeness_score": 0.05,
}


def required_delivery_points(load_mw: float) -> int:
    if load_mw <= 0:
        raise ValueError("load_mw must be positive")
    return math.ceil(load_mw / DP_CAP_MW)


def load_fit_score(documented_load_mw: Optional[float], scenario_load_mw: float) -> Optional[float]:
    if pd.isna(documented_load_mw):
        return None
    return round(min(100.0, float(documented_load_mw) / scenario_load_mw * 100.0), 2)


def delivery_point_fit_score(
    documented_delivery_points: Optional[float],
    scenario_load_mw: float,
) -> Optional[float]:
    if pd.isna(documented_delivery_points):
        return None
    required = required_delivery_points(scenario_load_mw)
    return round(min(100.0, float(documented_delivery_points) / required * 100.0), 2)


def schedule_alignment_score(latest_target: Optional[str], target_year: int) -> Optional[float]:
    if latest_target is None or pd.isna(latest_target) or str(latest_target).strip() == "":
        return None
    year = int(str(latest_target)[:4])
    if year <= target_year:
        return 100.0
    if year == target_year + 1:
        return 60.0
    return 20.0


def bridge_ratio_score(bridge_reference_mva: Optional[float], scenario_load_mw: float) -> float:
    if bridge_reference_mva is None or pd.isna(bridge_reference_mva):
        return 0.0
    return round(min(100.0, float(bridge_reference_mva) / scenario_load_mw * 100.0), 2)


def evidence_completeness_score(row: pd.Series) -> float:
    fields = [
        "serving_substations",
        "documented_load_mw",
        "documented_delivery_points",
        "latest_target",
        "direct_transmission_project",
        "direct_project_tdri",
    ]
    present = 0
    for field in fields:
        value = row.get(field)
        if value is not None and not pd.isna(value) and str(value).strip() != "":
            present += 1
    return round(present / len(fields) * 100.0, 2)


def technical_pathway_score(row: pd.Series, scenario_load_mw: float, target_year: int) -> Optional[float]:
    """Score only when load and delivery-point evidence are public.

    Corridor-only records intentionally return None.
    """
    load_score = load_fit_score(row.get("documented_load_mw"), scenario_load_mw)
    dp_score = delivery_point_fit_score(row.get("documented_delivery_points"), scenario_load_mw)

    if load_score is None or dp_score is None:
        return None

    metrics = {
        "load_fit_score": load_score,
        "delivery_point_fit_score": dp_score,
        "transmission_maturity_score": float(row["direct_project_tdri"]),
        "schedule_alignment_score": schedule_alignment_score(
            row.get("latest_target"), target_year
        ),
        "bridge_ratio_score": bridge_ratio_score(
            row.get("bridge_reference_mva"), scenario_load_mw
        ),
        "evidence_completeness_score": evidence_completeness_score(row),
    }

    if metrics["schedule_alignment_score"] is None:
        return None

    return round(
        sum(metrics[name] * weight for name, weight in WEIGHTS.items()),
        2,
    )


def load_pathways() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data" / "nova_candidate_pathways_v4.csv")


def score_pathways(scenario_load_mw: float, target_year: int) -> pd.DataFrame:
    df = load_pathways().copy()

    df["required_delivery_points"] = required_delivery_points(scenario_load_mw)
    df["load_fit_score"] = df["documented_load_mw"].apply(
        lambda x: load_fit_score(x, scenario_load_mw)
    )
    df["delivery_point_fit_score"] = df["documented_delivery_points"].apply(
        lambda x: delivery_point_fit_score(x, scenario_load_mw)
    )
    df["schedule_alignment_score"] = df["latest_target"].apply(
        lambda x: schedule_alignment_score(x, target_year)
    )
    df["bridge_ratio_score"] = df["bridge_reference_mva"].apply(
        lambda x: bridge_ratio_score(x, scenario_load_mw)
    )
    df["evidence_completeness_score"] = df.apply(evidence_completeness_score, axis=1)
    df["technical_pathway_score"] = df.apply(
        lambda row: technical_pathway_score(row, scenario_load_mw, target_year),
        axis=1,
    )
    return df


if __name__ == "__main__":
    for load in (100, 300, 500):
        scored = score_pathways(load, 2029)
        print(f"\nScenario: {load} MW by 2029")
        print(
            scored[
                [
                    "pathway_name",
                    "technical_pathway_score",
                    "evidence_completeness_score",
                ]
            ].to_string(index=False)
        )
