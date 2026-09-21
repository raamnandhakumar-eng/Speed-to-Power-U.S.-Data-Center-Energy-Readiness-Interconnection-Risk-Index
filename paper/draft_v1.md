# Speed to Power: A Multi-Criteria Framework for Screening U.S. Data Center Energy Readiness

## Working paper draft v1
**Date:** September 21, 2026

## Abstract

Rapid growth in data-center and other large-load electricity demand is forcing U.S. grid operators to redesign how they forecast, study, connect, and serve very large customers. This paper develops a transparent screening framework for comparing power-market readiness for a hypothetical 300 MW data center. The first version compares PJM, ERCOT, and MISO using observed public data on electricity prices, demand growth, planning reserve margins, and probabilistic loss-of-load hours, combined with documented-status indicators for large-load process maturity and flexible-service maturity.

The framework is designed as a decision-support tool rather than a prediction of guaranteed energization dates. The results show why low electricity price, system resource adequacy, and regulatory readiness must be evaluated together. They also demonstrate that public regional data are useful for first-stage screening but insufficient for a final site decision, which requires utility-specific tariffs, transmission deliverability, substation capacity, interconnection studies, and project-specific commercial terms.

## 1. Introduction

Data centers are changing the scale and speed of U.S. electric-load growth. In June 2026, the Federal Energy Regulatory Commission issued tailored show-cause orders to the six regional grid operators under its jurisdiction, requiring them to justify or reform rules for connecting data centers, manufacturing facilities, and other large loads.

Lawrence Berkeley National Laboratory organizes the large-load problem into five functional areas: load forecasting, interconnection, resource planning and procurement, markets and operations, and cost allocation and ratemaking. This paper converts that institutional problem into a reproducible market-screening model.

The core research question is:

> How do cost, resource adequacy, demand growth, large-load process maturity, and flexible-service options change the relative attractiveness of U.S. power markets for a 100–500 MW data-center load?

The paper intentionally does not claim that an RTO-wide score can identify a buildable site. Instead, it asks whether publicly available regional evidence can improve the first stage of site screening and reveal where deeper utility- and transmission-level due diligence is most important.

## 2. Markets

Version 1 compares three major power-market footprints:

- **PJM**, with Virginia used only as a state-level industrial-price proxy.
- **ERCOT**, with Texas serving as both the power-market footprint and price proxy.
- **MISO**, with Illinois used only as a state-level industrial-price proxy.

These are not equivalent geographies. PJM and MISO are multi-state systems, while ERCOT lies almost entirely within Texas. The price comparison therefore must be treated as a screening proxy rather than a tariff comparison.

## 3. Data

### 3.1 Electricity price

EIA's June 2026 industrial retail-price data report:

- Virginia: **9.31 cents/kWh**
- Texas: **6.58 cents/kWh**
- Illinois: **10.65 cents/kWh**

At a 300 MW load and 90% load factor, the implied annual energy requirement is **2.365 TWh**. Applying the state industrial-price proxy produces rough annual electricity-cost screens of:

- PJM / Virginia proxy: **$220.2 million**
- ERCOT / Texas proxy: **$155.6 million**
- MISO / Illinois proxy: **$251.9 million**

These figures are not project tariffs. They exclude demand charges, transmission charges, riders, negotiated large-load rates, taxes, hedging, backup generation, and other commercial terms.

### 3.2 Demand growth

NERC's 2025 Long-Term Reliability Assessment reports total internal demand from 2026 through 2035. Using those values, the project calculates a common summer-peak-demand CAGR measure:

- PJM: 3.14%
- ERCOT: 5.56%
- MISO: 1.38%

Growth is treated as a pressure indicator, not as a negative judgment about economic development. Rapid growth can support new infrastructure investment while simultaneously increasing near-term competition for generation and transmission capacity.

### 3.3 Resource adequacy

For 2029, NERC reports the following anticipated reserve margins and probabilistic loss-of-load hours:

| Market | Anticipated reserve margin | Reference margin | LOLH |
|---|---:|---:|---:|
| PJM | 18.9% | 23.9% | 9.97 |
| ERCOT | 30.8% | 13.75% | 3.64 |
| MISO | 8.6% | 8.5% | 6.61 |

NERC classifies all three areas as high risk by 2029 under the assumptions in the 2025 LTRA, though the severity and drivers differ.

PJM faces rapid load growth and tightening capacity. MISO faces demand growth and uncertainty around resource commercialization and retirements. ERCOT has substantial load growth but also incorporates large-load curtailment and demand-response assumptions that materially affect its planning-reserve-margin calculation.

