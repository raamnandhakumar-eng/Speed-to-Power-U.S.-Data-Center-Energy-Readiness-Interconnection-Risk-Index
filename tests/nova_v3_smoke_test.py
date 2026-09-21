from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.nova_readiness_v3 import (
    load_nodes,
    queue_scenario,
    required_delivery_points,
    transmission_development_readiness,
    verify_project_scores,
)

assert required_delivery_points(100) == 1
assert required_delivery_points(300) == 1
assert required_delivery_points(500) == 2

assert queue_scenario(100)["meets_large_load_threshold"] is True
assert queue_scenario(500)["minimum_delivery_points"] == 2

score = transmission_development_readiness(100, 100, 100, 70)
assert score == 95.5

verified = verify_project_scores()
assert verified["score_matches"].all()

nodes = load_nodes()
assert set(nodes["substation"]) == {
    "Twin Creeks",
    "Sycolin Creek",
    "Starlight",
    "Lunar",
    "Apollo",
}
assert int(nodes["dp_requested_load_mw"].sum()) == 1372

print("All Northern Virginia V3 checks passed.")
