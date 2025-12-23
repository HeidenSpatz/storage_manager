#!/usr/bin/env python3
"""
Clean up ingredient data: merge duplicates, fix categories, standardize names
"""
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "storage_data.json"

# Define merging rules: duplicates that should be merged
# Format: "name_to_keep": ["duplicate1", "duplicate2", ...]
MERGE_DUPLICATES = {
    "Carrots": ["Carottes", "Carotts"],
    "Carrots julienne": ["Carotts julienne", "carottes cujulienne",],
    "Carrot cubes": ["Karotten cut cubes"],
    "Celery": [],
    "Celery julienne": ["Sellerie julienne", "cellery julienne"],
    "Coconut milk": ["Coconutmilk", "Kokosnussmilch"],
    "Onions": [],  # Keep separate: Onions vs Onions TK
    "Onions TK": ["Onion TK", "Zwiebeln tk"],
    "Potatoes": [],
    "Potatoes peeled": ["Potatoe peeled"],
    "Sweet potatoes": ["Sweet potatoe cut"],
    "Rice": ["Reis"],
    "Minced meat": ["minced meat Beef"],
    "Red Wine": ["redwine"],
    "Red Pepper": ["Paprika (rot/gelb) fresh", "red and yellow pepper"],
    "Quinoa": ["quiona"],
    "Coriander fresh": ["Koriander fresh", "coriander fresh"],
    "Chickpeas canned": ["Chickpeas in can"],
    "Sour cream": ["sourcream plain", "Sour Cream Eßlöffel"],
    "Leek": ["Leach", "Lauch cut"],
}

# Define category corrections
# Format: "ingredient_name": "correct_category"
CATEGORY_FIXES = {
    # Side dish
    "Rice": "Side dish",
    "Reis": "Side dish",
    "Millet": "Side dish",
    "Quinoa": "Side dish",
    "Kidney Beans": "Side dish",
    "White Beans": "Side dish",
    "Red lentils": "Side dish",

    # Vegetables
    "Carrots": "Vegetables",
    "Carottes": "Vegetables",
    "Carotts": "Vegetables",
    "Carrots julienne": "Vegetables",
    "Carotts julienne": "Vegetables",
    "Karotten cut cubes": "Vegetables",
    "carottes cujulienne": "Vegetables",
    "Celery": "Vegetables",
    "Celery julienne": "Vegetables",
    "Sellerie julienne": "Vegetables",
    "cellery julienne": "Vegetables",
    "Leek": "Vegetables",
    "Leach": "Vegetables",
    "Lauch cut": "Vegetables",
    "Cauliflower fresh": "Vegetables",
    "Mushrooms fresh": "Vegetables",
    "Red Pepper": "Vegetables",
    "Paprika (rot/gelb) fresh": "Vegetables",
    "red and yellow pepper": "Vegetables",
    "Parsley": "Vegetables",

    # Dairy
    "Feta": "Dairy",
    "Joghurt": "Dairy",
    "Parmesan grinded": "Dairy",
    "Coconut milk": "Dairy",
    "Coconutmilk": "Dairy",
    "Kokosnussmilch": "Dairy",
    "Sour cream": "Dairy",
    "sourcream plain": "Dairy",
    "Sour Cream Eßlöffel": "Dairy",

    # Spices
    "!!!Tandoori masala spice!!!": "Spices",
    "Ginger paste": "Spices",
    "Ginger": "Spices",
    "spice mixture": "Spices",
    "piment": "Spices",
    "laurel": "Spices",
    "juniper": "Spices",
    "Coriander fresh": "Spices",
    "Koriander fresh": "Spices",
    "coriander fresh": "Spices",

    # Canned Goods
    "Chickpeas canned": "Canned Goods",
    "Chickpeas in can": "Canned Goods",

    # Breatfast
    "Oatmeal (Haferflocken)": "Breakfast",

    # Other - fix misclassifications
    "olive oil for dressing, lemon juice, mustard, apple juice, honey": "Other",
}

def normalize_name(name: str) -> str:
    """Normalize ingredient name for comparison."""
    return name.lower().strip()

def load_data():
    """Load data from JSON file."""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    """Save data to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def clean_ingredients(data):
    """Clean ingredient list: merge duplicates and fix categories."""
    ingredients = data['ingredients']

    # Build a map of normalized names to ingredients
    name_to_ingredients = {}
    for ing in ingredients:
        norm_name = normalize_name(ing['name'])
        if norm_name not in name_to_ingredients:
            name_to_ingredients[norm_name] = []
        name_to_ingredients[norm_name].append(ing)

    # Build merge plan
    merge_plan = {}  # Maps ingredient ID to keep ID
    keep_ingredients = {}  # IDs of ingredients to keep

    for keep_name, duplicate_names in MERGE_DUPLICATES.items():
        # Find the ingredient to keep
        norm_keep = normalize_name(keep_name)
        keep_ing = None

        # Try to find existing ingredient with this name
        if norm_keep in name_to_ingredients:
            keep_ing = name_to_ingredients[norm_keep][0]

        # If not found, use the first duplicate as the keeper and rename it
        if not keep_ing and duplicate_names:
            for dup_name in duplicate_names:
                norm_dup = normalize_name(dup_name)
                if norm_dup in name_to_ingredients:
                    keep_ing = name_to_ingredients[norm_dup][0]
                    keep_ing['name'] = keep_name  # Rename to standard name
                    break

        if keep_ing:
            keep_ingredients[keep_ing['id']] = keep_ing

            # Mark duplicates for removal
            for dup_name in duplicate_names:
                norm_dup = normalize_name(dup_name)
                if norm_dup in name_to_ingredients:
                    for dup_ing in name_to_ingredients[norm_dup]:
                        if dup_ing['id'] != keep_ing['id']:
                            merge_plan[dup_ing['id']] = keep_ing['id']
                            print(f"Merging: '{dup_ing['name']}' (ID {dup_ing['id']}) → '{keep_name}' (ID {keep_ing['id']})")

    # Remove duplicates
    cleaned_ingredients = []
    removed_count = 0

    for ing in ingredients:
        if ing['id'] in merge_plan:
            # This is a duplicate, skip it
            removed_count += 1
            continue

        # Fix category if needed
        if ing['name'] in CATEGORY_FIXES:
            old_category = ing['category']
            new_category = CATEGORY_FIXES[ing['name']]
            if old_category != new_category:
                ing['category'] = new_category
                print(f"Fixed category: '{ing['name']}' {old_category} → {new_category}")

        cleaned_ingredients.append(ing)

    # Re-number IDs to be sequential
    for idx, ing in enumerate(cleaned_ingredients, start=1):
        ing['id'] = idx

    data['ingredients'] = cleaned_ingredients

    print(f"\n{'='*60}")
    print(f"Removed {removed_count} duplicate ingredients")
    print(f"Final ingredient count: {len(cleaned_ingredients)}")
    print(f"{'='*60}")

    return data

def main():
    print("="*60)
    print("Cleaning ingredient data...")
    print("="*60)

    # Load data
    data = load_data()
    print(f"Original ingredient count: {len(data['ingredients'])}\n")

    # Clean ingredients
    data = clean_ingredients(data)

    # Save cleaned data
    save_data(data)
    print("\nCleaned data saved to storage_data.json")

if __name__ == "__main__":
    main()
