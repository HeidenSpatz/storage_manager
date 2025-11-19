import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import data_manager as dm

# Configure for mobile/smartphone use
st.set_page_config(
    page_title="Storage Manager",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Main navigation
page = st.sidebar.selectbox(
    "Navigate",
    ["Ingredients", "Recipes", "Meal Planning"]
)

st.title("Storage Manager")

# ===== INGREDIENTS PAGE =====
if page == "Ingredients":
    st.header("Ingredient Inventory")

    # Add new ingredient section
    with st.expander("Add New Ingredient"):
        col1, col2 = st.columns(2)

        with col1:
            ing_name = st.text_input("Ingredient Name")
            ing_category = st.selectbox("Category", dm.get_categories())
            ing_unit = st.selectbox("Unit", dm.get_units())

        with col2:
            ing_quantity = st.number_input("Quantity", min_value=0.0, step=0.1)
            ing_min_stock = st.number_input("Min Stock Alert", min_value=0.0, step=0.1)

        if st.button("Add Ingredient"):
            if ing_name:
                dm.add_ingredient(ing_name, ing_category, ing_unit, ing_quantity, ing_min_stock)
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
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

                with col1:
                    st.write(f"**{ing['name']}** ({ing['category']})")

                with col2:
                    # Update quantity
                    new_qty = st.number_input(
                        "Qty",
                        min_value=0.0,
                        value=float(ing['quantity']),
                        step=0.1,
                        key=f"qty_{ing['id']}",
                        label_visibility="collapsed"
                    )
                    if new_qty != ing['quantity']:
                        dm.update_ingredient(ing['id'], quantity=new_qty)

                with col3:
                    st.write(f"{ing['quantity']} {ing['unit']}")

                    # Low stock warning
                    if ing['min_stock'] > 0 and ing['quantity'] < ing['min_stock']:
                        st.warning("Low stock!")

                with col4:
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
        recipe_desc = st.text_area("Description")
        recipe_servings = st.number_input("Base Servings (people)", min_value=1, value=4, step=1)

        st.subheader("Ingredients")

        # Get all ingredients for selection
        all_ingredients = dm.get_ingredients()

        if all_ingredients:
            # Simple approach: add ingredients one by one
            num_ingredients = st.number_input("Number of ingredients", min_value=1, max_value=20, value=3, step=1)

            recipe_ingredients = []
            for i in range(num_ingredients):
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    selected_ing = st.selectbox(
                        f"Ingredient {i+1}",
                        options=all_ingredients,
                        format_func=lambda x: f"{x['name']} ({x['category']})",
                        key=f"recipe_ing_{i}"
                    )

                with col2:
                    qty = st.number_input(f"Qty {i+1}", min_value=0.0, step=0.1, key=f"recipe_qty_{i}")

                with col3:
                    unit = st.selectbox(f"Unit {i+1}", dm.get_units(), key=f"recipe_unit_{i}")

                if selected_ing and qty > 0:
                    recipe_ingredients.append({
                        'ingredient_id': selected_ing['id'],
                        'quantity': qty,
                        'unit': unit
                    })

            recipe_instructions = st.text_area("Instructions (optional)")

            if st.button("Add Recipe"):
                if recipe_name and recipe_ingredients:
                    dm.add_recipe(recipe_name, recipe_desc, recipe_servings, recipe_ingredients, recipe_instructions)
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
            with st.expander(f"{recipe['name']} (Serves {recipe['base_servings']})"):
                st.write(f"**Description:** {recipe['description']}")

                st.write("**Ingredients:**")
                for ring in recipe['ingredients']:
                    ing = next((i for i in all_ingredients if i['id'] == ring['ingredient_id']), None)
                    if ing:
                        st.write(f"- {ring['quantity']} {ring['unit']} {ing['name']}")

                if recipe.get('instructions'):
                    st.write(f"**Instructions:** {recipe['instructions']}")

                if st.button("Delete Recipe", key=f"del_recipe_{recipe['id']}"):
                    dm.delete_recipe(recipe['id'])
                    st.rerun()
    else:
        st.info("No recipes yet. Add one above!")


# ===== MEAL PLANNING PAGE =====
elif page == "Meal Planning":
    st.header("Meal Planning & Shopping List")

    recipes = dm.get_recipes()

    if recipes:
        # Select recipe
        selected_recipe = st.selectbox(
            "Select Recipe",
            options=recipes,
            format_func=lambda x: f"{x['name']} (Serves {x['base_servings']})"
        )

        # Number of people
        num_people = st.number_input(
            "Number of People",
            min_value=1,
            value=selected_recipe['base_servings'],
            step=1
        )

        if st.button("Calculate Requirements"):
            result = dm.calculate_meal_requirements(selected_recipe['id'], num_people)

            st.subheader(f"{result['recipe_name']} for {result['num_people']} people")

            # Display requirements
            st.write("**Ingredient Check:**")

            available = []
            missing = []

            for req in result['requirements']:
                if req['is_sufficient']:
                    available.append(req)
                else:
                    missing.append(req)

            # Available ingredients
            if available:
                st.success(f"Available ({len(available)} items)")
                for req in available:
                    st.write(f"✓ {req['name']}: {req['required_quantity']:.1f} {req['unit']} (have {req['available_quantity']:.1f})")

            # Missing ingredients
            if missing:
                st.error(f"Missing or Insufficient ({len(missing)} items)")
                st.write("**Shopping List:**")
                for req in missing:
                    st.write(f"⚠ {req['name']}: Need {req['shortfall']:.1f} {req['unit']} more (have {req['available_quantity']:.1f}, need {req['required_quantity']:.1f})")
            else:
                st.balloons()
                st.success("You have all ingredients! Ready to cook!")

    else:
        st.info("No recipes available. Create recipes first!")
