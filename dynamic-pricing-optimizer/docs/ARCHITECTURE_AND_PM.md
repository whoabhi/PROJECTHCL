# Architecture, Delivery Plan & PM Artifacts

## Architecture

```text
Browser UI (HTML/CSS/JavaScript)
   | fetch/JSON
   v
FastAPI application
   | validates request / selects SKU
   v
Explainable pricing engine (Python)
   | price recommendation + reasons + guardrails
   v
JSON response -> recommendation table / inspector / CSV export
```

Current demo uses an in-code catalogue and in-memory history. Pandas supports CSV export. No external integrations or database are connected.

## Suggested backlog

| Priority | Epic | Story / deliverable | Definition of done |
|---|---|---|---|
| P0 | Pricing engine | Compute bounded recommendation | Unit tests cover margin floor and movement cap |
| P0 | Dashboard | View product and portfolio metrics | Metrics match API responses |
| P0 | Explainability | Inspect drivers and guardrails | User can explain recommendation from UI |
| P0 | Export | Download CSV | File opens and includes one row per SKU |
| P1 | Data layer | Store timestamped observations in SQLite/Postgres | Migrations and data validation exist |
| P1 | Competitor integration | Import an approved API/CSV feed | Source, timestamp, stale-data rules visible |
| P1 | Authentication | Restrict access and role-based approvals | Protected endpoints and audit events |
| P1 | Experimentation | Track approved price changes and outcomes | Experiment assignment and outcome data logged |
| P2 | Forecasting | Train and compare demand model | Time-based holdout beats baseline or is not shipped |
| P2 | Operations | Monitoring, rollback and alerting | Tested rollback and incident runbook |

## Delivery milestones (suggested 2-week sprint)
- Days 1–2: problem framing, stakeholder assumptions, data dictionary, research plan.
- Days 3–4: UI flow and low-fidelity wireframe; validate labels and workflow with 3 users.
- Days 5–7: API and engine, constraints, unit tests, synthetic data generation.
- Days 8–9: frontend integration, error states, responsive checks and CSV export.
- Days 10–11: model limitations, analytics plan, documentation and architecture review.
- Days 12–13: usability test, fix issues, run test suite and rehearse demo.
- Day 14: final report, 5-minute demo, limitations and future roadmap.

## Risks

| Risk | Likelihood / impact | Mitigation |
|---|---|---|
| Synthetic data mistaken for live data | Medium / High | Persistent labels in UI and report; disclose in presentation |
| Heuristic coefficients not calibrated | High / High | Call model illustrative; obtain historical data and backtest |
| Revenue scenario mistaken for uplift | High / High | Explain constant-volume assumption; prioritise gross profit in future |
| Competitor offer not comparable | High / Medium | Add seller, pack size, shipping, availability and timestamp checks |
| API unavailable during demo | Medium / Medium | Start server in advance; test `/api/health`; keep screenshots as backup |
| Over-scope | High / Medium | Deliver a narrow, tested MVP before integrations |

## Definition of done
- A clean setup from README works on a fresh Python environment.
- API health endpoint returns `ok`.
- All unit tests pass.
- Optimise-all returns one recommendation per SKU.
- Margin and movement guardrails are tested.
- UI labels synthetic data and never claims live feeds.
- CSV export works and project limitations are in the report.

## Demo talk track (5 minutes)
1. Problem: pricing decisions often fragment competitor, demand, inventory and cost signals.
2. Product: show overview and product catalogue.
3. Action: optimise all, filter increases/decreases, inspect a SKU.
4. Trust: explain price drivers and show margin/movement guardrails.
5. Engineering: show `/docs`, explain API contract and unit tests.
6. Analytics maturity: clearly distinguish heuristic decision support from a trained model; describe historical backtesting and controlled experiment as next steps.
