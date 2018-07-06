from flask import Flask, render_template, redirect, url_for, request
import datetime
import json
import csv
import io
import re


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_recipe():
    if request.method == 'POST':
        # Check if both files exist
        try:
            file_ing = request.files['ingredients']
            file_rec = request.files['recipes']
        except:
            return render_template('home.html', error = "Missing file.")
        if not file_ing or not file_rec:
            return render_template('home.html', error = "Missing file.")
        # Parse files and check if both files contain valid content
        ingredients = validate_ing(file_ing)
        recipes = validate_rec(file_rec)
        if not ingredients or not recipes:
            return render_template('home.html', error = "Invalid file.")
        # Match recipes with ingredients and return one following the rules
        recipe = best_recipe(ingredients, recipes)
        return render_template('home.html', recipe = recipe)
    else:
        return render_template('home.html')


def validate_ing(file_ing):
    stream = io.StringIO(file_ing.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    ingredients = []
    for row in csv_input:
        if len(row) == 4 and row[1].isdigit() and re.search("^\d+/\d+/\d+?", row[3]):
            row[1] = int(row[1])
            row[3] = datetime.datetime.strptime(row[3], "%d/%m/%Y")
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
                if "item" in ingredient and "amount" in ingredient \
                and "unit" in ingredient:
                    recipes.append(item)
    if len(recipes) > 0:
        return recipes
    else:
        return False


def best_recipe(ingredients, recipes):
    recipe_name = "Order Takeout"
    closest_date = None
    for recipe in recipes:
        has_recipe, ingre_date = \
        validate_recipe(ingredients, recipe['ingredients'])
        if has_recipe and (closest_date == None or ingre_date < closest_date):
            closest_date = ingre_date
            recipe_name = recipe['name']
    return recipe_name


def validate_recipe(ingredients, recipe_ingres):
    today_date = datetime.datetime.today()
    has_recipe = True
    ingre_date = None
    for recipe_ingre in recipe_ingres:
        has_ingre = False
        for item in ingredients:
            if item[0] == recipe_ingre['item'] \
            and item[1] >= int(recipe_ingre['amount']) \
            and item[2] == recipe_ingre['unit'] \
            and item[3] > today_date:
                has_ingre = True
                if ingre_date == None or item[3] < ingre_date:
                    ingre_date = item[3]
                break
        if not has_ingre:
            has_recipe = False
            break
    return has_recipe, ingre_date


if __name__ == "__main__":
    app.run(debug=True)