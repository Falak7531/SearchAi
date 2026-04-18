"""
scripts/generate_embeddings.py
Generates dense vector embeddings for all products and saves them
to data/processed_products.json alongside their original fields.

Usage:
    python scripts/generate_embeddings.py
"""

import sys
import os
import json

# Make the backend app importable from the scripts directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../backend"))

from app.services.embedding_service import embedding_service
from app.utils.preprocessing import build_product_text

PRODUCTS_PATH = os.path.join(os.path.dirname(__file__), "../data/products.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../data/processed_products.json")


def generate():
    print("📂 Loading products...")
    with open(PRODUCTS_PATH, "r") as f:
        products = json.load(f)

    print(f"🔄 Generating embeddings for {len(products)} products...")
    texts = [build_product_text(p) for p in products]
    embeddings = embedding_service.encode_products(texts)

    # Attach embedding vectors to each product record
    processed = []
    for product, embedding in zip(products, embeddings):
        processed.append({
            **product,
            "embedding": embedding.tolist(),
        })

    with open(OUTPUT_PATH, "w") as f:
        json.dump(processed, f, indent=2)

    print(f"✅ Saved {len(processed)} processed products to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
