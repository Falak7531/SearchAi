"""
utils/preprocessing.py - Text preprocessing utilities.
Cleans and normalizes product text before embedding or indexing.
"""

import re
from typing import List


def clean_text(text: str) -> str:
    """
    Normalize raw text: lowercase, remove special characters,
    and collapse multiple spaces.
    """
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s.,'-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_product_text(product: dict) -> str:
    """
    Construct a single rich text string from a product dict.
    Used as input to the embedding model.

    Weights fields by importance: name > tags > description > brand/category.
    """
    parts = [
        product.get("name", "") * 2,          # Repeat name for higher weight
        " ".join(product.get("tags", [])),
        product.get("description", ""),
        product.get("brand", ""),
        product.get("category", ""),
    ]
    combined = " ".join(filter(None, parts))
    return clean_text(combined)


def tokenize(text: str) -> List[str]:
    """Simple whitespace tokenizer."""
    return clean_text(text).split()
