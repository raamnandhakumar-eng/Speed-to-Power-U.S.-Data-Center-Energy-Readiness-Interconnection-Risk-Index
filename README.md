# Speed-to-Power

## U.S. Data Center Energy Readiness & Interconnection Risk

**Version:** Northern Virginia V3  
**Updated:** September 21, 2026

Speed-to-Power is a reproducible screening framework for evaluating the energy
and grid-readiness of 100–500 MW U.S. data-center loads.

The project now has three analytical layers:

1. **Regional V1:** PJM vs ERCOT vs MISO
2. **Utility V2:** Dominion Energy Virginia vs Oncor Electric Delivery vs Commonwealth Edison
3. **Northern Virginia V3:** transmission projects, load-serving substations, and Dominion large-load queue mechanics

## V3 research question

How do transmission-project maturity, queue rules, site-readiness requirements,
documented load commitments, and infrastructure sequencing shape the plausible
path to power for 100–500 MW data-center loads in Northern Virginia?

## V3 evidence snapshot

Dominion's February 2026 large-load queue filing reports:

- approximately **25 GW** with projected connection dates through 2031
- approximately **45 GW** more assigned to study batches
- approximately **70 GW** total advancing through the queue
- an approximately **100 MW** threshold for the formal large-load process
- a **300 MW cap per delivery-point request**
- four queue stages from Project Initiation through Project Execution

A 2024 transmission filing identifies five load-serving substations totaling
**1,372 MW** of requested ten-year load:

| Substation | Requested load | Filing-era target | Bridging power |
|---|---:|---|---|
| Twin Creeks | 300 MW | June 2026 | Pleasant View, 30 MVA |
| Sycolin Creek | 300 MW | September 2026 | None |
| Starlight | 255 MW | June 2028 | None |
| Lunar | 278 MW | February 2028 | Edwards Ferry, 30 MVA |
| Apollo | 239 MW | March 2028 | Edwards Ferry, 30 MVA |

These values are public filing evidence, not guarantees of current available capacity.

### Transmission Development Readiness Index

V3 adds a documented-maturity index:

- 40% development stage
- 30% regulatory maturity
- 15% schedule specificity
- 15% explicit load linkage

The index does **not** estimate unused substation MW, power-flow capability, or
a guaranteed energization date.

## V2 research question

How do utility market structure, delivery tariffs, large-load contracts,
collateral requirements, demand floors, and interconnection rules change the
commercial path to power for a hyperscale data center?

## Why V2 matters

A regional electricity-price average is not enough for hyperscale siting.

A 300 MW project may face:

- utility-specific delivery tariffs
- 4CP transmission exposure
- long-term take-or-pay style demand floors
- collateral
- transmission construction contributions
- separate retail/wholesale energy procurement
- project-specific interconnection studies

V2 exposes those differences rather than forcing them into one misleading
$/MWh number.

## 300 MW / 90% load-factor base case

Annual energy requirement: **2.3652 TWh**.

### Oncor Electric Delivery / ERCOT

Using the published 2026 transmission-service base charges, August 2026 TCRF,
a 90% 4CP exposure assumption, and the 2026 interim surcharge:

- **Core delivery proxy: about $11.85M/year**
- **About $5.01/MWh**

This is delivery only. Retail energy supply, construction contributions,
special facilities, taxes, and several riders are excluded.

### Commonwealth Edison / PJM

Using the published 2026 High Voltage >10 MW delivery components at a 300 MW
billing demand:

- **Core delivery proxy: about $14.32M/year**
- **About $6.05/MWh**

Published ADJ factors, retail energy supply, PJM capacity, construction, and
other riders are excluded.

### Dominion Energy Virginia / PJM

Dominion's GS-5 structure is not a delivery-only tariff comparison. It is a
large-load contractual framework effective January 1, 2027.

For 300 MW:

- **Gross collateral benchmark: $450M**
- **Collateral after maximum 70% credit reduction: $135M**
- **Minimum distribution demand: 255 MW**
- **Minimum transmission demand: 255 MW**
- **Minimum generation demand: 180 MW**
- **Contract term: 14 years**
- **Ramp period: up to 4 years with at least 20% annual ramp**

These are contractual exposure metrics, not an annual electricity bill.

## Major V2 source findings

Virginia's SCC approved GS-5 for customers with at least 25 MW on a contiguous
site and at least a 75% measured or expected load factor. The Commission also
approved a framework for prospective direct assignment of direct-connect
transmission facilities attributable to new or expanding large loads.

Oncor's transmission-voltage retail-delivery tariff uses demand-based charges
and an ERCOT 4CP-based TCRF. ERCOT's Batch Zero large-load process became
effective in July 2026.

ComEd's published delivery tariff includes explicit Extra Large Load and High
Voltage classes. V2 uses the 2026 High Voltage >10 MW components for the
hyperscale scenario.

## Key files

- `paper/draft_v3.md` — Northern Virginia V3 working paper
- `paper/draft_v2.md` — utility-level V2 working paper
- `analysis/nova_v3_findings.md` — Northern Virginia transmission findings
- `analysis/utility_v2_findings.md` — utility-level V2 findings
- `TECHNICAL_BRIEF.md` — concise technical summary, assumptions, findings, and limitations
- `data/utility_sources_v2.csv`
- `data/nova_sources_v3.csv` — primary-source audit trail
- `src/nova_readiness_v3.py` — Northern Virginia transmission-development model
- `src/utility_model_v2.py` — utility tariff and contractual-exposure model
- `app.py` — interactive V1 + V2 dashboard

## Run the dashboard

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tests/smoke_test.py
python tests/utility_v2_smoke_test.py
python tests/nova_v3_smoke_test.py
streamlit run app.py
```

## Repository structure

```text
.
├── app.py
├── README.md
├── methodology.md
├── research_questions.md
├── analysis/
│   ├── results_v1.md
│   ├── utility_v2_findings.md
│   └── nova_v3_findings.md
├── config/
│   ├── scenario_weights.json
│   ├── scoring_rubric.md
│   └── weights.json
├── data/
│   ├── evidence_v1.csv
│   ├── scenario_scores_v1.csv
│   ├── utility_v2.csv
│   ├── utility_rate_components_v2.csv
│   ├── utility_scenario_outputs_v2.csv
│   ├── utility_sources_v2.csv
│   ├── source_register.csv
│   ├── nova_load_nodes_v3.csv
│   ├── nova_transmission_projects_v3.csv
│   ├── nova_queue_rules_v3.csv
│   └── nova_sources_v3.csv
├── paper/
│   ├── draft_v1.md
│   ├── outline.md
│   ├── v2_utility_layer.md
│   └── draft_v3.md
├── src/
│   ├── evidence_model.py
│   ├── scoring_engine.py
│   ├── scenarios.py
│   ├── utility_model_v2.py
│   └── nova_readiness_v3.py
└── tests/
    ├── smoke_test.py
    ├── utility_v2_smoke_test.py
    └── nova_v3_smoke_test.py
```

## Interpretation rule

This is a **screening and due-diligence model**.

It does not claim that a specific site can receive 100, 300, or 500 MW by a
guaranteed date. A production siting decision still requires utility,
transmission-zone, substation, point-of-interconnection, tariff, construction,
and network-upgrade studies.

## Primary-source trail

See:

- `data/source_register.csv`
- `data/utility_sources_v2.csv`

The project prioritizes primary material from EIA, NERC, FERC, ERCOT, PJM,
Dominion Energy Virginia, the Virginia SCC, Oncor, ComEd, and the Illinois
Commerce Commission.
