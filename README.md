# Storage Manager

A mobile-friendly Streamlit application for managing food inventory, recipes, and meal planning.

## Features

- **Ingredient Inventory**: Track food items with quantities, categories, and units
- **Recipe Management**: Create and store recipes with ingredient lists
- **Meal Planning**: Calculate ingredient requirements and check storage availability
- **Shopping Lists**: Automatically generate shopping lists for missing ingredients
- **Mobile Optimized**: Designed for smartphone use

## Quick Start

1. Install dependencies:
```bash
pip install streamlit
```

2. Run the app:
```bash
streamlit run app.py
```

3. Access on your phone:
   - Open the External URL shown in terminal
   - Or deploy to Streamlit Cloud for permanent access

## Usage

### Ingredients Page
- Add new ingredients with name, category, unit, and quantity
- Update quantities as you use or restock items
- Filter by category
- Set minimum stock alerts for low inventory warnings

### Recipes Page
- Create recipes with ingredients and serving sizes
- Specify quantities for each ingredient
- View all your saved recipes
- Delete recipes you no longer need

### Meal Planning Page
- Select a recipe
- Specify number of people
- Calculate scaled ingredient requirements
- See what you have and what you need to buy
- Get automatic shopping list for missing items

## Data Storage

All data is stored in `data/storage_data.json` (excluded from Git).

To reset data, delete the file and restart the app. It will regenerate from the template.

## Deployment to Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repository
4. Deploy!

Changes pushed to GitHub will automatically redeploy.
