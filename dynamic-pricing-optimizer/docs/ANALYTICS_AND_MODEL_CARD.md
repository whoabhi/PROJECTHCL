# Analytics Plan & Model Card

## Model name
Explainable hybrid rules v1 (heuristic decision engine)

## Intended use
Classroom demonstration and decision-support prototyping for retail catalogue pricing. It is not validated for production price-setting.

## Inputs
Current price, cost price, competitor price, demand index (0–100), inventory units, average daily sales, minimum margin percentage and maximum movement percentage.

## Output
Recommended price, percentage movement, gross margin estimate, inventory cover, estimated daily revenue scenario, action label and human-readable explanation.

## Design
- Demand pressure: scaled linear term centred at index 50.
- Inventory pressure: tiered heuristic based on days of stock cover.
- Competitor pressure: proportional gap signal with a cap.
- Combined movement: capped by a user-configured maximum change.
- Hard lower bound: unit cost divided by (1 minus configured gross-margin target).
- Upper bound: capped movement and a maximum premium relative to competitor.

Coefficients are illustrative and not trained from observed sales. A proper ML extension could estimate demand elasticity or demand forecasts from timestamped transaction data, but should be compared against simple baselines and backtested chronologically.

## Key limitation: revenue is not profit
The dashboard's daily revenue scenario multiplies recommended price by the current daily-sales estimate. It holds units constant. It does not predict how quantity will change after a price change and is not a causal uplift estimate. It can overstate the benefit of a price increase. Do not use it as a business case.

## Data required for next iteration
- SKU, timestamp, realised price, list price, units, revenue, returns and stockouts.
- Unit cost and time-varying costs.
- Traffic, product views, add-to-cart, conversion and marketing/promotion indicators.
- Competitor comparable offer price, seller, shipping, availability, promotion and observation timestamp.
- Calendar, holiday and seasonality features.

## Evaluation plan
1. Establish a naïve baseline (hold current price) and simple business-rule baseline.
2. Split data chronologically; never randomly leak future observations into training.
3. Measure demand forecast error (MAE/WAPE) and calibration by category.
4. Backtest gross profit, revenue, stockouts, inventory age and price volatility under explicit constraints.
5. Run a controlled experiment with pre-registered primary metric, guardrails, sample-size/power plan and stop conditions.
6. Monitor drift, data freshness, stockouts, unexpected price jumps and category-level performance.

## Risks and mitigations
- Bad/mismatched competitor observations: source metadata, comparability checks and stale-feed exclusion.
- Price war: cap competitor influence and prevent automatic matching loops.
- Margin erosion: unit-cost floor and finance-approved minimum margin.
- False confidence: show assumptions and label directional estimates.
- Discrimination/unfair pricing: define prohibited features and conduct legal/ethical review for any personalised pricing.
- Feedback loops: do not automatically train from outcomes caused by prior recommendations without causal analysis.

## Governance recommendation
Require human approval for each price change, immutable audit logs, versioned parameters, rollback capability, role-based access and an explicit owner before any production pilot.
