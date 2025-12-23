import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import data_manager as dm

# Configure for mobile/smartphone use
st.set_page_config(
    page_title="NYC 2025 Storage Manager",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Main navigation
page = st.sidebar.selectbox(
    "Navigate",
    ["Ingredients", "Recipes", "Meal Planning"]
)

st.title("NYC 2025 Storage Manager")

# ===== INGREDIENTS PAGE =====
if page == "Ingredients":
    st.header("Ingredient Inventory")

    # Add new ingredient section
    with st.expander("Add New Ingredient"):
        ing_name = st.text_input("Ingredient Name")
        ing_category = st.selectbox("Category", dm.get_categories())
        ing_measurement = st.selectbox("Measurement", ["kg", "liter", "pieces"])
        ing_amount = st.number_input("Amount", min_value=0.0, step=0.1, value=0.0)

        if st.button("Add Ingredient"):
            if ing_name:
                dm.add_ingredient(ing_name, ing_category, ing_measurement, ing_amount)
                st.success(f"Added {ing_name}!")
                st.rerun()
            else:
                st.error("Please enter an ingredient name")

    # Filter by category
    filter_category = st.selectbox("Filter by Category", ["All"] + dm.get_categories())

    # Display ingredients
    ingredients = dm.get_ingredients()

    if filter_category != "All":
        ingredients = [ing for ing in ingredients if ing['category'] == filter_category]

    if ingredients:
        for ing in sorted(ingredients, key=lambda x: x['name']):
            with st.container():
                st.write(f"**{ing['name']}** ({ing['category']})")
                st.write(f"Amount: {ing.get('amount', 0):.1f} {ing.get('measurement', 'pieces')}")

                col1, col2 = st.columns([3, 1])

                with col1:
                    new_amount = st.number_input(
                        "Amount",
                        min_value=0.0,
                        value=float(ing.get('amount', 0)),
                        step=0.1,
                        key=f"amount_{ing['id']}"
                    )
                    if new_amount != ing.get('amount', 0):
                        dm.update_ingredient(ing['id'], amount=new_amount)
                        st.rerun()

                with col2:
                    if st.button("Delete", key=f"del_{ing['id']}"):
                        dm.delete_ingredient(ing['id'])
                        st.rerun()

                st.divider()
    else:
        st.info("No ingredients yet. Add one above!")


# ===== RECIPES PAGE =====
elif page == "Recipes":
    st.header("Recipe Management")

    # Add new recipe section
    with st.expander("Add New Recipe"):
        recipe_name = st.text_input("Recipe Name")
        recipe_comments = st.text_area("Comments")

        st.subheader("Ingredients (per person, in grams)")

        # Get all ingredients for selection
        all_ingredients = dm.get_ingredients()

        if all_ingredients:
            # Simple approach: add ingredients one by one
            num_ingredients = st.number_input("Number of ingredients", min_value=1, max_value=20, value=3, step=1)

            recipe_ingredients = []
            for i in range(num_ingredients):
                col1, col2 = st.columns([3, 1])

                with col1:
                    selected_ing = st.selectbox(
                        f"Ingredient {i+1}",
                        options=all_ingredients,
                        format_func=lambda x: f"{x['name']} ({x['category']})",
                        key=f"recipe_ing_{i}"
                    )

                with col2:
                    qty_grams = st.number_input(f"Grams {i+1}", min_value=0.0, step=0.1, key=f"recipe_qty_{i}")

                if selected_ing and qty_grams > 0:
                    recipe_ingredients.append({
                        'ingredient_id': selected_ing['id'],
                        'quantity_grams': qty_grams
                    })

            if st.button("Add Recipe"):
                if recipe_name and recipe_ingredients:
                    dm.add_recipe(recipe_name, recipe_comments, recipe_ingredients)
                    st.success(f"Added recipe: {recipe_name}!")
                    st.rerun()
                else:
                    st.error("Please enter a recipe name and at least one ingredient")
        else:
            st.warning("Please add ingredients first before creating recipes")

    # Display recipes
    recipes = dm.get_recipes()

    if recipes:
        st.subheader("Your Recipes")

        for recipe in sorted(recipes, key=lambda x: x['id']):
            with st.expander(f"{recipe['name']} (per person)"):
                if recipe.get('comments'):
                    st.write(f"**Comments:** {recipe['comments']}")

                st.write("**Ingredients (per person):**")
                for ring in recipe['ingredients']:
                    ing = next((i for i in all_ingredients if i['id'] == ring['ingredient_id']), None)
                    if ing:
                        st.write(f"- {ring['quantity_grams']}g {ing['name']}")

                if st.button("Delete Recipe", key=f"del_recipe_{recipe['id']}"):
                    dm.delete_recipe(recipe['id'])
                    st.rerun()
    else:
        st.info("No recipes yet. Add one above!")


# ===== MEAL PLANNING PAGE =====
elif page == "Meal Planning":
    st.header("Meal Planning")

    recipes = dm.get_recipes()

    if recipes:
        # Select recipe
        selected_recipe = st.selectbox(
            "Select Recipe",
            options=recipes,
            format_func=lambda x: f"{x['name']} (per person)"
        )

        # Number of people
        num_people = st.number_input(
            "Number of People",
            min_value=1,
            value=1,
            step=1
        )

        # Display ingredients for selected recipe
        st.subheader(f"{selected_recipe['name']} - Ingredients")
        all_ingredients = dm.get_ingredients()

        st.write(f"**For {num_people} {'person' if num_people == 1 else 'people'}:**")
        for recipe_ing in selected_recipe['ingredients']:
            ing = next((i for i in all_ingredients if i['id'] == recipe_ing['ingredient_id']), None)
            if ing:
                total_grams = recipe_ing['quantity_grams'] * num_people
                st.write(f"- {total_grams:.1f}g {ing['name']}")

        st.divider()

        if st.button("Calculate Requirements"):
            result = dm.calculate_meal_requirements(selected_recipe['id'], num_people)

            st.subheader(f"{result['recipe_name']} for {result['num_people']} people")

            # Display requirements
            st.write("**Ingredient Check:**")

            available = []
            warnings = []
            missing = []

            for req in result['requirements']:
                if req.get('warning'):
                    warnings.append(req)
                elif req['is_sufficient']:
                    available.append(req)
                else:
                    missing.append(req)

            # Available ingredients
            if available:
                st.success(f"Available ({len(available)} items)")
                for req in available:
                    st.write(f"✓ {req['name']}: {req['conversion_note']} available")
                    st.write(f"  Recipe needs: {req['required_quantity']:.1f}g")

            # Warnings for ingredients that can't be auto-converted
            if warnings:
                st.warning(f"Manual Check Required ({len(warnings)} items)")
                for req in warnings:
                    st.write(f"⚠️ {req['name']}: {req['warning']}")
                    st.write(f"  Recipe needs: {req['required_quantity']:.1f}g")
                    st.write(f"  You have: {req['conversion_note']}")

            # Missing ingredients
            if missing:
                st.error(f"Missing or Insufficient ({len(missing)} items)")
                st.write("**Shopping List:**")
                for req in missing:
                    st.write(f"⚠️ {req['name']}: Need {req['shortfall']:.1f}g more")
                    st.write(f"  Available: {req['conversion_note']}")
                    st.write(f"  Required: {req['required_quantity']:.1f}g")

            if not missing and not warnings:
                st.balloons()
                st.success("You have all ingredients! Ready to cook!")

    else:
        st.info("No recipes available. Create recipes first!")
