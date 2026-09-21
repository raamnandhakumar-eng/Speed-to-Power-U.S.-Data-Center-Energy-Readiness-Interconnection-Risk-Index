# Speed to Power: From Regional Grid Readiness to Utility-Level Commercial Feasibility for Hyperscale Data Centers

## Working Paper Draft V2

**September 21, 2026**

## Abstract

Data-center load growth is changing the scale, timing, and commercial structure of electricity demand in the United States. Regional transmission organizations, utilities, and regulators are developing new procedures for large loads, but public discussions often collapse several distinct questions into a single concept of "power availability." This paper develops a two-layer screening framework for 100–500 MW data-center loads. The first layer evaluates regional power-market conditions across PJM, ERCOT, and MISO using public evidence on industrial electricity prices, demand growth, planning reserve margins, probabilistic loss-of-load hours, and large-load process maturity. The second layer moves to the utility/service-territory level and examines Dominion Energy Virginia, Oncor Electric Delivery, and Commonwealth Edison.

The utility-level analysis shows why regional averages alone are insufficient. A 300 MW data center in Dominion's Virginia territory faces a new GS-5 large-load framework that includes a 14-year contract, minimum demand obligations, and a collateral benchmark of $1.5 million per MW. A similarly sized project in Oncor's Texas territory participates in a competitive retail market in which energy procurement is separate from regulated delivery service and transmission charges depend materially on ERCOT four-coincident-peak exposure. In ComEd's Illinois territory, high-voltage delivery charges can be modeled from published tariff components, but energy supply, PJM capacity, tariff adjustments, and project-specific interconnection costs remain separate.

The principal finding is methodological: "speed to power" is not a single grid statistic or tariff rate. It is a joint outcome of system adequacy, transmission deliverability, utility process, service voltage, commercial commitments, cost allocation, customer flexibility, and project-specific infrastructure. A defensible screening tool should therefore decompose these drivers and preserve uncertainty rather than produce a false-precision national ranking.

## 1. Introduction

Artificial-intelligence computing, cloud infrastructure, advanced manufacturing, electrification, and other large-load sectors are creating electricity requests that can reach hundreds of megawatts at a single site. The challenge for a developer is no longer simply identifying a region with low electricity prices. A project must also determine whether sufficient generation and transmission can be made available, whether the utility or grid operator has a defined large-load study process, which infrastructure costs are assigned to the customer, how long the customer must contract for service, whether the load can ramp or curtail, and how much commercial security must be posted before infrastructure is built.

In June 2026, the Federal Energy Regulatory Commission opened region-specific proceedings focused on the rules governing the connection of large loads. Berkeley Lab's *Speed to Power* work similarly frames large-load integration across forecasting, interconnection, procurement, operations, and ratemaking. These developments indicate that large-load integration is both an engineering problem and a commercial/regulatory design problem.

This paper asks:

> How should a data-center developer screen U.S. power markets and utility territories for a 100–500 MW load when the relevant constraints span resource adequacy, transmission, tariffs, contracts, and interconnection rules?

The project answers this question with a two-layer model.

**Layer 1: Regional screening.** PJM, ERCOT, and MISO are compared using common public indicators.

**Layer 2: Utility due diligence.** Dominion Energy Virginia, Oncor Electric Delivery, and Commonwealth Edison are examined using utility-specific tariff and regulatory evidence.

The objective is not to predict a guaranteed energization date. The objective is to identify the commercial and technical variables that should determine where deeper site-level diligence is performed.

## 2. Why "Power Availability" Is Not One Variable

A statement that a region has "available power" can refer to several different concepts:

1. Installed generation capacity
2. Planning reserve margin
3. Transmission deliverability
4. Substation capacity
5. Distribution capacity
6. Energy-market liquidity
7. Capacity-market exposure
8. Utility willingness to contract
9. Interconnection-study position
10. Construction lead time

These variables can move in opposite directions.

