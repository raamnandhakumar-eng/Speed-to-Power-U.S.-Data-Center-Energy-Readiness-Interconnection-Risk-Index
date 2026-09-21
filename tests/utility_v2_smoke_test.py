from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utility_model_v2 import (
    Scenario,
    oncor_transmission_core_delivery_proxy,
    comed_high_voltage_core_delivery_proxy,
    dominion_gs5_obligations,
)

s = Scenario(300, 0.90)

assert round(s.annual_mwh, 0) == 2365200

oncor = oncor_transmission_core_delivery_proxy(s, four_cp_factor=0.90)
assert 11_800_000 < oncor["annual_usd"] < 11_900_000
assert 5.0 < oncor["usd_per_mwh"] < 5.1

comed = comed_high_voltage_core_delivery_proxy(s)
assert 14_300_000 < comed["annual_usd"] < 14_400_000
assert 6.0 < comed["usd_per_mwh"] < 6.1

dom = dominion_gs5_obligations(s, credit_reduction_pct=70)
assert dom["gross_collateral_usd"] == 450_000_000
assert round(dom["net_collateral_usd"], 0) == 135_000_000
assert dom["minimum_distribution_demand_mw"] == 255
assert dom["minimum_transmission_demand_mw"] == 255
assert dom["minimum_generation_demand_mw"] == 180

print("All Speed-to-Power V2 utility model checks passed.")
