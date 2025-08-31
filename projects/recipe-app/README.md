# Recipe App

A command-line recipe management application that allows users to store, organize, and search through their favorite recipes. This application uses JSON for data storage and provides a simple interface for managing recipes.

## Features
- **Add Recipes**: Create new recipes with name, ingredients, instructions, and category
- **View Recipes**: Browse all recipes or filter by category
- **Search Recipes**: Search for recipes by name or ingredient
- **Recipe Details**: View detailed information about specific recipes
- **Category Management**: Organize recipes into categories
- **Persistent Storage**: All recipes are saved to a JSON file

## Prerequisites
- Python 3.x
- No additional packages required (uses standard library only)

## How to Run
```bash
python main.py
```

## Usage
1. Start the application by running `main.py`.
2. Use the menu options to manage your recipes:
   - **View all recipes**: See all stored recipes
   - **View by category**: Filter recipes by specific categories
   - **Add new recipe**: Create a new recipe entry
   - **Search recipes**: Find recipes by name or ingredient
   - **View recipe details**: See complete recipe information
   - **List categories**: View all available categories

## Example
```
# Add a new recipe
Recipe name: Chocolate Chip Cookies
Ingredients: flour, sugar, butter, chocolate chips, eggs
Instructions: Mix ingredients and bake at 350°F for 12 minutes
Category: Desserts

# Search for recipes
Search for recipe or ingredient: chocolate
```

## File Structure
- `main.py` - Main application code
- `recipes.json` - Data storage file (created automatically)

## Data Format
Recipes are stored in JSON format with the following structure:
```json
[
  {
    "name": "Recipe Name",
    "ingredients": ["ingredient1", "ingredient2"],
    "instructions": "Step-by-step instructions",
    "category": "Category Name"
  }
]
```

## Customization
You can extend the application by:
- Adding recipe ratings and reviews
- Implementing meal planning features
- Adding nutritional information
- Including cooking time and difficulty level
- Implementing a web interface
- Adding image support for recipes

## Security Considerations
- This application stores data locally in JSON format
- No sensitive data is handled by default
- For personal recipe collections only

## Troubleshooting
- Ensure you have write permissions for the current directory
- Check that the JSON file is not corrupted if issues occur
- Verify that all required fields are provided when adding recipes

## Note
This project is intended for educational purposes and personal use. It can be expanded with additional features for more comprehensive recipe management.