A region may have abundant generation but constrained transmission. A utility may have a clear tariff but require large collateral. A competitive electricity market may offer procurement flexibility while exposing the customer to peak-based transmission charges. A regulated utility may offer vertically integrated service while imposing long-duration demand commitments to protect other customers from stranded infrastructure costs.

A credible speed-to-power framework must therefore preserve these distinctions.

## 3. Regional Screening Layer

### 3.1 Sample

The V1 model compares:

- PJM
- ERCOT
- MISO

Virginia, Texas, and Illinois are used as representative states only for the state-level industrial electricity-price proxy. The geographic mismatch is explicitly recognized: PJM and MISO span multiple states and utility territories, while ERCOT is almost entirely contained in Texas.

### 3.2 Variables

The regional layer uses:

- industrial retail electricity-price proxy
- 2026–2035 total internal demand growth
- 2029 anticipated reserve margin
- 2029 reference margin
- probabilistic loss-of-load hours
- large-load process maturity
- flexible-service maturity

Quantitative metrics are min-max normalized within the three-market sample. The process variables are documented-status indicators rather than measures of physical grid capacity.

### 3.3 V1 result

Under the project's default balanced weighting, ERCOT receives the highest screening score of the three markets. The result is driven by its lower Texas industrial-price proxy, stronger modeled 2029 adequacy values in the NERC dataset, and a formally implemented transitional large-load process.

This result should not be read as a recommendation to site in ERCOT. It is a screening signal that identifies why a developer might perform deeper diligence there.

The limitations become clear once the model moves to utilities.

## 4. Utility-Level V2

### 4.1 Case-selection logic

V2 selects one utility/service territory from each relevant context:

- **Dominion Energy Virginia:** vertically integrated regulated service in the country's largest data-center market.
- **Oncor Electric Delivery:** transmission and distribution service in ERCOT's competitive retail market.
- **Commonwealth Edison:** high-voltage delivery service in northern Illinois within PJM.

The three territories intentionally represent different commercial architectures.

### 4.2 The key modeling rule

V2 does **not** place all three utilities into one electricity-price ranking.

For Oncor and ComEd, the model calculates a transparent **core delivery-charge proxy** from published tariff components.

For Dominion, the model calculates **GS-5 contractual exposure**, including collateral and minimum demand obligations.

Energy supply remains separate where the market structure requires it.

This prevents a common analytical mistake: comparing a bundled regulated bill with a delivery-only tariff as though they represented the same product.

## 5. Dominion Energy Virginia

### 5.1 GS-5 eligibility

The Virginia State Corporation Commission approved a new GS-5 rate class effective January 1, 2027.

The class applies to customers with:

- measured or contracted demand of at least 25 MW on a contiguous site; and
- measured or expected load factor of at least 75%.

A 100 MW, 300 MW, or 500 MW hyperscale data center at a high load factor therefore falls well within the intended scope.

### 5.2 Contract term and ramp

The approved framework includes:

- a 14-year contract term;
- an optional load-ramp period of up to four years; and
- a minimum annual ramp of 20%.

If the customer ceases operations or defaults during the contract term, the framework includes exit-fee exposure for remaining minimum obligations, subject to approved capacity-reassignment provisions.

This turns load forecasting into a commercial commitment problem. Overstating future load can create long-duration financial exposure.

### 5.3 Collateral

The SCC approved collateral terms based on:

[
Collateral_{gross} = 1.5	ext{ million dollars} 	imes Contracted MW
]

The requirement may be reduced by up to 70% based on established credit.

For a 300 MW project:

[
Collateral_{gross} = 300 	imes $1.5M = $450M
]

At the maximum 70% reduction:

[
Collateral_{net} = $450M 	imes 30% = $135M
]

This is not an annual operating cost. It is a balance-sheet and credit requirement.

### 5.4 Minimum demand obligations

The approved GS-5 framework establishes minimum billed-demand floors of:

- 85% of contracted distribution demand
- 85% of contracted transmission demand
- 60% of contracted generation demand

For 300 MW:

- distribution floor = 255 MW
- transmission floor = 255 MW
- generation floor = 180 MW

