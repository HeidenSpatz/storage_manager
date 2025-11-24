# Storage Manager - Specifications

**Version:** 1.0
**Date:** 2025-11-19
**Type:** Food inventory and meal planning application

## Overview

Storage Manager helps users track food inventory, manage recipes, and plan meals with automatic ingredient calculation and availability checking.

## Core Features

### 1. Ingredient Management

**Ingredient Properties:**
- Name
- Category (vegetables, fruits, meat, dairy, grains, spices, beverages, canned goods, frozen, etc.)
- Unit type (pieces, cans, packages, bottles, kilograms, grams, liters, milliliters)
- Current quantity in storage
- Minimum stock alert level (optional)

**Operations:**
- Add new ingredients
- Edit ingredient details
- Update quantity in storage
- Delete ingredients
- Filter/search by category or name

### 2. Recipe Management

**Recipe Properties:**
- Recipe ID (for sorting)
- Recipe name
- Description
- Base serving size (number of people)
- Ingredients list with quantities
- Preparation instructions (optional)
- Tags/categories (breakfast, lunch, dinner, dessert, etc.)

**Recipe Ingredients:**
- Ingredient reference
- Required quantity
- Unit

**Operations:**
- Create new recipes
- Edit recipes
- Delete recipes
- Sort recipes (by ID or drag-and-drop)
- Search/filter recipes

### 3. Meal Planning & Calculation

**Inputs:**
- Select recipe(s)
- Number of people to cook for

**Calculations:**
- Scale ingredient quantities based on number of people
- Total demand across multiple recipes
- Compare demand vs. current storage

**Output:**
- Ingredient requirements list
- Availability status (sufficient / insufficient)
- Missing quantities for shopping list

### 4. Storage Availability Check

**Functionality:**
- Compare recipe requirements against current storage
- Highlight available vs. missing ingredients
- Calculate exact shortfall amounts
- Generate shopping list for missing items

## Data Structure

### Ingredient Model
```
Ingredient {
  id: unique identifier
  name: string
  category: string (vegetables, fruits, meat, dairy, grains, etc.)
  unit: string (pieces, cans, packages, bottles, kg, g, l, ml)
  quantity: number (current stock)
  min_stock: number (optional alert threshold)
}
```

### Recipe Model
```
Recipe {
  id: unique identifier / sort order
  name: string
  description: string
  base_servings: number (people)
  ingredients: [
    {
      ingredient_id: reference
      quantity: number
      unit: string
    }
  ]
  instructions: string (optional)
  tags: [string] (optional)
}
```

### Meal Plan Model
```
MealPlan {
  recipe_id: reference
  num_people: number
  calculated_ingredients: [
    {
      ingredient_id: reference
      required_quantity: number
      available_quantity: number
      is_sufficient: boolean
      shortfall: number
    }
  ]
}
```

## User Workflows

### Workflow 1: Stock Management
1. User views ingredient inventory by category
2. User adds/updates ingredient quantities
3. System shows low-stock alerts if below minimum

### Workflow 2: Recipe Creation
1. User creates new recipe
2. User adds ingredients with quantities and units
3. User sets base serving size
4. System saves recipe with unique ID

### Workflow 3: Meal Planning
1. User selects one or more recipes
2. User specifies number of people
3. System calculates scaled ingredient requirements
4. System checks storage availability
5. System displays:
   - Available ingredients (green/checkmark)
   - Missing ingredients (red/warning)
   - Shortfall quantities
6. User can generate shopping list for missing items

### Workflow 4: Recipe Organization
1. User views recipe list
2. User sorts by:
   - ID number (manual reordering)
   - Drag and drop (if supported)
   - Name, category, date created

## Future Enhancements (Optional)

- Barcode scanning for quick ingredient entry
- Expiration date tracking
- Nutritional information
- Cost tracking and budget planning
- Meal history and favorites
- Export/import recipes
- Multi-user support
