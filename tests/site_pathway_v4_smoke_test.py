from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.site_pathway_v4 import (
    required_delivery_points,
    score_pathways,
)

assert required_delivery_points(100) == 1
assert required_delivery_points(300) == 1
assert required_delivery_points(500) == 2

s300 = score_pathways(300, 2029)
campus = s300[s300["evidence_class"] == "Public campus precedent"]
corridors = s300[s300["evidence_class"] == "Corridor evidence"]

assert len(campus) == 3
assert campus["technical_pathway_score"].notna().all()
assert corridors["technical_pathway_score"].isna().all()

s500 = score_pathways(500, 2029).set_index("pathway_id")
assert s500.loc["B", "delivery_point_fit_score"] == 100
assert s500.loc["C", "delivery_point_fit_score"] == 100
assert s500.loc["A", "delivery_point_fit_score"] == 50
assert s500.loc["A", "load_fit_score"] == 60

print("All Northern Virginia V4 candidate-pathway checks passed.")
