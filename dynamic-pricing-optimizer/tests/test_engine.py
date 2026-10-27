import unittest
from app.engine import PricingInput, optimize_price

class PricingEngineTests(unittest.TestCase):
    def make(self, **kwargs):
        data = dict(product_id='T1', product_name='Test', current_price=100.0,
                    cost_price=60.0, competitor_price=95.0, demand_index=50,
                    inventory_units=100, daily_sales=10, min_margin_pct=20,
                    max_change_pct=10)
        data.update(kwargs)
        return PricingInput(**data)

    def test_respects_minimum_margin_floor(self):
        result = optimize_price(self.make(current_price=70, competitor_price=40,
                                          demand_index=0, inventory_units=500,
                                          min_margin_pct=25))
        self.assertGreaterEqual(result['recommended_price'], 80.0)
        self.assertGreaterEqual(result['gross_margin_pct'], 25.0)

    def test_change_is_bounded_for_normal_constraints(self):
        result = optimize_price(self.make(demand_index=100, inventory_units=5,
                                          competitor_price=150, max_change_pct=8))
        self.assertLessEqual(result['change_pct'], 8.01)
        self.assertGreaterEqual(result['change_pct'], -8.01)

    def test_inventory_cover_is_calculated(self):
        result = optimize_price(self.make(inventory_units=30, daily_sales=10))
        self.assertEqual(result['inventory_cover_days'], 3.0)

    def test_explanation_is_returned(self):
        result = optimize_price(self.make())
        self.assertGreaterEqual(len(result['reasons']), 3)
        self.assertIn('recommended_price', result)
        self.assertIn('guardrails', result)

if __name__ == '__main__':
    unittest.main()
