"""
scripts/load_data.py
End-to-end data pipeline script. Runs in sequence:
  1. Seeds products.json with sample data
  2. Indexes products into Elasticsearch (if available)
  3. Generates embeddings and builds the FAISS index

Usage:
    python scripts/load_data.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../backend"))

def step(msg):
    print(f"\n{'='*50}\n🔷 {msg}\n{'='*50}")


def main():
    # ── Step 1: Seed the JSON database ─────────────────
    step("Step 1/3 — Seeding product database")
    from app.db.seed import seed
    seed()

    # ── Step 2: Index into Elasticsearch ───────────────
    step("Step 2/3 — Indexing into Elasticsearch")
    import json
    from app.services.keyword_search import keyword_search_service

    products_path = os.path.join(os.path.dirname(__file__), "../data/products.json")
    with open(products_path) as f:
        products = json.load(f)

    keyword_search_service.index_products(products)

    # ── Step 3: Build FAISS index ───────────────────────
    step("Step 3/3 — Building FAISS vector index")
    from app.vectorstore.build_index import build
    build()

    print("\n🎉 Data pipeline complete! The system is ready to serve searches.\n")


if __name__ == "__main__":
    main()
