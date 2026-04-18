"""Normalize product prices to realistic USD ranges and add Nike shoes."""
import json

with open("data/products.json") as f:
    products = json.load(f)

# Realistic price ranges (USD) per category
PRICE_RANGES = {
    "accessories": (9.99, 149.99),
    "headphones": (19.99, 449.99),
    "laptop": (399.99, 2499.99),
    "smartphone": (149.99, 1399.99),
    "smartwatch": (49.99, 799.99),
    "tablet": (149.99, 1299.99),
}

# Normalize: map each product's price proportionally into the realistic range
for cat in set(p["category"] for p in products):
    if cat not in PRICE_RANGES:
        continue  # shoes already have correct prices
    cat_products = [p for p in products if p["category"] == cat]
    old_prices = [p["price"] for p in cat_products]
    old_min, old_max = min(old_prices), max(old_prices)
    new_min, new_max = PRICE_RANGES[cat]
    for p in cat_products:
        if old_max == old_min:
            ratio = 0.5
        else:
            ratio = (p["price"] - old_min) / (old_max - old_min)
        p["price"] = round(new_min + ratio * (new_max - new_min), 2)

# Remove any existing Nike shoes (from prior partial run) to avoid duplicates
products = [p for p in products if not (p.get("category") == "shoes")]

# Add Nike shoes
max_id = max(p["id"] for p in products)
nike_shoes = [
    {"title": "Nike Air Max 270", "description": "Nike Air Max 270 with large Air unit in the heel for unrivaled all-day comfort. Lightweight mesh upper and modern sleek design for everyday wear.", "price": 159.99, "rating": 4.7, "category": "shoes", "brand": "Nike", "tags": ["running", "comfortable", "air max", "casual", "lightweight"]},
    {"title": "Nike ZoomX Vaporfly NEXT%", "description": "Nike ZoomX Vaporfly NEXT% with carbon fiber plate and ZoomX foam for record-breaking speed. Designed for competitive marathon runners.", "price": 249.99, "rating": 4.9, "category": "shoes", "brand": "Nike", "tags": ["racing", "marathon", "performance", "carbon plate", "elite"]},
    {"title": "Nike Pegasus 41", "description": "Nike Pegasus 41 featuring ReactX foam for a smooth, responsive ride. The go-to daily running shoe trusted by millions of runners worldwide.", "price": 139.99, "rating": 4.6, "category": "shoes", "brand": "Nike", "tags": ["running", "daily trainer", "cushioned", "responsive", "versatile"]},
    {"title": "Nike Air Force 1 '07", "description": "Nike Air Force 1 '07 — the iconic basketball-inspired sneaker with crisp leather upper and encapsulated Air sole. A timeless classic since 1982.", "price": 109.99, "rating": 4.8, "category": "shoes", "brand": "Nike", "tags": ["classic", "casual", "leather", "iconic", "street style"]},
    {"title": "Nike Revolution 7", "description": "Nike Revolution 7 with soft cushioning and lightweight breathable mesh. An affordable entry-level running shoe perfect for beginners.", "price": 69.99, "rating": 4.3, "category": "shoes", "brand": "Nike", "tags": ["budget", "running", "beginner", "lightweight", "breathable"]},
    {"title": "Nike Dunk Low Retro", "description": "Nike Dunk Low Retro with premium leather and padded collar. Originally designed for the basketball court, now a streetwear staple.", "price": 119.99, "rating": 4.7, "category": "shoes", "brand": "Nike", "tags": ["retro", "casual", "streetwear", "leather", "classic"]},
    {"title": "Nike Free Run 5.0", "description": "Nike Free Run 5.0 with flexible grooved sole that mimics barefoot running. Sock-like fit with ultra-lightweight construction.", "price": 109.99, "rating": 4.5, "category": "shoes", "brand": "Nike", "tags": ["barefoot", "flexible", "running", "minimalist", "natural motion"]},
    {"title": "Nike Invincible 3", "description": "Nike Invincible 3 with thick ZoomX foam for maximum cushioning on long runs. Designed for runners who want plush comfort mile after mile.", "price": 179.99, "rating": 4.6, "category": "shoes", "brand": "Nike", "tags": ["max cushion", "long distance", "running", "plush", "recovery"]},
    {"title": "Nike Air Zoom Structure 25", "description": "Nike Air Zoom Structure 25 with stability support for overpronators. Dual-density foam and wide base provide a secure, guided ride.", "price": 139.99, "rating": 4.4, "category": "shoes", "brand": "Nike", "tags": ["stability", "running", "support", "overpronation", "structured"]},
    {"title": "Nike Metcon 9", "description": "Nike Metcon 9 built for high-intensity training and CrossFit. Flat stable heel, rope-wrap outsole, and reactive cushioning for explosive workouts.", "price": 149.99, "rating": 4.7, "category": "shoes", "brand": "Nike", "tags": ["training", "crossfit", "gym", "weightlifting", "HIIT"]},
    {"title": "Nike Wildhorse 8", "description": "Nike Wildhorse 8 trail running shoe with aggressive lug pattern and rock plate. Durable protection and grip for rugged off-road terrain.", "price": 149.99, "rating": 4.5, "category": "shoes", "brand": "Nike", "tags": ["trail", "off-road", "rugged", "grip", "outdoor"]},
    {"title": "Nike Air Monarch IV", "description": "Nike Air Monarch IV with full-length Air sole and leather upper. The ultimate dad shoe — comfortable, affordable, and reliable for everyday use.", "price": 74.99, "rating": 4.2, "category": "shoes", "brand": "Nike", "tags": ["budget", "walking", "comfort", "classic", "everyday"]},
    {"title": "Nike React Infinity Run 4", "description": "Nike React Infinity Run 4 designed to help reduce running injuries. Wide rocker sole and plush React foam keep your stride smooth and supported.", "price": 164.99, "rating": 4.6, "category": "shoes", "brand": "Nike", "tags": ["injury prevention", "running", "support", "cushioned", "rocker"]},
    {"title": "Nike Zoom Fly 6", "description": "Nike Zoom Fly 6 tempo running shoe with carbon fiber plate for fast-paced training. Bridges the gap between daily trainers and race-day shoes.", "price": 169.99, "rating": 4.5, "category": "shoes", "brand": "Nike", "tags": ["tempo", "speed", "carbon plate", "running", "training"]},
    {"title": "Nike Air Zoom Alphafly NEXT% 3", "description": "Nike Alphafly NEXT% 3 — the pinnacle of Nike racing technology. Double Air Zoom pods, carbon plate, and AtomKnit upper for sub-2-hour marathon performance.", "price": 249.99, "rating": 4.9, "category": "shoes", "brand": "Nike", "tags": ["elite", "racing", "marathon", "carbon plate", "record breaking"]},
]

for i, shoe in enumerate(nike_shoes, start=max_id + 1):
    shoe["id"] = i
    products.append(shoe)

products.sort(key=lambda p: p["id"])

with open("data/products.json", "w") as f:
    json.dump(products, f, indent=2)

# Print summary
prices = [p["price"] for p in products]
print(f"Total products: {len(products)}")
print(f"Price range: ${min(prices):.2f} - ${max(prices):.2f}")
for cat in sorted(set(p["category"] for p in products)):
    cp = [p["price"] for p in products if p["category"] == cat]
    print(f"  {cat:15s}: ${min(cp):>8.2f} - ${max(cp):>8.2f}  (n={len(cp)})")
