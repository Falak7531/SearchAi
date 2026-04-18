"""
db/seed.py - Seeds the products.json with sample e-commerce data.
Run this script once to initialize the data layer.
"""

import json
import os
import uuid

PRODUCTS = [
    {
        "id": str(uuid.uuid4()),
        "name": "Sony WH-1000XM5 Wireless Headphones",
        "description": "Industry-leading noise canceling with two processors and eight microphones. Perfect for travel, work, and everything in between.",
        "category": "Electronics",
        "price": 349.99,
        "brand": "Sony",
        "tags": ["headphones", "wireless", "noise-cancelling", "bluetooth", "audio"],
        "image_url": "https://via.placeholder.com/300x300?text=Sony+WH-1000XM5",
        "rating": 4.8,
        "stock": 150,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Apple AirPods Pro (2nd Generation)",
        "description": "Active noise cancellation, Transparency mode, Adaptive Audio. Now with USB-C charging.",
        "category": "Electronics",
        "price": 249.00,
        "brand": "Apple",
        "tags": ["earbuds", "wireless", "noise-cancelling", "apple", "bluetooth"],
        "image_url": "https://via.placeholder.com/300x300?text=AirPods+Pro",
        "rating": 4.7,
        "stock": 200,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Nike Air Max 270",
        "description": "Inspired by two icons of big Air: the Air Max 180 and Air Max 93. Featuring Nike's biggest heel Air unit yet.",
        "category": "Footwear",
        "price": 150.00,
        "brand": "Nike",
        "tags": ["shoes", "sneakers", "running", "nike", "air max"],
        "image_url": "https://via.placeholder.com/300x300?text=Nike+Air+Max",
        "rating": 4.5,
        "stock": 80,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Samsung 4K QLED Smart TV 65\"",
        "description": "Quantum Dot technology delivers brilliant color. With a 65-inch 4K display and built-in Alexa.",
        "category": "Electronics",
        "price": 1299.99,
        "brand": "Samsung",
        "tags": ["tv", "4k", "smart tv", "qled", "samsung", "television"],
        "image_url": "https://via.placeholder.com/300x300?text=Samsung+TV",
        "rating": 4.6,
        "stock": 30,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Instant Pot Duo 7-in-1 Electric Pressure Cooker",
        "description": "7-in-1 multi-cooker: pressure cooker, slow cooker, rice cooker, steamer, sauté, yogurt maker, and warmer.",
        "category": "Kitchen",
        "price": 79.99,
        "brand": "Instant Pot",
        "tags": ["kitchen", "cooking", "pressure cooker", "instant pot", "appliance"],
        "image_url": "https://via.placeholder.com/300x300?text=Instant+Pot",
        "rating": 4.7,
        "stock": 300,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Levi's 501 Original Fit Jeans",
        "description": "The original jean since 1873. Straight leg with a regular fit through the seat and thigh.",
        "category": "Clothing",
        "price": 59.50,
        "brand": "Levi's",
        "tags": ["jeans", "denim", "clothing", "levi's", "pants"],
        "image_url": "https://via.placeholder.com/300x300?text=Levis+501",
        "rating": 4.4,
        "stock": 500,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Kindle Paperwhite (16 GB)",
        "description": "Now with a larger 6.8\" display, adjustable warm light, and up to 10 weeks of battery life.",
        "category": "Electronics",
        "price": 139.99,
        "brand": "Amazon",
        "tags": ["kindle", "ebook", "reader", "amazon", "books", "tablet"],
        "image_url": "https://via.placeholder.com/300x300?text=Kindle+Paperwhite",
        "rating": 4.8,
        "stock": 120,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Yoga Mat Non-Slip 6mm",
        "description": "Extra thick 6mm yoga mat with alignment lines. Anti-slip surface for all types of yoga and exercise.",
        "category": "Sports",
        "price": 29.99,
        "brand": "BalanceFrom",
        "tags": ["yoga", "fitness", "exercise mat", "sports", "gym"],
        "image_url": "https://via.placeholder.com/300x300?text=Yoga+Mat",
        "rating": 4.5,
        "stock": 400,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Dyson V15 Detect Cordless Vacuum",
        "description": "Laser reveals microscopic dust. Acoustic piezo sensor counts and measures dust particles in real time.",
        "category": "Home",
        "price": 749.99,
        "brand": "Dyson",
        "tags": ["vacuum", "cordless", "dyson", "cleaning", "home appliance"],
        "image_url": "https://via.placeholder.com/300x300?text=Dyson+V15",
        "rating": 4.7,
        "stock": 60,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Logitech MX Master 3S Mouse",
        "description": "Advanced ergonomic mouse with ultra-fast scrolling, quiet clicks, and 8K DPI on any surface.",
        "category": "Electronics",
        "price": 99.99,
        "brand": "Logitech",
        "tags": ["mouse", "wireless", "ergonomic", "logitech", "computer", "office"],
        "image_url": "https://via.placeholder.com/300x300?text=MX+Master+3S",
        "rating": 4.9,
        "stock": 250,
    },
]

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../../../../data/products.json")


def seed():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(PRODUCTS, f, indent=2)
    print(f"✅ Seeded {len(PRODUCTS)} products to {OUTPUT_PATH}")


if __name__ == "__main__":
    seed()
