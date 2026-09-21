# Interview Brief

## 30-second version

I built **Speed-to-Power**, a data-center energy screening model for 100–500 MW loads.

V1 compares PJM, ERCOT, and MISO using resource adequacy, demand growth, electricity-price proxies, and large-load process maturity.

V2 moves down to the utility level and compares Dominion Virginia, Oncor Texas, and ComEd Illinois. The main insight is that you cannot compare hyperscale power options using one average $/MWh figure because the commercial structures are different. I separated delivery charges, energy procurement, collateral, minimum demand obligations, and interconnection risk instead.

## 60-second version

The question I wanted to answer was: **where can a 100–500 MW data center secure power fast enough, at acceptable cost and risk?**

I first built a regional model using EIA, NERC, FERC, ERCOT, PJM, MISO, and Berkeley Lab data.

Then I realized the regional result was not enough for a real siting decision, so I built V2 at the utility level.

For a 300 MW / 90% load-factor case:

- Oncor's modeled core transmission-voltage delivery proxy is about **$11.85M/year**, before energy supply and project-specific costs.
- ComEd's modeled high-voltage delivery proxy is about **$14.32M/year**, before ADJ factors, energy supply, PJM capacity, and construction.
- Dominion's GS-5 structure creates a different problem: a 300 MW project has a **$450M gross collateral benchmark**, potentially reduced to **$135M** at the maximum approved credit reduction, plus 85% transmission/distribution and 60% generation minimum-demand floors.

The project helped me treat power availability as a combined engineering, regulatory, and commercial problem rather than a single grid statistic.

## Technical design

The project uses:

- Python
- Pandas
- Streamlit
- scenario modeling
- min-max normalization for V1
- utility-specific tariff formulas for V2
- primary-source evidence registers
- automated smoke tests through GitHub Actions

## Strongest methodological choice

I did **not** force Dominion, Oncor, and ComEd into one "cheapest utility" ranking.

That would be misleading because:

- Dominion's GS-5 framework combines regulated service with long-term contractual obligations.
- Oncor is a transmission and distribution utility in ERCOT's competitive retail market.
- ComEd delivery charges are separate from retail energy supply and PJM capacity exposure.

So I kept unlike cost categories separate.

## Key assumptions to explain

### Oncor

The model assumes transmission-voltage service and uses an adjustable ERCOT 4CP exposure factor.

It includes selected 2026 published delivery components but excludes:

- retail energy supply
- construction contributions
- special facilities
- taxes
- several riders

### ComEd

The model assumes a >10 MW customer served at or above 69 kV.

It includes selected published 2026 High Voltage Delivery Class components but excludes:

- ADJ factors
- retail energy supply
- PJM capacity
- construction
- other riders

### Dominion

The model uses the SCC-approved GS-5 structure effective January 1, 2027.

The collateral figure is **not an annual cost**. It is contractual/security exposure.

## Questions I would ask next on a real project

1. What is the exact point of interconnection?
2. What substation and transmission upgrades are required?
3. Who pays for direct-connect facilities?
4. What is the realistic partial-energization date?
5. What service voltage will the customer take?
6. What is the applicable utility tariff and rider stack?
7. What capacity-market exposure applies?
8. Can the load curtail or shift during system peaks?
9. What credit support is required before construction?
10. What changes if the facility ramps from 50 MW to 300 MW over four years?

## What V3 should add

V3 should move from utility territory to candidate transmission zones and substations.

That means adding:

- substations / POIs
- transmission constraints
- planned upgrades
- network-upgrade responsibility
- energization ranges
- capacity prices
- wholesale energy basis
- renewable procurement
- land / water / permitting
- onsite generation options
