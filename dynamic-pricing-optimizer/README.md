# PricePilot: Dynamic Pricing Strategy Optimiser

**HCL Career Shaper academic project | Domain: Data Analytics with Python**

A full-stack, explainable pricing decision-support prototype that combines competitor price, demand index, inventory cover, unit cost and configurable business guardrails. It is designed to be demonstrable locally and extensible toward real data feeds.

> **Important truth-in-labeling:** the bundled catalogue and competitor prices are synthetic demonstration data. There is no live retailer/competitor connection, no production-trained ML model, and no automatic price publishing. The tool generates advisory scenarios for human review. Do not present simulated uplift as a measured business result.

## What is included

- Responsive dashboard UI with catalogue search, action filters, KPI cards, recommendation inspector and CSV export.
- FastAPI backend with validation, health check, catalogue, single/all SKU optimisation, metrics, and CSV export endpoints.
- Explainable Python pricing engine: demand effect, inventory scarcity/excess effect, competitor gap effect, price-movement cap, minimum gross-margin floor and competitor-premium ceiling.
- Synthetic product catalogue with eight products across categories.
- Project/product management docs: problem framing, user research plan, PRD, event/metric definitions, architecture, risk register, experiment plan and demo script.
- Unit tests for pricing constraints.

## Run locally

Requires Python 3.10+.

```bash
# Windows PowerShell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`. API docs are at `http://127.0.0.1:8000/docs` and health at `http://127.0.0.1:8000/api/health`.

Run tests from the project root:

```bash
python -m unittest discover -s tests -v
```

## API quick reference

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/health` | Service health and demo-data status |
| GET | `/api/products` | Product catalogue |
| GET | `/api/metrics` | Portfolio-level demo metrics and recommendations |
| POST | `/api/optimize` | Optimise one SKU using optional overrides |
| POST | `/api/optimize-all` | Generate recommendations for all SKUs |
| GET | `/api/history` | In-memory recommendation history for this server process |
| GET | `/api/export.csv` | Export product-level recommendations |

Example request:

```json
{
  "product_id": "SKU-101",
  "competitor_price": 2249,
  "demand_index": 82,
  "inventory_units": 72,
  "daily_sales": 12,
  "min_margin_pct": 15,
  "max_change_pct": 10
}
```

## Pricing logic (v1)

1. Demand pressure ranges from approximately -8% to +8% as the demand index moves from 0 to 100.
2. Inventory cover is `inventory_units / daily_sales`; below 3 days creates a scarcity premium, while high cover triggers markdown pressure.
3. Competitor price gap influences the candidate price but its effect is capped to avoid reactive price wars.
4. Combined movement is limited by a configurable maximum change.
5. Final price is bounded by the minimum-margin price floor and a ceiling relative to competitor price.
6. A recommendation is advisory; a real deployment must add approval workflow, price-history storage, monitoring and rollback.

These are transparent heuristic coefficients selected for a classroom prototype, not empirically calibrated business constants. They should be estimated from historical data and reviewed with domain stakeholders before production.

## Current limitations and next steps

- No live competitor APIs, scraping, inventory system, point-of-sale feed, authentication, database, scheduler or deployment pipeline.
- Revenue scenario multiplies recommended price by current daily sales. It assumes volume remains constant and therefore is **not a demand-elasticity forecast**.
- Demo demand index is illustrative. A production model needs timestamped historical price, traffic, conversion, stockouts, promotions, seasonality and unit economics.
- `HISTORY` is in-memory and resets when the server restarts.
- Add model validation, offline backtesting, elasticity estimation, time-series features, drift checks, role-based approval and audit logs before real usage.

## Suggested project narrative

“I built a full-stack pricing decision-support prototype using Python, FastAPI and a responsive web UI. It brings together competitor positioning, demand and inventory signals, enforces margin and price-movement guardrails, and explains every recommendation. I documented the research assumptions and proposed a controlled A/B experiment rather than claiming unverified revenue gains.”
