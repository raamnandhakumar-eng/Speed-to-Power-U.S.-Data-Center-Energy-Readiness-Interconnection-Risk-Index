import pandas as pd
import streamlit as st

from src.evidence_model import (
    annual_cost_proxy_usd,
    annual_energy_mwh,
    load_evidence,
    load_scenarios,
    score_markets,
)

st.set_page_config(page_title="Speed-to-Power", layout="wide")
st.title("Speed-to-Power")
st.caption("U.S. Data Center Energy Readiness & Interconnection Risk | Evidence v1")

df = load_evidence()
scenarios = load_scenarios()

st.sidebar.header("Data-center scenario")
load_mw = st.sidebar.slider("Full load (MW)", 100, 500, 300, step=25)
target_year = st.sidebar.slider("Target full energization year", 2027, 2035, 2029)
load_factor = st.sidebar.slider("Load factor", 0.50, 1.00, 0.90, step=0.01)

scenario_name = st.sidebar.selectbox(
    "Decision profile",
    list(scenarios.keys()),
    format_func=lambda x: x.replace("_", " ").title(),
)

st.sidebar.markdown("**Decision weights**")
weights = scenarios[scenario_name].copy()
custom = {}
for key, default in weights.items():
    custom[key] = st.sidebar.number_input(
        key.replace("_score", "").replace("_", " ").title(),
        min_value=0.0,
        max_value=1.0,
        value=float(default),
        step=0.05,
    )

total_weight = sum(custom.values())
if abs(total_weight - 1.0) > 1e-6:
    st.sidebar.error(f"Weights sum to {total_weight:.2f}. They must sum to 1.00.")
    st.stop()

scored = score_markets(df, custom).sort_values("screening_score", ascending=False)

annual_mwh = annual_energy_mwh(load_mw, load_factor)
c1, c2, c3 = st.columns(3)
c1.metric("Full load", f"{load_mw} MW")
c2.metric("Annual energy", f"{annual_mwh/1_000_000:.2f} TWh")
c3.metric("Target full energization", str(target_year))

st.subheader("Screening result")
st.warning(
    "This is a comparative screening score, not a claim that any region can deliver "
    "a specific MW amount by a guaranteed date. Site-level transmission and utility studies are still required."
)

result = scored[[
    "market",
    "screening_score",
    "resource_adequacy_score",
    "cost_score",
    "growth_pressure_score",
    "large_load_process_maturity_score",
    "flexibility_maturity_score",
]].rename(columns={
    "market": "Market",
    "screening_score": "Screening score",
    "resource_adequacy_score": "Resource adequacy",
    "cost_score": "Cost proxy",
    "growth_pressure_score": "Growth pressure",
    "large_load_process_maturity_score": "Process maturity",
    "flexibility_maturity_score": "Flexibility maturity",
})
st.dataframe(result.round(1), use_container_width=True, hide_index=True)
st.bar_chart(scored.set_index("market")["screening_score"])

st.subheader("Observed evidence")
observed = scored[[
    "market",
    "representative_state",
    "industrial_price_cents_per_kwh",
    "anticipated_reserve_margin_2029_pct",
    "reference_margin_2029_pct",
    "reserve_margin_headroom_2029_pct_points",
    "lolh_2029_hours",
    "summer_peak_cagr_2026_2035_pct",
    "nerc_2029_risk_category",
]].rename(columns={
    "market": "Market",
    "representative_state": "Price proxy state",
    "industrial_price_cents_per_kwh": "Industrial price (¢/kWh)",
    "anticipated_reserve_margin_2029_pct": "2029 ARM (%)",
    "reference_margin_2029_pct": "2029 reference margin (%)",
    "reserve_margin_headroom_2029_pct_points": "2029 ARM headroom (pp)",
    "lolh_2029_hours": "2029 LOLH (hours/year)",
    "summer_peak_cagr_2026_2035_pct": "2026–35 peak-demand CAGR (%)",
    "nerc_2029_risk_category": "NERC 2029 risk",
})
st.dataframe(observed.round(2), use_container_width=True, hide_index=True)

st.subheader("Annual electricity-cost proxy")
cost_rows = []
for _, row in scored.iterrows():
    annual_cost = annual_cost_proxy_usd(
        load_mw,
        load_factor,
        row["industrial_price_cents_per_kwh"],
    )
    cost_rows.append({
        "Market": row["market"],
        "Price proxy state": row["representative_state"],
        "Annual energy (TWh)": annual_mwh / 1_000_000,
        "Industrial price proxy (¢/kWh)": row["industrial_price_cents_per_kwh"],
        "Annual electricity-cost proxy ($M)": annual_cost / 1_000_000,
    })
st.dataframe(pd.DataFrame(cost_rows).round(2), use_container_width=True, hide_index=True)
st.caption(
    "This is a screening calculation using EIA state industrial retail prices. "
    "It excludes negotiated large-load tariffs, demand charges, transmission, riders, taxes, backup generation, and hedging."
)

st.subheader("Large-load process")
process = scored[[
    "market",
    "large_load_process_status",
    "large_load_threshold_note",
    "process_note",
]].rename(columns={
    "market": "Market",
    "large_load_process_status": "Status",
    "large_load_threshold_note": "Threshold / scope",
    "process_note": "Current evidence",
})
st.dataframe(process, use_container_width=True, hide_index=True)

st.subheader("Phased energization")
phases = pd.DataFrame([
    {"Year": 1, "MW": min(50, load_mw)},
    {"Year": 2, "MW": min(125, load_mw)},
    {"Year": 3, "MW": min(225, load_mw)},
    {"Year": 4, "MW": load_mw},
]).drop_duplicates(subset=["MW"])
phases["Annualized energy at selected LF (GWh)"] = phases["MW"] * load_factor * 8760 / 1000
st.dataframe(phases.round(1), use_container_width=True, hide_index=True)

with st.expander("Methodology and caveats"):
    st.markdown(
        """
**Observed evidence** comes from EIA and NERC.

**Process maturity** and **flexibility maturity** are transparent policy-status indicators.
They are not physical measures of grid capacity.

**Normalization** is relative to the three markets in this MVP, so a 100 does not mean
perfect performance and a 0 does not mean unusable.

For a real siting decision, the next unit of analysis must be the utility territory,
transmission zone, substation/POI, and actual tariff.
"""
    )

st.subheader("Source register")
sources = pd.read_csv("data/source_register.csv")
st.dataframe(sources[["organization", "title", "as_of", "used_for", "url"]], use_container_width=True, hide_index=True)
