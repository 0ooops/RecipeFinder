from flask import Flask, render_template, redirect, url_for, request
import json
import csv
import io
import re


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    # Check if both files exist
    file_ing = request.files['ingredients']
    file_rec = request.files['recipes']
    if not file_ing or not file_rec:
        return "Missing file"  # change to redirect and error messages later
    # Parse files and check if both files contain valid content
    ingredients = validate_ing(file_ing)
    recipes = validate_rec(file_rec)
    print(ingredients)
    print(recipes)
    if not ingredients or not recipes:
        return "Invalid file" # change to redirect and error messages later
    # Match recipes with ingredients and return one following the rules
    recipe = best_recipe(ingredients, recipes)
    # return recipe # change to redirect with recipe later
    # # return redirect(url_for('home'))
    return "test"


def validate_ing(file_ing):
    stream = io.StringIO(file_ing.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    ingredients = []
    for row in csv_input:
        if len(row) == 4 and re.search("^\d+?", row[1]) 
        and re.search("^\d+/\d+/\d+?", row[3]):
            ingredients.append(row)
    if len(ingredients) > 0:
        return ingredients
    else:
        return False


def validate_rec(file_rec):
    json_input = file_rec.read()
    json_list = json.loads(json_input)
    recipes = []
    for item in json_list:
        if "name" in item and "ingredients" in item:
            for ingredient in item['ingredients']:
                if "item" in ingredient and "amount" in ingredient 
                and "unit" in ingredient:
                    recipes.append(item)
    if len(recipes) > 0:
        return recipes
    else:
        return False


def best_recipe(ingredients, recipes):
    return "Order Takeout"


if __name__ == "__main__":
    app.run(debug=True)