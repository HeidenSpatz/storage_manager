import json
from pathlib import Path
from typing import Dict, List, Optional

DATA_FILE = Path(__file__).parent.parent / "data" / "storage_data.json"


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
                "pieces",
                "cans",
                "packages",
                "bottles",
                "kg",
                "g",
                "l",
                "ml"
            ]
        }

    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data: Dict) -> None:
    """Save data to JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


# Ingredient operations
def add_ingredient(name: str, category: str, unit: str, weight_per_unit: float, num_units: int) -> Dict:
    """Add a new ingredient."""
    data = load_data()

    # Generate new ID
    new_id = max([ing.get('id', 0) for ing in data['ingredients']], default=0) + 1

    ingredient = {
        'id': new_id,
        'name': name,
        'category': category,
        'unit': unit,
        'weight_per_unit': weight_per_unit,
        'num_units': num_units,
        'quantity': weight_per_unit * num_units  # Keep for backward compatibility
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
            # Recalculate quantity if weight_per_unit or num_units changed
            if 'weight_per_unit' in kwargs or 'num_units' in kwargs:
                ingredient['quantity'] = ingredient.get('weight_per_unit', 0) * ingredient.get('num_units', 0)
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
def add_recipe(name: str, comments: str, ingredients: List[Dict]) -> Dict:
    """Add a new recipe (per person, grams only)."""
    data = load_data()

    # Generate new ID
    new_id = max([recipe.get('id', 0) for recipe in data['recipes']], default=0) + 1

    recipe = {
        'id': new_id,
        'name': name,
        'comments': comments,
        'ingredients': ingredients  # [{'ingredient_id': int, 'quantity_grams': float}]
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
            available_qty = storage_ing['quantity']
            is_sufficient = available_qty >= required_qty_grams
            shortfall = max(0, required_qty_grams - available_qty)

            requirements.append({
                'ingredient_id': ing_id,
                'name': storage_ing['name'],
                'required_quantity': required_qty_grams,
                'available_quantity': available_qty,
                'unit': 'g',
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
