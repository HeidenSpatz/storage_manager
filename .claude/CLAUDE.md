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
pip install streamlit openpyxl
```
- `streamlit` - Web application framework
- `openpyxl` - Excel file reading (for import scripts)

### Dev Container
Auto-configured with Python 3.11 and Streamlit. Server starts automatically on port 8501.

### Data Management
- **Reset data:** Delete `data/storage_data.json` and restart app
- **Backup data:** Copy `data/storage_data.json` to safe location
- Data file auto-generates with default categories and units on first run

## Architecture

### Application Structure
**Core Python codebase:**
- `app.py` (251 lines) - Main Streamlit UI with three pages: Ingredients, Recipes, Meal Planning
- `src/data_manager.py` (336 lines) - Data access layer with CRUD operations, meal planning logic, and data migration
- `scripts/` - Utility scripts for data import and cleaning

### Data Model (JSON-based)

**Ingredient:**
```python
{
  'id': int,                    # Auto-incremented
  'name': str,
  'category': str,              # From default categories
  'measurement': str,           # kg, liter, or pieces
  'amount': float               # Quantity in specified measurement
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

**Key Design Patterns:**
- **Simplified Inventory**: Ingredients use a single measurement (kg/liter/pieces) and amount field, replacing the previous complex multi-field system
- **Recipe Scaling**: Recipes store **per-person** quantities in grams only. Scaling happens at meal planning time
- **Smart Conversion**: Meal planning automatically converts kg/liter to grams for comparison. Pieces-based measurements show warnings requiring manual verification

### Default Data
**Categories:** Vegetables, Fruits, Meat, Dairy, Grains, Spices, Beverages, Canned Goods, Frozen, Side dish, Breakfast, Other

**Measurements:** kg, liter, pieces

### Pages & Workflows

**Ingredients Page (app.py:26-91):**
- Add ingredients with category, measurement type (kg/liter/pieces), and amount
- Display inventory with category filter
- Edit measurement type and amount inline
- Delete ingredients

**Recipes Page (app.py:105-176):**
- Create recipes with per-person gram-based ingredients
- Dynamic ingredient list (add/remove rows)
- Comments field for recipe notes
- Display all recipes in expandable sections

**Meal Planning Page (app.py:178-241):**
- Select recipe and number of people
- Immediately display scaled ingredients (per-person grams)
- Calculate requirements vs. inventory
- Automatic unit conversion (kg/liter to grams)
- Warnings for pieces (cannot auto-convert)
- Generate shopping list for missing ingredients
- Visual feedback (checkmarks for available, warnings for missing or incompatible units)

### Key Functions (data_manager.py)

**CRUD Operations:**
- `add_ingredient(name, category, measurement, amount)` - Add new ingredient
- `update_ingredient(ingredient_id, **kwargs)` - Update any ingredient fields (flexible)
- `delete_ingredient(ingredient_id)` - Remove ingredient
- `get_ingredients(category=None)` - Get all or filtered ingredients
- `add_recipe(name, comments, ingredients)` - Add new recipe
- `delete_recipe(recipe_id)` - Remove recipe
- `get_recipes()` - Get all recipes

**Meal Planning:**
- `calculate_meal_requirements(recipe_id, num_people)` - Scales recipe (grams per person), converts inventory measurements to grams, compares availability, returns detailed requirements with conversion notes and warnings

**Utilities:**
- `get_categories()` - Return category list with fallback
- `get_units()` - Return measurement types (kg, liter, pieces)

**Data Migration:**
- `migrate_ingredient_data(data)` - Automatically converts old data structure (unit/weight_per_unit/num_units) to new simplified structure (measurement/amount)

### Utility Scripts (scripts/)

**import_ingredients.py:**
- Reads ingredients from Excel file (`data/source.xlsx`)
- Processes all sheets (meal planning data)
- Deduplicates across sheets
- Maps Excel units to simplified measurements (kg/liter/pieces)
- Smart category assignment based on keywords
- Skips existing ingredients to prevent duplicates

**clean_ingredients.py:**
- Merges duplicate ingredients with typos
- Fixes category mismatches
- Standardizes ingredient names
- Re-numbers IDs sequentially
- Preserves original data (backup recommended)

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