The Commission excluded PJM capacity expense from the minimum generation demand charge.

### 5.5 Direct-connect transmission cost assignment

In 2026, the Virginia SCC approved a framework requiring prospective direct assignment of direct-connect transmission facilities that would not be built but for the needs of a new or expanding large-load customer.

This means the eventual economics of a Virginia site may depend heavily on whether a project triggers dedicated transmission facilities.

The lesson is important: tariff rates alone cannot determine site economics.

## 6. Oncor Electric Delivery

### 6.1 Market structure

Oncor is a transmission and distribution utility in ERCOT's competitive retail market.

The delivery utility does not supply the project's retail electricity commodity. A large customer procures energy through a competitive retail electric provider or other eligible market arrangement.

V2 therefore models only selected Oncor delivery components.

### 6.2 Transmission-service tariff

For transmission-voltage service, the June 2026 tariff lists:

- customer charge: $258.80/month
- metering charge: $321.63/month
- distribution-system charge: $0.331004 per billing kW-month

The Transmission Cost Recovery Factor effective August 1, 2026 is:

- $3.491759 per 4CP kW-month for Transmission Service.

The tariff also includes a temporary 2026 interim surcharge of:

- -$0.182495 per distribution-system billing kW for Transmission Service.

The V2 proxy excludes other riders, construction contributions, special facilities, taxes, and the retail energy contract.

### 6.3 Why 4CP matters

ERCOT transmission charges depend on four-coincident-peak demand.

V2 therefore defines:

[
4CP kW = Maximum Load kW 	imes 4CP Exposure Factor
]

The default factor is 0.90 but the dashboard allows the user to change it.

For a 300 MW facility at the default assumption, the V2 core-delivery proxy is approximately:

- $11.85 million/year
- $5.01/MWh of annual facility energy

This is not the project's total electricity cost.

The model's real insight is sensitivity: peak-management strategy can change transmission-cost exposure without changing annual energy consumption.

## 7. Commonwealth Edison

### 7.1 Delivery classification

ComEd's tariff defines separate nonresidential delivery classes.

For a hyperscale facility, V2 assumes service in the High Voltage Delivery Class with maximum demand above 10 MW and conductors entering the premises at or above 69 kV.

This assumption must be replaced with the actual service-voltage design in a project-specific study.

### 7.2 2026 modeled components

The V2 core proxy uses the published 2026 amounts:

- customer charge: $719.73/month
- standard metering service charge: $32.00/month
- HV distribution facilities charge for >10 MW: $0.51/kW-month
- HV transformer charge for >10 MW: $2.65/kW-month
- Illinois Electricity Distribution Tax: $0.00124/kWh

Many published tariff values are stated as the listed amount plus an adjustment factor. V2 deliberately excludes those ADJ amounts until a complete adjustment model is added.

Retail energy supply, PJM capacity, construction, and project-specific interconnection charges are also excluded.

For a 300 MW facility at a 90% load factor and a billing-demand factor of 1.00, the core delivery proxy is approximately:

- $14.32 million/year
- $6.05/MWh

Again, this is not a total electricity bill.

## 8. 100 MW, 300 MW, and 500 MW Scenarios

With a 90% load factor, V2 calculates the following baseline outputs.

| Full Load | Oncor Core Delivery Proxy | ComEd Core Delivery Proxy | Dominion Gross GS-5 Collateral | Dominion Collateral After Max 70% Credit Reduction |
|---:|---:|---:|---:|---:|
| 100 MW | $3.96M/yr | $4.78M/yr | $150M | $45M |
| 300 MW | $11.85M/yr | $14.32M/yr | $450M | $135M |
| 500 MW | $19.75M/yr | $23.86M/yr | $750M | $225M |

The first two columns are delivery-charge proxies. The final two columns are collateral requirements. They should not be compared as equivalent cost measures.

The table demonstrates why decomposed outputs are preferable to a single blended index.

## 9. Phased Energization

The project retains the V1 phased-load concept.

A 300 MW facility can be represented as:

