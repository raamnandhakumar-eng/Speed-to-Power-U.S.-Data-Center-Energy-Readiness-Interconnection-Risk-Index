# Utility-Level V2 Findings

**As of September 21, 2026**

## Why V2 changes the model

The V1 RTO comparison was useful for regional screening, but a hyperscale site decision is made through utilities, tariffs, transmission zones, substations, contracts, and interconnection studies.

V2 therefore compares three service territories:

- Dominion Energy Virginia in PJM
- Oncor Electric Delivery in ERCOT
- Commonwealth Edison in PJM

The three utilities do not sell electricity under the same market structure. V2 keeps unlike cost categories separate.

## 300 MW / 90% load-factor base case

Annual energy requirement: **2.3652 TWh**.

### Oncor Electric Delivery

For a transmission-voltage customer, the V2 core delivery proxy includes the published customer charge, metering charge, distribution-system charge, August 2026 TCRF, and the temporary 2026 interim surcharge.

With a 90% 4CP exposure factor:

- Core delivery proxy: **about $11.85 million/year**
- Core delivery proxy: **about $5.01/MWh**

This is **delivery only**. It does not include the retail electricity supplier, generation energy, construction contributions, special facilities, taxes, or all riders.

The model makes 4CP exposure adjustable because Oncor's TCRF is billed using ERCOT coincident-peak demand rather than simply annual energy use.

### Commonwealth Edison

For a hypothetical >10 MW load served at high voltage, the V2 proxy uses the published 2026 High Voltage Delivery Class components:

- customer charge
- metering charge
- HV distribution facilities charge
- HV transformer charge
- Illinois Electricity Distribution Tax

At 300 MW and a 90% load factor:

- Core delivery proxy: **about $14.32 million/year**
- Core delivery proxy: **about $6.05/MWh**

Published **ADJ** factors, retail energy supply, PJM capacity, construction, interconnection, taxes beyond the listed IEDT, and other riders are excluded.

### Dominion Energy Virginia

Dominion cannot be put into the same delivery-only comparison because its GS-5 structure is a regulated large-load class with substantial contractual commitments.

For a 300 MW contracted load beginning under GS-5:

- Gross collateral benchmark: **$450 million**
- If the customer receives the maximum 70% credit-based reduction: **$135 million**
- Minimum distribution billed-demand floor: **255 MW**
- Minimum transmission billed-demand floor: **255 MW**
- Minimum generation billed-demand floor: **180 MW**
- Contract term: **14 years**
- Ramp period: up to **4 years**, with at least **20% annual ramp**

These are contractual exposure metrics, not an annual electricity bill.

## A major 2026 Virginia development

The Virginia SCC has also approved a framework for prospective direct assignment of the costs of direct-connect transmission facilities that would not be built but for a new or expanding large-load customer. The detailed line-extension policy is being developed in a supplemental proceeding.

This materially increases the importance of distinguishing:

1. normal tariff charges,
2. collateral and minimum demand obligations, and
3. project-specific transmission infrastructure contributions.

## Decision-useful interpretation

V2 does **not** declare a universal utility winner.

Instead, it exposes different tradeoffs:

- **Oncor / ERCOT:** competitive energy procurement and an implemented large-load study framework, with material exposure to 4CP-based transmission charges and project-specific construction.
- **ComEd / PJM:** explicit high-voltage delivery rates that can be modeled transparently, but energy supply and PJM capacity remain separate from the utility delivery proxy.
- **Dominion / Virginia:** unusually explicit large-load contractual protections and a dedicated GS-5 class, but with high commitment/collateral exposure and evolving direct-connect cost assignment and flexibility rules.

## Next technical layer

V3 should move from utility territory to candidate transmission zones / substations and add:

- interconnection-study milestone timelines
- utility construction contributions
- network-upgrade cost responsibility
- PJM/ ERCOT locational wholesale-price history
- capacity price exposure
- specific renewable procurement options
- substation and transmission constraint proxies
- land, water, permitting, and gas-pipeline proximity
