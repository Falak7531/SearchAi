"""
vectorstore/build_index.py - Builds the FAISS vector index from product data.

Steps:
    1. Load products from data/products.json
    2. Combine name + description + category into one searchable text per product
    3. Generate embeddings in batch using EmbeddingService
    4. Add all vectors to FAISSIndex and persist to disk

Usage:
    cd backend
    python -m app.vectorstore.build_index
"""

import json
import os
import sys
import numpy as np

# Make sure the backend/app package is importable when run as a script
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.services.embedding_service import embedding_service
from app.vectorstore.faiss_index import faiss_index

# Path to the raw product data file
PRODUCTS_PATH = os.environ.get(
    "PRODUCTS_PATH",
    os.path.join(os.path.dirname(__file__), "../../../data/products.json"),
)


def combine_fields(product: dict) -> str:
    """
    Merge the most semantically rich product fields into a single string.
    Field order and repetition influence embedding quality:
      - name repeated twice → higher weight in the vector space
      - tags joined with spaces → keyword signals
      - description → context and detail
      - category / brand → broad grouping signals
    """
    parts = [
        product.get("name", ""),
        product.get("name", ""),                    # repeat for emphasis
        " ".join(product.get("tags", [])),
        product.get("description", ""),
        product.get("category", ""),
        product.get("brand", ""),
    ]
    # Filter empty strings and join with a space separator
    return " ".join(filter(None, parts))


def build():
    # ── Step 1: Load products ─────────────────────────────────────────────
    print(f"📂 Loading products from {PRODUCTS_PATH} ...")
    with open(PRODUCTS_PATH, "r") as f:
        products = json.load(f)

    if not products:
        print("❌ No products found. Run scripts/load_data.py first.")
        sys.exit(1)

    print(f"✅ Loaded {len(products)} products.\n")

    # ── Step 2: Build combined text strings ───────────────────────────────
    print("📝 Combining product fields (name + description + category) ...")
    ids = []
    texts = []
    for product in products:
        ids.append(product["id"])
        texts.append(combine_fields(product))

    # ── Step 3: Generate embeddings in one batch pass ─────────────────────
    # Batch encoding is far more efficient than embedding one product at a time
    print(f"🔄 Generating embeddings for {len(texts)} products ...")
    vectors: np.ndarray = embedding_service.encode_products(texts)  # shape: (n, 384)
    print(f"✅ Embeddings ready — shape: {vectors.shape}\n")

    # ── Step 4: Build FAISS index and persist to disk ─────────────────────
    print("🗂️  Building FAISS index ...")
    faiss_index.add_vectors(vectors, ids)

    print(f"\n🎉 Done! FAISS index built with {len(ids)} products and saved to disk.")


if __name__ == "__main__":
    build()
