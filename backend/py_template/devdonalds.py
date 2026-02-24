from collections import Counter
from dataclasses import dataclass, asdict
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re
import dacite

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	requiredItems: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cookTime: int

@dataclass
class BaseIngredient(RequiredItem):
	cookTime: int

@dataclass
class Response:
	name: str
	totalCookTime: int
	ingredients: List[RequiredItem]



# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = {}

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	# Replace - and _ with whitespace
	recipeName = re.sub(r"[_-]", " ", recipeName)

	# Remove non character including whitespace
	recipeName = re.sub(r"[^A-Za-z ]", "", recipeName)

	# Change the string to str_token to remove multiple of whitespaces
	strToken = recipeName.split()
	recipeName = " ".join(strToken)

	# Capitalise each word
	recipeName = recipeName.title()

	if len(recipeName) == 0:
		return None

	return recipeName


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	data = request.get_json()
	dataName = data.get('name')
	dataType = data.get('type')

	if dataName is None:
		return 'Invalid name provided', 400

	if dataType is None:
		return 'Invalid type provided', 400

	if dataName in cookbook:
		return 'Entry with the same name already exists', 400

	match dataType:
		case "recipe":
			# Matching the given data into Recipe class
			try:
				recipeData = dacite.from_dict(Recipe, data)
			except dacite.exceptions.DaciteError as e:
				return jsonify({'error': str(e)}), 400

			# Checking no repeated name (unique item name)
			itemName = list(item.name for item in recipeData.requiredItems)

			if len(itemName) != len(set(itemName)):
				return 'Repeated item found in the recipe', 400

			# Store the recipe in cookbook
			cookbook[dataName] = recipeData

		case "ingredient":
			# Matching the given data into Ingredient class
			try:
				ingredientData = dacite.from_dict(Ingredient, data)
			except dacite.exceptions.DaciteError as e:
				return jsonify({'error': str(e)}), 400

			# Check if the cook time is valid, return error 400 if invalid
			if ingredientData.cookTime is None:
				return 'No cook time provided for the ingredient', 400
			elif ingredientData.cookTime < 0:
				return 'Invalid cook time provided for the ingredient', 400

			# Store the ingredient in cookbook
			cookbook[dataName] = ingredientData

		case _:
			return "Invalid Entry Type Provided", 400

	return '', 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
    name = request.args.get('name')

    if not name:
        return 'Invalid name provided', 400

    recipeData = cookbook.get(name)

    if recipeData is None:
        return 'Recipe does not exist', 400

    if isinstance(recipeData, Ingredient):
        return 'It is Ingredient not a Recipe, Invalid', 400

    try:
        # Recursively flatten ingredient for this recipe
        flatIngredients = flatten_recipes(recipeData.requiredItems)
    except Exception as err:
        return str(err), 400

    # Calculate total cook time directly from the flattened list of ingredients
    totalCookTime = sum(item.quantity * item.cookTime for item in flatIngredients)

    # Aggregate quantities per ingredient using Counter
    ingredient_counts = Counter(ingredient.name for ingredient in flatIngredients)
    ingredients = [RequiredItem(ingredientName, quantity) for ingredientName, quantity in ingredient_counts.items()]

    return jsonify(Response(name, totalCookTime, ingredients)), 200

# Recursively flatten a list of required items into base ingredients, return Exception if recipe is not found
def flatten_recipes(items):
    flatIngredients = []

    for item in items:
        entry = cookbook.get(item.name)

        if entry is None:
            raise Exception("Recipe with name {} cannot be found.", item.name)

        if isinstance(entry, Recipe):
            # if found recipe, recursively flattening
            flatIngredients.extend(flatten_recipes(entry.requiredItems))

        elif isinstance(entry, Ingredient):
            # if found ingredient append to list
            flatIngredients.append(BaseIngredient(item.name, item.quantity, entry.cookTime))

    return flatIngredients


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
