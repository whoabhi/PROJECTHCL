from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import csv
import io
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .engine import PricingInput, optimize_price

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="Dynamic Pricing Strategy Optimiser", version="1.0.0", description="Academic decision-support prototype for demand-, competitor- and inventory-aware pricing.")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")

PRODUCTS = [
 {"product_id":"SKU-101","product_name":"Wireless Headphones","category":"Electronics","current_price":2499,"cost_price":1450,"competitor_price":2299,"demand_index":78,"inventory_units":84,"daily_sales":12,"min_margin_pct":15,"max_change_pct":12},
 {"product_id":"SKU-102","product_name":"Everyday Backpack","category":"Accessories","current_price":1799,"cost_price":820,"competitor_price":1899,"demand_index":62,"inventory_units":420,"daily_sales":11,"min_margin_pct":18,"max_change_pct":15},
 {"product_id":"SKU-103","product_name":"Smart Watch","category":"Electronics","current_price":4999,"cost_price":3300,"competitor_price":4599,"demand_index":44,"inventory_units":38,"daily_sales":9,"min_margin_pct":12,"max_change_pct":10},
 {"product_id":"SKU-104","product_name":"Insulated Bottle","category":"Lifestyle","current_price":899,"cost_price":310,"competitor_price":949,"demand_index":35,"inventory_units":760,"daily_sales":18,"min_margin_pct":20,"max_change_pct":15},
 {"product_id":"SKU-105","product_name":"Running Shoes","category":"Apparel","current_price":3299,"cost_price":1880,"competitor_price":3499,"demand_index":86,"inventory_units":26,"daily_sales":13,"min_margin_pct":16,"max_change_pct":10},
 {"product_id":"SKU-106","product_name":"USB-C Hub","category":"Electronics","current_price":1499,"cost_price":650,"competitor_price":1399,"demand_index":53,"inventory_units":180,"daily_sales":7,"min_margin_pct":15,"max_change_pct":12},
 {"product_id":"SKU-107","product_name":"Desk Lamp","category":"Home Office","current_price":1299,"cost_price":540,"competitor_price":1199,"demand_index":29,"inventory_units":540,"daily_sales":8,"min_margin_pct":18,"max_change_pct":15},
 {"product_id":"SKU-108","product_name":"Portable Speaker","category":"Electronics","current_price":2199,"cost_price":1190,"competitor_price":2399,"demand_index":71,"inventory_units":65,"daily_sales":10,"min_margin_pct":15,"max_change_pct":12},
]
HISTORY = []

class OptimizeRequest(BaseModel):
 product_id: str
 current_price: Optional[float] = Field(None, gt=0)
 cost_price: Optional[float] = Field(None, ge=0)
 competitor_price: Optional[float] = Field(None, gt=0)
 demand_index: Optional[float] = Field(None, ge=0, le=100)
 inventory_units: Optional[int] = Field(None, ge=0)
 daily_sales: Optional[float] = Field(None, gt=0)
 min_margin_pct: Optional[float] = Field(None, ge=0, le=90)
 max_change_pct: Optional[float] = Field(None, ge=1, le=30)


def product_input(product: dict, overrides: dict | None = None) -> PricingInput:
 data = dict(product)
 data.update({k:v for k,v in (overrides or {}).items() if v is not None and k in data})
 data.setdefault("price_position_pct", 0.0)
 return PricingInput(**{k:data[k] for k in PricingInput.__dataclass_fields__})

@app.get("/", response_class=HTMLResponse)
def home():
 return (ROOT / "frontend" / "index.html").read_text(encoding="utf-8")

@app.get("/api/health")
def health():
 return {"status":"ok","service":"Dynamic Pricing Strategy Optimiser","timestamp":datetime.now(timezone.utc).isoformat(),"mode":"demo data; no live competitor feed connected"}

@app.get("/api/products")
def get_products():
 return {"products":[{**p,"category":p["category"]} for p in PRODUCTS],"count":len(PRODUCTS),"data_note":"Synthetic demonstration catalogue. Replace with approved real feeds before operational use."}

@app.post("/api/optimize")
def optimize(req: OptimizeRequest):
 p = next((x for x in PRODUCTS if x["product_id"] == req.product_id), None)
 if not p: raise HTTPException(404, "Unknown product_id")
 result = optimize_price(product_input(p, req.model_dump(exclude={"product_id"})))
 result["created_at"] = datetime.now(timezone.utc).isoformat()
 HISTORY.insert(0, result)
 del HISTORY[100:]
 return result

@app.post("/api/optimize-all")
def optimize_all():
 results = []
 for p in PRODUCTS:
  r = optimize_price(product_input(p)); results.append(r)
  HISTORY.insert(0, {**r,"created_at":datetime.now(timezone.utc).isoformat()})
 return {"results":results,"count":len(results)}

@app.get("/api/metrics")
def metrics():
 results = [optimize_price(product_input(p)) for p in PRODUCTS]
 current_rev = sum(r["current_daily_revenue"] for r in results)
 rec_rev = sum(r["estimated_daily_revenue"] for r in results)
 return {"sku_count":len(PRODUCTS),"avg_demand":round(sum(p["demand_index"] for p in PRODUCTS)/len(PRODUCTS),1),"inventory_units":sum(p["inventory_units"] for p in PRODUCTS),"current_daily_revenue":round(current_rev,2),"estimated_daily_revenue":round(rec_rev,2),"revenue_delta":round(rec_rev-current_rev,2),"recommendations_up":sum(r["change_pct"]>0.5 for r in results),"recommendations_down":sum(r["change_pct"]< -0.5 for r in results),"recommendations_hold":sum(abs(r["change_pct"])<=0.5 for r in results),"results":results}

@app.get("/api/history")
def history(): return {"history":HISTORY[:30]}

@app.get("/api/export.csv")
def export_csv():
 results = [optimize_price(product_input(p)) for p in PRODUCTS]
 frame = pd.DataFrame(results)
 stream = io.StringIO(); frame.to_csv(stream,index=False)
 return StreamingResponse(iter([stream.getvalue()]), media_type="text/csv", headers={"Content-Disposition":"attachment; filename=pricing_recommendations.csv"})
