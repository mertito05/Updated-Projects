import json
import os

RECIPE_FILE = "recipes.json"

def load_recipes():
    """Load recipes from JSON file"""
    if os.path.exists(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as file:
            return json.load(file)
    return []

def save_recipes(recipes):
    """Save recipes to JSON file"""
    with open(RECIPE_FILE, 'w') as file:
        json.dump(recipes, file, indent=2)

def add_recipe(recipes, name, ingredients, instructions, category):
    """Add a new recipe"""
    recipe = {
        'name': name,
        'ingredients': ingredients,
        'instructions': instructions,
        'category': category
    }
    recipes.append(recipe)
    save_recipes(recipes)
    print(f"Added recipe: {name}")

def view_recipes(recipes, category=None):
    """View all recipes or filter by category"""
    if not recipes:
        print("No recipes found!")
        return
    
    filtered_recipes = recipes
    if category:
        filtered_recipes = [r for r in recipes if r['category'].lower() == category.lower()]
    
    if not filtered_recipes:
        print(f"No recipes found in category: {category}")
        return
    
    print(f"\n{'='*50}")
    print("RECIPES" + (f" - {category.upper()}" if category else ""))
    print(f"{'='*50}")
    
    for i, recipe in enumerate(filtered_recipes, 1):
        print(f"\n{i}. {recipe['name']} ({recipe['category']})")
        print(f"   Ingredients: {', '.join(recipe['ingredients'])}")
        print(f"   Instructions: {recipe['instructions'][:100]}...")

def view_recipe_detail(recipes, index):
    """View detailed information about a specific recipe"""
    if 0 <= index < len(recipes):
        recipe = recipes[index]
        print(f"\n{'='*50}")
        print(f"RECIPE: {recipe['name']}")
        print(f"{'='*50}")
        print(f"Category: {recipe['category']}")
        print("\nIngredients:")
        for ingredient in recipe['ingredients']:
            print(f"  - {ingredient}")
        print("\nInstructions:")
        print(recipe['instructions'])
    else:
        print("Invalid recipe number!")

def search_recipes(recipes, query):
    """Search recipes by name or ingredient"""
    results = []
    query = query.lower()
    
    for recipe in recipes:
        if (query in recipe['name'].lower() or 
            any(query in ingredient.lower() for ingredient in recipe['ingredients'])):
            results.append(recipe)
    
    return results

def get_categories(recipes):
    """Get all unique categories"""
    return list(set(recipe['category'] for recipe in recipes))

def main():
    """Main function"""
    recipes = load_recipes()
    
    while True:
        print("\n=== Recipe App ===")
        print("1. View all recipes")
        print("2. View recipes by category")
        print("3. Add new recipe")
        print("4. Search recipes")
        print("5. View recipe details")
        print("6. List categories")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            view_recipes(recipes)
        
        elif choice == "2":
            categories = get_categories(recipes)
            if categories:
                print("Available categories:", ", ".join(categories))
                category = input("Enter category: ").strip()
                view_recipes(recipes, category)
            else:
                print("No categories available. Add some recipes first!")
        
        elif choice == "3":
            name = input("Recipe name: ").strip()
            ingredients = input("Ingredients (comma-separated): ").strip().split(',')
            ingredients = [ing.strip() for ing in ingredients if ing.strip()]
            instructions = input("Instructions: ").strip()
            category = input("Category: ").strip()
            
            if name and ingredients and instructions and category:
                add_recipe(recipes, name, ingredients, instructions, category)
            else:
                print("All fields are required!")
        
        elif choice == "4":
            query = input("Search for recipe or ingredient: ").strip()
            if query:
                results = search_recipes(recipes, query)
                if results:
                    view_recipes(results)
                else:
                    print("No recipes found matching your search.")
            else:
                print("Please enter a search term.")
        
        elif choice == "5":
            view_recipes(recipes)
            try:
                index = int(input("Enter recipe number to view details: ")) - 1
                view_recipe_detail(recipes, index)
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "6":
            categories = get_categories(recipes)
            if categories:
                print("Available categories:", ", ".join(categories))
            else:
                print("No categories available. Add some recipes first!")
        
        elif choice == "7":
            print("Goodbye! Your recipes have been saved.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
