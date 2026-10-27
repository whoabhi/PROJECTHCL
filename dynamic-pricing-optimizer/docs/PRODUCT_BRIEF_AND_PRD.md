# Product Brief & PRD: PricePilot

## 1. Executive summary

PricePilot is a decision-support tool for retail pricing analysts who need to evaluate price changes across a catalogue without relying on intuition alone. It brings together current price, unit cost, competitor price, a demand signal and inventory cover, then proposes a bounded price with an explanation and guardrails.

## 2. Problem statement

Retailers may monitor competitors in spreadsheets while demand and stock signals live in separate systems. Manual updates are slow, inconsistent and can cause margin erosion or unnecessary price wars. The project tests whether one explainable workspace can make pricing reviews faster and more auditable.

## 3. Target users and jobs-to-be-done

- **Pricing analyst:** “When I review a SKU, help me understand whether price should move and why, while protecting margin.”
- **Category manager:** “When many products need review, help me prioritise inventory risk and high-impact decisions.”
- **E-commerce manager:** “When competitors change prices, help me react proportionately rather than blindly matching them.”
- **Finance/merchandising reviewer:** “Before approving a change, show the cost floor, estimated margin and assumptions.”

These are hypotheses to validate through interviews, not findings from completed research.

## 4. Goals and non-goals

### Goals
1. Produce an explainable recommendation for each product using defined inputs.
2. Keep the recommendation inside configured price-movement and gross-margin guardrails.
3. Make product-level reasoning inspectable and exportable.
4. Demonstrate end-to-end frontend/backend integration.
5. Establish an evaluation plan for future data-driven calibration.

### Non-goals for this version
- Live web scraping or licensed competitor feed integration.
- Automatically publishing prices to a store.
- Guaranteed revenue/profit uplift.
- Fully trained machine-learning demand forecasting.
- Multi-tenant production security, payments or enterprise deployment.

## 5. MVP scope and acceptance criteria

| Feature | Acceptance criterion | Status |
|---|---|---|
| Portfolio overview | Shows SKU count, inventory units, average demand and directional revenue scenario | Implemented |
| Product catalogue | Lists products with current/competitor price, demand and stock cover | Implemented |
| Optimise all | API returns one recommendation per SKU and UI updates the table | Implemented |
| Recommendation inspector | Explains demand, inventory, competitor pressure and constraints | Implemented |
| Margin guardrail | Recommendation does not undercut cost plus configured margin floor | Implemented; unit tests included |
| Movement guardrail | Recommendation movement does not exceed configured limit, except when constraints conflict with candidate price; final price still respects floor | Implemented |
| CSV export | Downloads SKU-level recommendations | Implemented |
| Real competitor integration | Uses an approved external source with freshness metadata | Not implemented |
| Historical model evaluation | Backtest against historical holdout data | Planned |
| Human approval and audit | Records reviewer, reason, timestamp and approved price | Planned |

## 6. UX principles

- **Explain before persuade:** each recommendation displays contributing signals and guardrails.
- **Human in the loop:** recommendation is not a command; no price is published automatically.
- **Progressive disclosure:** portfolio KPIs first, then SKU table, then detailed inspector.
- **Clear uncertainty:** synthetic data and directional assumptions are labelled visibly.
- **Operational safety:** margin floor, maximum movement and auditability should be explicit.
- **Accessible responsive layout:** readable contrast, keyboard-accessible controls and responsive table container; conduct formal WCAG review before release.

## 7. User stories

1. As an analyst, I can filter SKUs by recommendation direction so I can focus my review.
2. As a category manager, I can inspect the logic behind a price so I can challenge assumptions.
3. As a finance reviewer, I can see the minimum allowable price and gross margin before recommending approval.
4. As an analyst, I can export recommendations for review outside the application.
5. As a project evaluator, I can inspect API endpoints and tests to verify end-to-end behaviour.

## 8. Metrics

### Product usability
- Task completion rate for “find a SKU and explain its recommendation”.
- Median time to review one SKU.
- Percentage of recommendations users mark understandable.
- Export success rate and API error rate.

### Model/business evaluation
- Gross margin per unit and gross profit, not revenue alone.
- Conversion rate, units sold, stockout rate and inventory age.
- Price elasticity estimates and price-change reversal rate.
- Guardrail violation rate (target 0).
- Recommendation acceptance rate, segmented by category.

Do not optimise revenue in isolation; revenue can rise while profit falls.

## 9. Dependencies and assumptions

- Product master has stable SKU IDs, current price, unit cost and on-hand stock.
- Competitor price is comparable on pack size, shipping, seller reliability and promotion status.
- Demand index can eventually be computed from observed traffic, conversion and sales.
- Daily sales is a reasonable near-term estimate for inventory cover.
- Data is sufficiently fresh and timestamped for a meaningful decision.

## 10. Release plan

- **MVP (this repo):** synthetic data, explainable heuristics, API, dashboard, export and docs.
- **V1 data integration:** database, historical records, scheduled imports, source/freshness indicators and user authentication.
- **V2 analytics:** elasticity estimation, demand forecasting, backtesting and category-specific parameters.
- **V3 controlled operations:** human approval, staged rollout, A/B testing, monitoring, alerts and rollback.
