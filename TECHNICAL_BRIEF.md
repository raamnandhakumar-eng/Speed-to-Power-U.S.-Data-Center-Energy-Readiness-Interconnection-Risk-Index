# Technical Brief

## Project objective

Speed-to-Power evaluates the energy and grid-readiness of 100–500 MW U.S. data-center loads.

The framework has two analytical layers:

1. **Regional screening:** PJM, ERCOT, and MISO
2. **Utility-level due diligence:** Dominion Energy Virginia, Oncor Electric Delivery, and Commonwealth Edison

The objective is to identify the technical, regulatory, and commercial variables that shape the path to power for large loads.

## Core research question

How do resource adequacy, transmission conditions, utility market structure, delivery tariffs, large-load contracts, collateral requirements, demand floors, flexibility provisions, and interconnection rules affect the feasibility of serving a hyperscale data-center load?

## 300 MW base case

Assumptions:

- Facility load: 300 MW
- Load factor: 90%
- Annual energy: 2.3652 TWh

### Oncor Electric Delivery

The V2 model estimates a core transmission-voltage delivery proxy of approximately:

- **$11.85 million/year**
- **$5.01/MWh**

The calculation uses selected 2026 delivery components and a 90% ERCOT 4CP exposure assumption.

Excluded:

- retail energy supply
- project-specific construction
- special facilities
- taxes
- several riders

### Commonwealth Edison

The V2 model estimates a core high-voltage delivery proxy of approximately:

- **$14.32 million/year**
- **$6.05/MWh**

The calculation uses selected published 2026 High Voltage >10 MW delivery components.

Excluded:

- published ADJ factors
- retail energy supply
- PJM capacity
- construction
- additional riders

### Dominion Energy Virginia

The GS-5 framework produces contractual obligations rather than a directly comparable delivery-only cost.

For 300 MW:

- Gross collateral benchmark: **$450 million**
- Collateral after maximum 70% credit reduction: **$135 million**
- Minimum distribution demand: **255 MW**
- Minimum transmission demand: **255 MW**
- Minimum generation demand: **180 MW**
- Contract term: **14 years**
- Ramp period: up to **4 years**
- Minimum annual ramp: **20%**

The collateral amount is a contractual-security requirement, not an annual electricity cost.

## Methodological principle

The project does not force Dominion, Oncor, and ComEd into a single cost ranking.

The service structures are materially different:

- Dominion uses a regulated large-load framework with long-term contractual obligations.
- Oncor provides regulated transmission and distribution delivery in ERCOT's competitive retail market.
- ComEd provides delivery service while electricity supply and PJM capacity exposure remain separate.

The model therefore keeps delivery charges, energy procurement, collateral, minimum demand commitments, and project-specific infrastructure costs as distinct categories.

## Key assumptions

### Oncor

- Transmission-voltage service
- Adjustable ERCOT 4CP exposure
- Selected published 2026 delivery components

### ComEd

- Customer demand above 10 MW
- Service at or above 69 kV
- Selected published 2026 High Voltage Delivery Class components

### Dominion

- GS-5 applicability
- Effective January 1, 2027
- Approved collateral and minimum-demand structure

## Limitations

The current model does not yet include:

- site-specific transmission capacity
- substation headroom
- transformer availability
- network-upgrade costs
- utility construction contributions
- complete retail energy procurement costs
- full capacity-market exposure
- all tariff riders and adjustment factors
- permitting timelines
- water availability
- land cost
- tax incentives
- onsite generation economics

## Next research stage

The next version should move from utility service territory to candidate transmission zones, substations, and points of interconnection.

Priority additions:

1. substation and POI data
2. transmission constraints
3. planned network upgrades
4. network-upgrade cost responsibility
5. study milestones
6. service-voltage assumptions
7. capacity prices
8. wholesale energy basis
9. renewable procurement pathways
10. land, water, and permitting constraints
11. onsite generation options
12. partial and phased energization scenarios

## Source trail

Primary sources are maintained in:

- `data/source_register.csv`
- `data/utility_sources_v2.csv`
