# Methodology

## 1. Unit of analysis

The MVP compares regional power-market footprints using a representative state for state-level retail-price data. This is a first-stage screening tool, not a parcel-level siting model.

Future versions should move from market-level to:
- utility service territory
- transmission zone
- substation / POI
- specific candidate site

## 2. Data classes

### Observed
Measured or reported data such as:
- industrial electricity price
- peak demand
- generation capacity
- queue capacity
- reserve / adequacy indicators

### Process
Documented interconnection and tariff rules:
- large-load threshold
- study cadence
- deposit/readiness requirements
- firm vs non-firm options
- co-location options
- curtailment / flexibility provisions

### Modeled
Derived indicators:
- normalized cost score
- process clarity score
- readiness score
- scenario-adjusted score

## 3. Score construction

Each quantitative metric is normalized to 0–100.

For a metric where higher is better:

score = 100 * (x - min) / (max - min)

For a metric where lower is better:

score = 100 * (max - x) / (max - min)

Composite:

Readiness = sum(weight_i * score_i)

## 4. Guardrails

- Never convert an uncertain or proposed rule into a factual energization timeline.
- Keep proposed, approved, and effective rules separate.
- Preserve raw source values alongside transformed scores.
- Report sensitivity to weights.
- Flag missing variables instead of silently imputing them.
- Distinguish state-level retail prices from negotiated hyperscale tariffs.
- Do not interpret queue capacity as capacity available to serve a new load.

## 5. Planned sensitivity tests

1. Speed-first hyperscaler
2. Cost-first operator
3. Carbon-constrained operator
4. High-reliability critical load
5. Flexible / interruptible load
6. Phased energization versus full 300 MW Day 1

## 6. Planned outputs

- market comparison table
- radar / profile chart
- scenario ranking
- sensitivity chart
- regulatory status timeline
- primary bottleneck by market
- mitigation option by bottleneck