- Year 1: 50 MW
- Year 2: 125 MW
- Year 3: 225 MW
- Year 4: 300 MW

This is particularly relevant to Dominion because the GS-5 framework explicitly permits a ramp period of up to four years.

Future versions should test whether phased energization changes:

- required network upgrades
- collateral timing
- capacity procurement
- transmission demand floors
- construction sequencing
- time to partial service

Those effects cannot be inferred from tariff data alone.

## 10. Implications for Data-Center Energy Strategy

### 10.1 Procurement structure matters

A low wholesale-energy environment does not automatically imply a low all-in power cost.

In Oncor territory, a developer must combine delivery economics with a competitive energy contract and manage 4CP exposure.

In ComEd territory, delivery economics must be combined with retail supply and PJM capacity/transmission exposures.

In Dominion territory, a developer must evaluate bundled/regulatory economics together with long-duration GS-5 commitments.

### 10.2 Credit capacity becomes a siting variable

The Dominion GS-5 collateral framework makes corporate credit quality directly relevant to the commercial feasibility of large-load siting.

For a 500 MW project, the gross benchmark reaches $750 million before credit reduction.

The availability and cost of letters of credit, parent guarantees, cash collateral, and other security therefore belong in a speed-to-power model.

### 10.3 Customer flexibility has economic value

Flexible computing workloads may be able to reduce peak exposure, accept interruptible arrangements, or support staged energization.

The value of flexibility differs by market.

ERCOT provides a particularly clear example because coincident-peak exposure affects transmission costs and large-load curtailment has become part of the system's planning framework.

Dominion is developing a large-load demand-flexibility program pursuant to 2026 Virginia legislation.

## 11. Limitations

V2 remains a screening model.

It does not yet include:

- actual retail energy contract prices
- PJM capacity prices by load obligation
- full Oncor rider stack
- ComEd ADJ factors
- utility construction contributions
- site-specific transmission studies
- substation headroom
- transformer lead times
- line-routing and permitting
- water availability
- land cost
- tax incentives
- gas-pipeline access for onsite generation
- carbon-free energy matching

The Oncor and ComEd proxies should therefore be treated as transparent lower-level tariff models, not forecast total bills.

The Dominion collateral calculation is a contractual-security model, not an expense forecast.

## 12. Next Research Stage

The next version should move from utility territory to **candidate transmission zones and substations**.

A production framework should contain:

1. candidate site coordinates
2. serving utility
3. service voltage
4. nearest transmission substations
5. thermal/transmission constraint proxy
6. planned network upgrades
7. utility construction scope
8. interconnection milestones
9. network-upgrade cost responsibility
10. wholesale energy basis
11. capacity cost
12. renewable procurement pathway
13. backup-generation assumptions
14. water and permitting constraints
15. energization confidence range

The result would be a true site-screening engine rather than a market-screening model.

## 13. Conclusion

The path to power for a hyperscale data center is both an electrical-engineering problem and a commercial-structure problem.

Regional resource adequacy can identify where deeper diligence is warranted, but the utility layer determines how a project will actually contract, pay, and progress toward service.

The comparison of Dominion, Oncor, and ComEd shows three different architectures:

- long-term regulated large-load commitments;
- competitive energy procurement with regulated transmission and distribution delivery; and
- high-voltage delivery with separate supply and capacity exposure.

The practical implication is straightforward: the question is not simply "Where is electricity cheapest?"

The better question is:

> Where can the project secure a technically deliverable, commercially acceptable, and sufficiently flexible path to its required megawatts on the required schedule?

Speed-to-Power V2 provides a reproducible framework for beginning that analysis.

## References and Source Register

Machine-readable source details and URLs are maintained in:

- `data/source_register.csv`
- `data/utility_sources_v2.csv`

Primary sources include the U.S. Energy Information Administration, North American Electric Reliability Corporation, Federal Energy Regulatory Commission, ERCOT, PJM, Virginia State Corporation Commission, Dominion Energy Virginia, Oncor Electric Delivery, Commonwealth Edison, and the Illinois Commerce Commission.
