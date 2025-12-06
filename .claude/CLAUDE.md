# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Date:** 2025-11-19
**Version:** 1.1
**Author:** uweli

## Guide References

See `.claude/guides/` for detailed guidance:
- **GUIDE_DOCS.md** - Documentation standards and file structure
- **GUIDE_PROJECT.md** - Project principles and token efficiency
- **GUIDE_TODO.md** - Todo file naming, structure, and writing standards

## Project Overview

Storage Manager (branded "Lunas Storage") - A mobile-optimized Streamlit application for managing food inventory, recipes, and meal planning.

**Technology Stack:**
- Python 3.11 + Streamlit framework
- JSON file-based data storage (no database required)
- Mobile-first responsive design

## Development Commands

### Run Application
```bash
streamlit run app.py
```
Access at http://localhost:8501 (auto-opens in browser)

### Install Dependencies
```bash
pip install streamlit
```

### Dev Container
Auto-configured with Python 3.11 and Streamlit. Server starts automatically on port 8501.

### Data Management
- **Reset data:** Delete `data/storage_data.json` and restart app
- **Backup data:** Copy `data/storage_data.json` to safe location
- Data file auto-generates with default categories and units on first run

## Architecture

### Application Structure
**Two-file Python codebase:**
- `app.py` (248 lines) - Main Streamlit UI with three pages: Ingredients, Recipes, Meal Planning
- `src/data_manager.py` (249 lines) - Data access layer with CRUD operations and meal planning logic

### Data Model (JSON-based)

**Ingredient:**
```python
{
  'id': int,                    # Auto-incremented
  'name': str,
  'category': str,              # From default categories
  'unit': str,                  # From default units
  'weight_per_unit': float,     # Weight of one unit
  'num_units': int,             # Number of units in stock
  'quantity': float             # Calculated: weight_per_unit × num_units
}
```

**Recipe:**
```python
{
  'id': int,
  'name': str,
  'comments': str,              # Recipe notes/description
  'ingredients': [
    {
      'ingredient_id': int,
      'quantity_grams': float   # Grams per person (not total!)
    }
  ]
}
```

**Key Design Pattern:** Recipes store **per-person** quantities in grams only. Scaling happens at meal planning time.

### Default Data
**Categories:** Vegetables, Fruits, Meat, Dairy, Grains, Spices, Beverages, Canned Goods, Frozen, Other

**Units:** pieces, cans, packages, bottles, kg, g, l, ml

### Pages & Workflows

**Ingredients Page (app.py:26-103):**
- Add ingredients with category, unit, weight per unit, number of units
- Display inventory with category filter
- Update quantities inline
- Total quantity auto-calculated

**Recipes Page (app.py:105-176):**
- Create recipes with per-person gram-based ingredients
- Dynamic ingredient list (add/remove rows)
- Comments field for recipe notes
- Display all recipes in expandable sections

**Meal Planning Page (app.py:178-248):**
- Select recipe and number of people
- Immediately display scaled ingredients (non-calculated mode)
- Calculate requirements vs. inventory
- Generate shopping list for missing ingredients
- Visual feedback (checkmarks for available, warnings for missing)

### Key Functions (data_manager.py)

**CRUD Operations:**
- `add_ingredient()`, `update_ingredient_quantity()`, `delete_ingredient()`, `get_all_ingredients()`
- `add_recipe()`, `delete_recipe()`, `get_all_recipes()`

**Meal Planning:**
- `calculate_meal_plan(recipe_id, num_people)` - Scales recipe, compares with inventory, returns requirements and availability

**Utilities:**
- `get_categories()`, `get_units()` - Return defaults with fallback handling

## Project Principles

### Token Efficiency
- Keep files and file lengths minimal
- Every element has a cost - maintain only what's essential
- **Archive folder:** Non-essential materials go to `/archive`. Ignore this folder unless explicitly requested
- **Completed todos:** Finished todo files go to `/todo/done`. Ignore this folder to focus on active tasks

### Version Control
- Project uses Git version control
- JSON data files (`data/*.json`) are excluded from Git
- All source code, config templates, and documentation are tracked

### Git Commit Guidelines

**Commit Message Structure:**
```
Brief imperative description
```

**Don't add:**
- Emoji or AI attribution
- "Generated with Claude Code" footer
- Co-authored tags


