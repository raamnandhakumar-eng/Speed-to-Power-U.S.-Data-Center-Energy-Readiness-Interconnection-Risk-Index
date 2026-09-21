from pathlib import Path

import pandas as pd
import streamlit as st

from src.evidence_model import (
    annual_cost_proxy_usd,
    annual_energy_mwh,
    load_evidence,
    load_scenarios,
    score_markets,
)
from src.utility_model_v2 import (
    Scenario,
    comed_high_voltage_core_delivery_proxy,
    dominion_gs5_obligations,
    oncor_transmission_core_delivery_proxy,
)

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Speed-to-Power", layout="wide")
st.title("Speed-to-Power")
st.caption("U.S. Data Center Energy Readiness & Interconnection Risk")

tab_v2, tab_v1, tab_method = st.tabs(
    ["Utility V2", "Regional V1", "Methodology & Sources"]
)

with tab_v2:
    st.subheader("Utility-level due diligence")
    st.write(
        "V2 compares Dominion Energy Virginia, Oncor Electric Delivery, and "
        "Commonwealth Edison. It keeps delivery charges, energy procurement, "
        "collateral, and contractual obligations separate because the utilities "
        "operate under different market structures."
    )

    c1, c2, c3, c4 = st.columns(4)
    load_mw = c1.slider("Facility load (MW)", 100, 500, 300, step=25, key="v2_load")
    load_factor = c2.slider(
        "Load factor", 0.75, 1.00, 0.90, step=0.01, key="v2_lf"
    )
    four_cp_factor = c3.slider(
        "Oncor 4CP exposure factor",
        0.40,
        1.00,
        0.90,
        step=0.05,
        key="v2_4cp",
        help="Assumed ERCOT 4CP demand as a fraction of facility maximum demand.",
    )
    credit_reduction = c4.slider(
        "Dominion credit reduction",
        0,
        70,
        0,
        step=5,
        key="v2_credit",
        help="GS-5 collateral may be reduced by up to 70% based on established credit.",
    )

    comed_demand_factor = st.slider(
        "ComEd billing-demand factor",
        0.75,
        1.00,
        1.00,
        step=0.05,
        key="v2_comed_demand",
        help="Assumed billed maximum demand as a fraction of facility maximum demand.",
    )

    scenario = Scenario(load_mw=load_mw, load_factor=load_factor)
    oncor = oncor_transmission_core_delivery_proxy(
        scenario, four_cp_factor=four_cp_factor
    )
    comed = comed_high_voltage_core_delivery_proxy(
        scenario, billing_demand_factor=comed_demand_factor
    )
    dominion = dominion_gs5_obligations(
        scenario, credit_reduction_pct=credit_reduction
    )

    st.markdown("### Scenario")
    s1, s2, s3 = st.columns(3)
    s1.metric("Full load", f"{load_mw} MW")
    s2.metric("Annual energy", f"{scenario.annual_mwh / 1_000_000:.3f} TWh")
    s3.metric("Annual load factor", f"{load_factor:.0%}")

    st.markdown("### Core outputs")
    o1, o2, o3 = st.columns(3)

    with o1:
        st.markdown("#### Oncor / ERCOT")
        st.metric("Core delivery proxy", f"${oncor['annual_usd'] / 1e6:,.2f}M/yr")
        st.metric("Core delivery proxy", f"${oncor['usd_per_mwh']:,.2f}/MWh")
        st.caption(
            "Transmission-voltage delivery only. Energy supply, construction, "
            "taxes, and several riders are excluded."
        )

    with o2:
        st.markdown("#### ComEd / PJM")
        st.metric("Core delivery proxy", f"${comed['annual_usd'] / 1e6:,.2f}M/yr")
        st.metric("Core delivery proxy", f"${comed['usd_per_mwh']:,.2f}/MWh")
        st.caption(
            "High Voltage >10 MW delivery proxy. Published ADJ factors, energy "
            "supply, PJM capacity, construction, and other riders are excluded."
        )

    with o3:
        st.markdown("#### Dominion / PJM")
        st.metric(
            "GS-5 collateral exposure",
            f"${dominion['net_collateral_usd'] / 1e6:,.0f}M",
        )
        st.metric(
            "Transmission demand floor",
            f"{dominion['minimum_transmission_demand_mw']:,.0f} MW",
        )
        st.caption(
            "This is contractual exposure, not an annual electricity bill. "
            "GS-5 takes effect January 1, 2027."
        )

    st.info(
        "Do not compare Dominion collateral directly with Oncor or ComEd annual "
        "delivery charges. V2 intentionally separates these categories."
    )

    st.markdown("### Dominion GS-5 obligations")
    dominion_table = pd.DataFrame(
        [
            ["Contract term", "14 years"],
            ["Maximum ramp period", "4 years"],
            ["Minimum annual ramp", "20%"],
            [
                "Gross collateral benchmark",
                f"${dominion['gross_collateral_usd'] / 1e6:,.0f}M",
            ],
            [
                "Net collateral at selected credit reduction",
                f"${dominion['net_collateral_usd'] / 1e6:,.0f}M",
            ],
            [
                "Minimum distribution demand",
                f"{dominion['minimum_distribution_demand_mw']:,.1f} MW",
            ],
            [
                "Minimum transmission demand",
                f"{dominion['minimum_transmission_demand_mw']:,.1f} MW",
            ],
            [
                "Minimum generation demand",
                f"{dominion['minimum_generation_demand_mw']:,.1f} MW",
            ],
        ],
        columns=["GS-5 term", "Scenario value"],
    )
    st.dataframe(dominion_table, use_container_width=True, hide_index=True)

    st.markdown("### Utility structure")
    utility_df = pd.read_csv(ROOT / "data" / "utility_v2.csv")
    utility_display = utility_df[
        [
            "utility",
            "regional_market",
            "market_structure",
            "large_load_definition",
            "connection_process_status",
            "demand_flexibility_status",
        ]
    ].rename(
        columns={
            "utility": "Utility",
            "regional_market": "Market",
            "market_structure": "Market structure",
            "large_load_definition": "Large-load treatment",
            "connection_process_status": "Connection process",
            "demand_flexibility_status": "Flexibility status",
        }
    )
    st.dataframe(utility_display, use_container_width=True, hide_index=True)

    st.markdown("### What the V2 proxies include")
    rate_df = pd.read_csv(ROOT / "data" / "utility_rate_components_v2.csv")
    st.dataframe(rate_df, use_container_width=True, hide_index=True)

