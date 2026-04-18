"""
test_search.py - Manual test script for semantic search.

Tests the full semantic search pipeline end-to-end:
    products.json → embeddings → FAISS index → query → ranked results

Usage:
    cd backend
    source .venv/bin/activate
    python test_search.py
"""

import json
import os
import sys
import numpy as np

# Make the app package importable from the backend/ directory
sys.path.insert(0, os.path.dirname(__file__))

from app.services.embedding_service import EmbeddingService
from app.vectorstore.faiss_index import FAISSIndex

# ── Config ────────────────────────────────────────────────────────────────────
PRODUCTS_PATH = os.path.join(os.path.dirname(__file__), "../data/products.json")
QUERY         = "cheap phone with good camera"
TOP_K         = 5

# ── Step 1: Load products from JSON ───────────────────────────────────────────
print("=" * 60)
print("📂 Step 1 — Loading products")
print("=" * 60)

with open(PRODUCTS_PATH, "r") as f:
    products = json.load(f)

# Build a quick lookup map: product_id → product dict
product_map = {p["id"]: p for p in products}
print(f"✅ Loaded {len(products)} products.\n")


# ── Step 2: Combine fields into searchable text per product ───────────────────
def combine_fields(product: dict) -> str:
    """
    Merge name, description, category, and tags into one string.
    Name is repeated to give it higher weight in the embedding space.
    """
    parts = [
        product.get("name", ""),
        product.get("name", ""),               # repeat for emphasis
        " ".join(product.get("tags", [])),
        product.get("description", ""),
        product.get("category", ""),
        product.get("brand", ""),
    ]
    return " ".join(filter(None, parts))

ids   = [p["id"] for p in products]
texts = [combine_fields(p) for p in products]


# ── Step 3: Generate product embeddings in batch ──────────────────────────────
print("=" * 60)
print("🔄 Step 2 — Generating product embeddings")
print("=" * 60)

# EmbeddingService loads the Sentence Transformer model once
embedding_svc = EmbeddingService()

# encode_products returns shape (n, 384) float32 ndarray
product_vectors: np.ndarray = embedding_svc.encode_products(texts)
print(f"✅ Embeddings shape: {product_vectors.shape}\n")


# ── Step 4: Build an in-memory FAISS index ────────────────────────────────────
print("=" * 60)
print("🗂️  Step 3 — Building FAISS index")
print("=" * 60)

# Create a fresh FAISSIndex (dim=384 matches all-MiniLM-L6-v2 output)
index = FAISSIndex(dim=product_vectors.shape[1])

# add_vectors indexes all product embeddings and maps integer rows → product IDs
index.add_vectors(product_vectors, ids)
print()


# ── Step 5: Encode the query ──────────────────────────────────────────────────
print("=" * 60)
print(f"🔍 Step 4 — Encoding query: \"{QUERY}\"")
print("=" * 60)

# encode_query returns shape (1, 384) — ready for FAISS search
query_vector: np.ndarray = embedding_svc.encode_query(QUERY)
print(f"✅ Query vector shape: {query_vector.shape}\n")


# ── Step 6: Search the FAISS index ───────────────────────────────────────────
print("=" * 60)
print(f"📊 Step 5 — Top {TOP_K} semantic search results")
print("=" * 60)

# Returns list of { "id": str, "score": float } sorted by L2 distance (asc)
results = index.search(query_vector, k=TOP_K)

if not results:
    print("⚠️  No results returned. Check that products were indexed correctly.")
    sys.exit(1)


# ── Step 7: Print results ─────────────────────────────────────────────────────
print(f"\nQuery : \"{QUERY}\"\n")
print(f"{'Rank':<5} {'L2 Distance':<14} {'Product Name':<45} {'Category':<15} {'Price'}")
print("-" * 95)

for rank, result in enumerate(results, start=1):
    product = product_map.get(result["id"], {})
    print(
        f"{rank:<5} "
        f"{result['score']:<14.4f} "
        f"{product.get('name','?')[:43]:<45} "
        f"{product.get('category','?'):<15} "
        f"${product.get('price', 0):.2f}"
    )

print("\n✅ Semantic search test complete.")
print("ℹ️  Lower L2 distance = more semantically similar to the query.")
