import json
from pathlib import Path
from typing import Dict, List, Optional

DATA_FILE = Path(__file__).parent.parent / "data" / "storage_data.json"


def migrate_ingredient_data(data: Dict) -> Dict:
    """Migrate old ingredient structure to new simplified structure."""
    ingredients = data.get('ingredients', [])

    if not ingredients:
        return data

    # Check if migration is needed
    needs_migration = any('weight_per_unit' in ing for ing in ingredients)

    if not needs_migration:
        return data

    # Create backup
    import shutil
    if DATA_FILE.exists():
        backup_path = DATA_FILE.with_suffix('.json.backup')
        shutil.copy2(DATA_FILE, backup_path)
        print(f"Created backup at {backup_path}")

    # Migrate each ingredient
    migrated_count = 0
    for ing in ingredients:
        if 'weight_per_unit' not in ing:
            continue

        unit = ing.get('unit', 'pieces')
        weight_per_unit = ing.get('weight_per_unit', 0)
        num_units = ing.get('num_units', 0)
        quantity = ing.get('quantity', weight_per_unit * num_units)

        # Determine new measurement and amount
        if unit in ['kg']:
            ing['measurement'] = 'kg'
            ing['amount'] = quantity
        elif unit in ['g']:
            ing['measurement'] = 'kg'
            ing['amount'] = quantity / 1000
        elif unit in ['l']:
            ing['measurement'] = 'liter'
            ing['amount'] = quantity
        elif unit in ['ml']:
            ing['measurement'] = 'liter'
            ing['amount'] = quantity / 1000
        else:  # pieces, cans, packages, bottles, etc.
            ing['measurement'] = 'pieces'
            ing['amount'] = num_units

        # Remove old fields
        ing.pop('unit', None)
        ing.pop('weight_per_unit', None)
        ing.pop('num_units', None)
        ing.pop('quantity', None)

        migrated_count += 1

    if migrated_count > 0:
        print(f"Migrated {migrated_count} ingredient(s) to new structure")

    # Update units to measurements
    data['units'] = ['kg', 'liter', 'pieces']

    return data


def load_data() -> Dict:
    """Load data from JSON file."""
    if not DATA_FILE.exists():
        return {
            "ingredients": [],
            "recipes": [],
            "categories": [
                "Vegetables",
                "Fruits",
                "Meat",
                "Dairy",
                "Grains",
                "Spices",
                "Beverages",
                "Canned Goods",
                "Frozen",
                "Other"
            ],
            "units": [
                "kg",
                "liter",
                "pieces"
            ]
        }

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # Migrate old data structure if needed
    original_data = json.dumps(data)
    data = migrate_ingredient_data(data)

    # Save migrated data if changes were made
    if json.dumps(data) != original_data:
        save_data(data)

    return data


