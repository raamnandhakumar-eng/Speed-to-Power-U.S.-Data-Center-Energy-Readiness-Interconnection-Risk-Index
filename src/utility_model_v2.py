"""Utility-level V2 models for Speed-to-Power.

The functions below intentionally separate:
1) utility delivery-charge proxies for Oncor and ComEd, and
2) Dominion GS-5 contractual/collateral exposure.

They are not all-in electricity bills and should not be combined into one
"cheapest utility" ranking.
"""

from __future__ import annotations

from dataclasses import dataclass


HOURS_PER_YEAR = 8760.0


@dataclass(frozen=True)
class Scenario:
    load_mw: float
    load_factor: float = 0.90

    @property
    def load_kw(self) -> float:
        return self.load_mw * 1000.0

    @property
    def annual_kwh(self) -> float:
        return self.load_kw * self.load_factor * HOURS_PER_YEAR

    @property
    def annual_mwh(self) -> float:
        return self.annual_kwh / 1000.0


def oncor_transmission_core_delivery_proxy(
    scenario: Scenario,
    four_cp_factor: float = 0.90,
    include_interim_surcharge: bool = True,
) -> dict:
    """Core 2026 Oncor transmission-voltage delivery proxy.

    Included:
    - Customer charge: $258.80/month
    - Metering charge: $321.63/month
    - Distribution System Charge: $0.331004 per billing kW-month
    - TCRF effective Aug. 1, 2026: $3.491759 per 4CP kW-month
    - Interim surcharge: -$0.182495 per billing kW-month, if enabled

    Excluded:
    - REP energy supply
    - construction contributions / special facilities
    - EECRF, RCE, taxes, and other riders
    - any project-specific contractual terms
    """
    if not 0 <= four_cp_factor <= 1.25:
        raise ValueError("four_cp_factor must be between 0 and 1.25")

    kw = scenario.load_kw
    four_cp_kw = kw * four_cp_factor

    customer_charge = 258.80
    metering_charge = 321.63
    distribution_system_charge = 0.331004 * kw
    tcrf = 3.491759 * four_cp_kw
    interim = (-0.182495 * kw) if include_interim_surcharge else 0.0

    monthly = (
        customer_charge
        + metering_charge
        + distribution_system_charge
        + tcrf
        + interim
    )
    annual = monthly * 12.0

    return {
        "monthly_usd": monthly,
        "annual_usd": annual,
        "usd_per_mwh": annual / scenario.annual_mwh,
        "four_cp_kw": four_cp_kw,
    }


def comed_high_voltage_core_delivery_proxy(
    scenario: Scenario,
    billing_demand_factor: float = 1.0,
) -> dict:
    """Core 2026 ComEd High Voltage >10 MW delivery proxy.

    Included:
    - Customer charge: $719.73/month
    - Standard metering service charge: $32.00/month
    - HV DFC >10 MW: $0.51/kW-month
    - HV Transformer Charge >10 MW: $2.65/kW-month
    - IEDT: $0.00124/kWh

    Excluded:
    - published ADJ factors
    - retail energy supply / PJM capacity
    - project-specific construction or interconnection costs
    - other applicable riders and taxes

    Assumes the relevant portion of load is served at >=69 kV and the customer's
    maximum kilowatt demand exceeded 10 MW.
    """
    if not 0 <= billing_demand_factor <= 1.25:
        raise ValueError("billing_demand_factor must be between 0 and 1.25")

    billing_kw = scenario.load_kw * billing_demand_factor
    customer_charge = 719.73
    metering_charge = 32.00
    demand_charges = (0.51 + 2.65) * billing_kw
    monthly = customer_charge + metering_charge + demand_charges
    annual_demand_and_fixed = monthly * 12.0
    iedt = 0.00124 * scenario.annual_kwh
    annual = annual_demand_and_fixed + iedt

    return {
        "monthly_demand_and_fixed_usd": monthly,
        "annual_usd": annual,
        "annual_iedt_usd": iedt,
        "usd_per_mwh": annual / scenario.annual_mwh,
        "billing_kw": billing_kw,
    }


def dominion_gs5_obligations(
    scenario: Scenario,
    credit_reduction_pct: float = 0.0,
) -> dict:
    """Dominion GS-5 contractual exposure effective Jan. 1, 2027.

    The SCC approved:
    - GS-5 applicability at >=25 MW and >=75% load factor
    - 14-year contract term
    - ramp period up to four years with >=20% annual ramp
    - collateral of $1.5M/MW, reducible up to 70% based on credit
    - minimum demand floors of 85% distribution, 85% transmission,
      and 60% generation

    Returns obligations in physical/contractual units, not an annual power bill.
    """
    if scenario.load_mw < 25:
        raise ValueError("GS-5 applies at 25 MW or greater")
    if not 0 <= credit_reduction_pct <= 70:
        raise ValueError("credit_reduction_pct must be between 0 and 70")

    gross_collateral = scenario.load_mw * 1_500_000.0
    net_collateral = gross_collateral * (1.0 - credit_reduction_pct / 100.0)

    return {
        "gross_collateral_usd": gross_collateral,
        "net_collateral_usd": net_collateral,
        "minimum_distribution_demand_mw": scenario.load_mw * 0.85,
        "minimum_transmission_demand_mw": scenario.load_mw * 0.85,
        "minimum_generation_demand_mw": scenario.load_mw * 0.60,
        "contract_term_years": 14,
        "max_ramp_years": 4,
        "minimum_annual_ramp_pct": 20,
    }


def comparison_rows(
    load_mw: float,
    load_factor: float = 0.90,
    four_cp_factor: float = 0.90,
    comed_billing_demand_factor: float = 1.0,
    dominion_credit_reduction_pct: float = 0.0,
) -> list[dict]:
    scenario = Scenario(load_mw=load_mw, load_factor=load_factor)
    oncor = oncor_transmission_core_delivery_proxy(scenario, four_cp_factor)
    comed = comed_high_voltage_core_delivery_proxy(
        scenario, comed_billing_demand_factor
    )
    dominion = dominion_gs5_obligations(
        scenario, dominion_credit_reduction_pct
    )

    return [
        {
            "utility": "Oncor Electric Delivery",
            "metric": "Core delivery proxy",
            "annual_usd": oncor["annual_usd"],
            "usd_per_mwh": oncor["usd_per_mwh"],
            "comparison_type": "delivery_only",
        },
        {
            "utility": "Commonwealth Edison",
            "metric": "Core delivery proxy",
            "annual_usd": comed["annual_usd"],
            "usd_per_mwh": comed["usd_per_mwh"],
            "comparison_type": "delivery_only",
        },
        {
            "utility": "Dominion Energy Virginia",
            "metric": "GS-5 net collateral",
            "annual_usd": None,
            "usd_per_mwh": None,
            "comparison_type": "contractual_exposure",
            "collateral_usd": dominion["net_collateral_usd"],
        },
    ]
