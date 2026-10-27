"""Explainable pricing engine for the Dynamic Pricing Strategy Optimiser demo."""
from dataclasses import dataclass, asdict
from typing import Any
import math

@dataclass
class PricingInput:
    product_id: str
    product_name: str
    current_price: float
    cost_price: float
    competitor_price: float
    demand_index: float       # 0-100
    inventory_units: int
    daily_sales: float
    min_margin_pct: float = 12.0
    max_change_pct: float = 15.0
    price_position_pct: float = 0.0


def optimize_price(p: PricingInput) -> dict[str, Any]:
    """Return a recommendation with transparent, bounded rules; not a black box.

    Demand and scarcity lift price; excess inventory and a competitor undercut
    create downward pressure. Cost floor, margin floor, and movement limits are
    hard constraints. The output is a decision-support recommendation, not an
    automatic price change.
    """
    current = max(float(p.current_price), 0.01)
    cost = max(float(p.cost_price), 0.0)
    competitor = max(float(p.competitor_price), 0.01)
    demand = min(100.0, max(0.0, float(p.demand_index)))
    inventory = max(0, int(p.inventory_units))
    daily_sales = max(0.1, float(p.daily_sales))
    cover_days = inventory / daily_sales

    # Interpretable demand signal: -6% at very weak demand, +8% at very strong demand.
    demand_effect = ((demand - 50.0) / 50.0) * 0.08
    # Scarcity: low cover adds a premium; high cover prompts markdowns.
    if cover_days < 3:
        inventory_effect = 0.07
    elif cover_days < 7:
        inventory_effect = 0.03
    elif cover_days > 30:
        inventory_effect = -0.08
    elif cover_days > 18:
        inventory_effect = -0.04
    else:
        inventory_effect = 0.0
    # Competitor response is deliberately capped; matching is not always optimal.
    gap = (competitor - current) / current
    competitor_effect = max(-0.06, min(0.06, gap * 0.45))

    raw_change = demand_effect + inventory_effect + competitor_effect
    max_change = min(30.0, max(1.0, float(p.max_change_pct))) / 100.0
    bounded_change = max(-max_change, min(max_change, raw_change))
    candidate = current * (1.0 + bounded_change)

    # Guardrails: minimum gross margin and a sensible ceiling relative to competitor.
    margin_target = min(90.0, max(0.0, float(p.min_margin_pct))) / 100.0
    margin_floor = cost / (1.0 - margin_target) if margin_target < 1.0 else float("inf")
    lower_bound = max(margin_floor, current * (1.0 - max_change))
    upper_bound = current * (1.0 + max_change)
    # Don't enforce competitor parity; only avoid extreme premium in this demo.
    upper_bound = min(upper_bound, competitor * 1.25)
    recommended = max(lower_bound, min(upper_bound, candidate))
    recommended = round(recommended, 2)
    change_pct = round((recommended / current - 1) * 100, 2)
    gross_margin = round((recommended - cost) / recommended * 100, 2) if recommended else 0
    estimated_daily_revenue = round(recommended * daily_sales, 2)
    current_daily_revenue = round(current * daily_sales, 2)

    reasons = []
    reasons.append(f"Demand is {demand:.0f}/100, contributing {demand_effect*100:+.1f}% price pressure.")
    reasons.append(f"Inventory cover is {cover_days:.1f} days, contributing {inventory_effect*100:+.1f}%.")
    reasons.append(f"Competitor is {((competitor/current)-1)*100:+.1f}% vs your current price; competitor signal contributes {competitor_effect*100:+.1f}%.")
    if recommended <= margin_floor + 0.01 and candidate < margin_floor:
        reasons.append(f"Margin guardrail applied: price cannot fall below ₹{margin_floor:.2f}.")
    if abs(change_pct) >= max_change * 100 - 0.02:
        reasons.append(f"Change limit applied: movement is capped at {max_change*100:.0f}% per recommendation.")
    if cover_days < 3:
        action = "Protect margin / manage scarcity"
    elif cover_days > 18 and demand < 55:
        action = "Clear excess inventory"
    elif change_pct > 1:
        action = "Increase selectively"
    elif change_pct < -1:
        action = "Use a controlled markdown"
    else:
        action = "Hold price and monitor"

    return {
        "product_id": p.product_id, "product_name": p.product_name,
        "current_price": round(current, 2), "recommended_price": recommended,
        "change_pct": change_pct, "competitor_price": round(competitor, 2),
        "cost_price": round(cost, 2), "gross_margin_pct": gross_margin,
        "inventory_units": inventory, "daily_sales": round(daily_sales, 1),
        "inventory_cover_days": round(cover_days, 1), "demand_index": round(demand, 1),
        "estimated_daily_revenue": estimated_daily_revenue,
        "current_daily_revenue": current_daily_revenue,
        "daily_revenue_delta": round(estimated_daily_revenue-current_daily_revenue, 2),
        "action": action, "reasons": reasons,
        "guardrails": {"minimum_price": round(margin_floor, 2), "max_change_pct": round(max_change*100, 1)},
        "model": "Explainable hybrid rules v1", "confidence": "Directional estimate; validate with experiments"
    }