def save_data(data: Dict) -> None:
    """Save data to JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


# Ingredient operations
def add_ingredient(name: str, category: str, measurement: str, amount: float) -> Dict:
    """Add a new ingredient."""
    data = load_data()

    # Generate new ID
    new_id = max([ing.get('id', 0) for ing in data['ingredients']], default=0) + 1

    ingredient = {
        'id': new_id,
        'name': name,
        'category': category,
        'measurement': measurement,
        'amount': amount
    }

    data['ingredients'].append(ingredient)
    save_data(data)
    return ingredient


def update_ingredient(ingredient_id: int, **kwargs) -> Optional[Dict]:
    """Update an existing ingredient."""
    data = load_data()

    for ingredient in data['ingredients']:
        if ingredient['id'] == ingredient_id:
            ingredient.update(kwargs)
            save_data(data)
            return ingredient

    return None


def delete_ingredient(ingredient_id: int) -> bool:
    """Delete an ingredient."""
    data = load_data()
    original_count = len(data['ingredients'])
    data['ingredients'] = [ing for ing in data['ingredients'] if ing['id'] != ingredient_id]

    if len(data['ingredients']) < original_count:
        save_data(data)
        return True
    return False


def get_ingredients(category: Optional[str] = None) -> List[Dict]:
    """Get all ingredients, optionally filtered by category."""
    data = load_data()
    ingredients = data['ingredients']

    if category:
        ingredients = [ing for ing in ingredients if ing['category'] == category]

    return ingredients


# Recipe operations
def add_recipe(name: str, comments: str, ingredients: List[Dict], vegie: str = "no", tag: str = "") -> Dict:
    """Add a new recipe (per person, grams only)."""
    data = load_data()

    # Generate new ID
    new_id = max([recipe.get('id', 0) for recipe in data['recipes']], default=0) + 1

    recipe = {
        'id': new_id,
        'name': name,
        'comments': comments,
        'ingredients': ingredients,  # [{'ingredient_id': int, 'quantity_grams': float}]
        'vegie': vegie,
        'tag': tag
    }

    data['recipes'].append(recipe)
    save_data(data)
    return recipe


def update_recipe(recipe_id: int, **kwargs) -> Optional[Dict]:
    """Update an existing recipe."""
    data = load_data()

    for recipe in data['recipes']:
        if recipe['id'] == recipe_id:
            recipe.update(kwargs)
            save_data(data)
            return recipe

    return None


def delete_recipe(recipe_id: int) -> bool:
    """Delete a recipe."""
    data = load_data()
    original_count = len(data['recipes'])
    data['recipes'] = [recipe for recipe in data['recipes'] if recipe['id'] != recipe_id]

    if len(data['recipes']) < original_count:
        save_data(data)
        return True
    return False


def get_recipes() -> List[Dict]:
    """Get all recipes."""
    data = load_data()
    return data['recipes']


def get_recipe(recipe_id: int) -> Optional[Dict]:
    """Get a specific recipe by ID."""
    data = load_data()
    for recipe in data['recipes']:
        if recipe['id'] == recipe_id:
            return recipe
    return None


# Meal planning calculations
def calculate_meal_requirements(recipe_id: int, num_people: int) -> Dict:
    """Calculate ingredient requirements for a recipe scaled to number of people."""
    data = load_data()
    recipe = get_recipe(recipe_id)

    if not recipe:
        return {'error': 'Recipe not found'}

    # Recipes are per person, so scale is just num_people
    scale = num_people

    requirements = []
    for recipe_ing in recipe['ingredients']:
        ing_id = recipe_ing['ingredient_id']
        required_qty_grams = recipe_ing['quantity_grams'] * scale

        # Find ingredient in storage
        storage_ing = next((ing for ing in data['ingredients'] if ing['id'] == ing_id), None)

        if storage_ing:
            measurement = storage_ing.get('measurement', 'pieces')
            amount = storage_ing.get('amount', 0)

            # Convert storage amount to grams for comparison
            if measurement == 'kg':
                available_qty_grams = amount * 1000
                conversion_note = f"{amount:.1f} kg"
                can_compare = True
                warning = None
            elif measurement == 'liter':
                available_qty_grams = amount * 1000
                conversion_note = f"{amount:.1f} liter (water-based estimate)"
                can_compare = True
                warning = None
            else:  # pieces
                available_qty_grams = 0
                conversion_note = f"{amount:.1f} pieces"
                can_compare = False
                warning = "Cannot auto-convert pieces to grams - manual check required"

            is_sufficient = available_qty_grams >= required_qty_grams if can_compare else False
            shortfall = max(0, required_qty_grams - available_qty_grams) if can_compare else required_qty_grams

            requirements.append({
                'ingredient_id': ing_id,
                'name': storage_ing['name'],
                'required_quantity': required_qty_grams,
                'available_quantity': available_qty_grams,
                'measurement': measurement,
                'raw_amount': amount,
                'conversion_note': conversion_note,
                'can_compare': can_compare,
                'warning': warning,
                'is_sufficient': is_sufficient,
                'shortfall': shortfall
            })

    return {
        'recipe_name': recipe['name'],
        'num_people': num_people,
        'requirements': requirements
    }


def get_categories() -> List[str]:
    """Get list of categories."""
    data = load_data()
    categories = data.get('categories', [])
    if not categories:
        categories = [
            "Vegetables",
            "Fruits",
            "Meat",
            "Dairy",
            "Grains",
            "Spices",
            "Beverages",
            "Canned Goods",
            "Frozen",
            "Other"
        ]
    return categories


def get_units() -> List[str]:
    """Get list of units."""
    data = load_data()
    units = data.get('units', [])
    if not units:
        units = [
            "pieces",
            "cans",
            "packages",
            "bottles",
            "kg",
            "g",
            "l",
            "ml"
        ]
    return units
