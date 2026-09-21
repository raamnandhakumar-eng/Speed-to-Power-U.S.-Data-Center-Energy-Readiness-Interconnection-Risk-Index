# Evidence Scoring Rubric

This project distinguishes **raw evidence** from **model judgment**.

## Quantitative metrics

The following are sourced directly, then normalized across the three-market MVP:

- Industrial electricity-price proxy, lower is better
- 2029 anticipated planning reserve margin, higher is better
- 2029 loss-of-load hours (LOLH), lower is better
- 2026–2035 summer-peak demand CAGR, lower growth pressure is better

The `resource_adequacy_score` is the average of:

1. normalized anticipated reserve margin, and
2. inverse-normalized LOLH.

These scores are **comparative within the MVP set**, not absolute grades of grid reliability.

## Large-load process maturity

This is a documented-status indicator, not a physical grid-capacity metric.

- **100**: dedicated large-load process is implemented/effective, with published eligibility and implementation materials
- **75**: tariff/process filed with regulator and materially specified, but not fully effective
- **50**: formal operator proposal is under stakeholder/regulatory development
- **25**: concept is publicly under study but no defined process exists
- **0**: no dedicated process identified

Version 1 values:
- ERCOT: 100
- PJM: 60
- MISO: 50

PJM receives 60 rather than 75 because its August 2026 IRAS filing is substantial, but it is primarily a resource-adequacy framework rather than a complete, settled large-load interconnection pathway.

## Flexibility maturity

- **100**: effective curtailment/flexible-load authority or operating framework is documented
- **75**: regulatory filing contains a defined flexible/curtailment framework
- **50**: detailed operator proposal is under development
- **25**: early concept
- **0**: no identified pathway

Version 1 values:
- ERCOT: 100
- PJM: 60
- MISO: 40

## Default balanced score

- Resource adequacy: 35%
- Cost proxy: 20%
- Growth pressure: 15%
- Large-load process maturity: 15%
- Flexibility maturity: 15%

The dashboard exposes the weights. A user should not treat the default score as a universal ranking.

## Critical limitations

- State industrial retail prices are not hyperscale tariffs.
- RTO/ISO-level resource adequacy does not establish capacity at a specific substation or point of interconnection.
- A high reserve margin does not guarantee transmission deliverability.
- Large-load rules are changing rapidly.
- MISO and PJM proposals may change before becoming effective.
- ERCOT's reserve-margin treatment reflects large-load curtailment assumptions; it should not be compared without reading the NERC methodology.