### 3.4 Large-load process status

**ERCOT.** Batch Zero became effective July 11, 2026 as a transitional interconnection study process for eligible large loads. ERCOT's public materials state that load facilities of 75 MW or greater should consult PGRR145 for eligibility.

**PJM.** PJM filed a new framework in August 2026 that includes Interim Resource Adequacy Service and a proposed Large Load Registry. The framework was still pending regulatory resolution as of the date of this draft.

**MISO.** MISO is actively developing a Large Load Project Review process and flexible/non-firm transmission-service options. Stakeholder materials describe a proposed quarterly LLPR cycle with 90 days of study work plus 30 days for agreements and final approval.

## 4. Model

Version 1 uses five decision dimensions:

1. Resource adequacy
2. Electricity-cost proxy
3. Demand-growth pressure
4. Large-load process maturity
5. Flexible-service maturity

Quantitative variables are min-max normalized within the three-market comparison set.

The resource-adequacy score is the equal-weight average of:

- normalized 2029 anticipated reserve margin, and
- inverse-normalized 2029 LOLH.

The default balanced weights are:

| Dimension | Weight |
|---|---:|
| Resource adequacy | 35% |
| Cost proxy | 20% |
| Growth pressure | 15% |
| Large-load process maturity | 15% |
| Flexibility maturity | 15% |

The model also provides speed-first, cost-first, and reliability-first weight sets.

## 5. Preliminary Results

Under the default balanced weights, the Version 1 screening scores are:

| Market | Score |
|---|---:|
| ERCOT | 85.0 |
| PJM | 41.4 |
| MISO | 37.8 |

These numbers should not be interpreted as a final market ranking. They are highly sensitive to the limited MVP variable set and to ERCOT's documented large-load curtailment framework, which improves both its process-maturity indicators and NERC reserve-margin treatment.

The useful result is not the ordering itself. The useful result is the decomposition:

- ERCOT currently combines the lowest state industrial-price proxy in the three-market set with a formally implemented transitional large-load process.
- PJM's price proxy is intermediate, but NERC's 2029 probabilistic adequacy results are materially tighter under the assessment assumptions.
- MISO has slower projected demand growth in the NERC dataset but is still developing several large-load-specific service and study mechanisms.

## 6. Phased Energization

A hyperscale project may not require its full contracted load on day one. Version 1 therefore includes a phased 300 MW profile:

- Year 1: 50 MW
- Year 2: 125 MW
- Year 3: 225 MW
- Year 4: 300 MW

Future versions will test whether flexible or staged service can reduce required network upgrades or accelerate partial energization. This cannot be inferred from regional public data alone. It requires transmission-node and utility-level study assumptions.

## 7. Sensitivity Analysis

The model includes four default decision profiles:

- Balanced
- Speed-first
- Cost-first
- Reliability-first

This is important because no universal weighting scheme exists. A cloud provider prioritizing deployment speed may rationally accept higher curtailment exposure. A mission-critical facility may instead place more weight on firmness and resource adequacy. A cost-sensitive flexible compute load may value low energy price and interruptible service more heavily.

The dashboard exposes these assumptions rather than hiding them.

## 8. Limitations

The first version has five major limitations.

First, industrial retail prices are state averages and not utility-specific large-load tariffs.

Second, regional reserve margins do not measure transmission deliverability to a specific site.

Third, large-load regulatory processes are changing quickly, particularly in PJM and MISO.

Fourth, min-max scoring is relative to the markets included in the sample. Adding additional regions will change normalized scores.

Fifth, a region can have adequate generation but still face local transmission, substation, permitting, equipment, or construction constraints.

## 9. Next Research Stage

The next stage should move from regional screening to **utility- and transmission-zone screening**.

Priority additions:

1. Utility-specific large-load tariffs
2. Transmission zone / substation constraints
3. Network-upgrade responsibility
4. Firm versus non-firm service
5. Curtailment rules
6. Interconnection study deposits and milestones
7. Generation and storage pipeline near candidate load centers
8. Carbon-free procurement options
9. Water and land constraints
10. Site-specific permitting

## 10. Conclusion

Speed-to-power is not a single variable. It is the outcome of resource adequacy, transmission capability, utility process, regulatory design, customer flexibility, generation availability, and commercial risk.

A transparent screening model can make the first stage of data-center energy due diligence faster and more consistent, but it should direct deeper study rather than replace it.

Version 1 establishes that framework and provides a reproducible base for utility-level expansion.

## Primary Sources

See `data/source_register.csv`.