with tab_v1:
    st.subheader("Regional market screening")

    df = load_evidence()
    scenarios = load_scenarios()

    c1, c2, c3 = st.columns(3)
    load_mw_v1 = c1.slider("Full load (MW)", 100, 500, 300, step=25, key="v1_load")
    target_year = c2.slider(
        "Target full energization year", 2027, 2035, 2029, key="v1_year"
    )
    load_factor_v1 = c3.slider(
        "Load factor", 0.50, 1.00, 0.90, step=0.01, key="v1_lf"
    )

    scenario_name = st.selectbox(
        "Decision profile",
        list(scenarios.keys()),
        format_func=lambda x: x.replace("_", " ").title(),
    )

    weights = scenarios[scenario_name]
    scored = score_markets(df, weights).sort_values(
        "screening_score", ascending=False
    )

    st.warning(
        "V1 is a comparative RTO screening model. It does not establish "
        "site-level transmission availability or a guaranteed energization date."
    )

    result = scored[
        [
            "market",
            "screening_score",
            "resource_adequacy_score",
            "cost_score",
            "growth_pressure_score",
            "large_load_process_maturity_score",
            "flexibility_maturity_score",
        ]
    ].rename(
        columns={
            "market": "Market",
            "screening_score": "Screening score",
            "resource_adequacy_score": "Resource adequacy",
            "cost_score": "Cost proxy",
            "growth_pressure_score": "Growth pressure",
            "large_load_process_maturity_score": "Process maturity",
            "flexibility_maturity_score": "Flexibility maturity",
        }
    )
    st.dataframe(result.round(1), use_container_width=True, hide_index=True)
    st.bar_chart(scored.set_index("market")["screening_score"])

    annual_mwh_v1 = annual_energy_mwh(load_mw_v1, load_factor_v1)
    cost_rows = []
    for _, row in scored.iterrows():
        annual_cost = annual_cost_proxy_usd(
            load_mw_v1,
            load_factor_v1,
            row["industrial_price_cents_per_kwh"],
        )
        cost_rows.append(
            {
                "Market": row["market"],
                "Price proxy state": row["representative_state"],
                "Annual energy (TWh)": annual_mwh_v1 / 1_000_000,
                "Industrial price proxy (¢/kWh)": row[
                    "industrial_price_cents_per_kwh"
                ],
                "Annual electricity-cost proxy ($M)": annual_cost / 1_000_000,
            }
        )
    st.dataframe(
        pd.DataFrame(cost_rows).round(2),
        use_container_width=True,
        hide_index=True,
    )

with tab_method:
    st.subheader("Methodology")
    st.markdown(
        """
**V1** answers: which regional market warrants deeper diligence?

**V2** answers: what do the utility tariff, market structure, and large-load
contract terms imply before a site-specific transmission study?

The next layer must be a candidate **transmission zone / substation / point of
interconnection**. No public RTO or utility-level score can replace that study.

### V2 guardrails

- Oncor and ComEd outputs are **core delivery proxies**, not complete bills.
- Dominion GS-5 outputs are **contractual exposure metrics**, not annual energy costs.
- Oncor 4CP exposure is an explicit adjustable assumption.
- ComEd's published `ADJ` factors are excluded from the proxy.
- Project-specific construction and network-upgrade costs are excluded.
- Energy procurement is outside the Oncor and ComEd delivery proxies.
"""
    )

    st.markdown("### V2 primary sources")
    sources_v2 = pd.read_csv(ROOT / "data" / "utility_sources_v2.csv")
    st.dataframe(sources_v2, use_container_width=True, hide_index=True)

    st.markdown("### V1 primary sources")
    sources_v1 = pd.read_csv(ROOT / "data" / "source_register.csv")
    st.dataframe(sources_v1, use_container_width=True, hide_index=True)
