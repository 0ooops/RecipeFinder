import sys
# go back to parent directory
sys.path.append("..")  
from recipes.main import *
import unittest


class Test(unittest.TestCase):
    # Testing method validate_recipe(ingredients, recipe_ingres)
    def test_validate_recipe(self):
        # test cases
        recipe_ingres1 = [ 
                { "item":"bread", "amount":"2", "unit":"slices"},   
                { "item":"mixed salad", "amount":"100", "unit":"grams"}   
            ]  
        recipe_ingres2 = [  
                { "item":"cheese", "amount":"2", "unit":"slices"},
                { "item":"bread", "amount":"2", "unit":"slices"}
            ]  
        recipe_ingres3 = [ 
                { "item":"bread", "amount":"20", "unit":"slices"},   
                { "item":"mixed salad", "amount":"100", "unit":"grams"}   
            ] 
        recipe_ingres4 = [ 
                { "item":"meat", "amount":"2", "unit":"slices"},
                { "item":"bread", "amount":"2", "unit":"slices"}
            ] 
        recipe_ingres5 = [ 
                { "item":"bread", "amount":"2", "unit":"grams"},   
                { "item":"mixed salad", "amount":"100", "unit":"grams"}   
            ]  
        ingredients = [
                ['bread','10','slices','25/12/2018'],
                ['cheese','10','slices','25/12/2014'],
                ['butter','250','grams','15/7/2018'],
                ['peanut butter','250','grams','11/7/2018'],
                ['mixed salad','150','grams','12/7/2018']
            ] 
        # valid recipe with valid ingredients
        has_recipe, ingre_date = validate_recipe(ingredients, recipe_ingres1)
        self.assertEqual(has_recipe, True)
        self.assertEqual(ingre_date, '12/7/2018')
        # invalid recipe with outdated ingredient
        has_recipe, ingre_date = validate_recipe(ingredients, recipe_ingres2)
        self.assertEqual(has_recipe, False)
        self.assertEqual(ingre_date, None)
        # invalid recipe without enough amount
        has_recipe, ingre_date = validate_recipe(ingredients, recipe_ingres3)
        self.assertEqual(has_recipe, False)
        self.assertEqual(ingre_date, None)
        # invalid recipe without enough ingredients
        has_recipe, ingre_date = validate_recipe(ingredients, recipe_ingres4)
        self.assertEqual(has_recipe, False)
        self.assertEqual(ingre_date, None)
        # invalid recipe with wrong unit
        has_recipe, ingre_date = validate_recipe(ingredients, recipe_ingres5)
        self.assertEqual(has_recipe, False)
        self.assertEqual(ingre_date, None)


    # Testing method best_recipe(ingredients, recipes)
    def test_best_recipe(self):
        recipes = [ 
            {  
                "name": "grilled cheese on toast", 
                "ingredients": [  
                    { "item":"bread", "amount":"2", "unit":"slices"}, 
                    { "item":"cheese", "amount":"2", "unit":"slices"}
                ]  
            }  
            ,  
            {  "name": "salad sandwich", 
                "ingredients": [ 
                    { "item":"bread", "amount":"2", "unit":"slices"},   
                    { "item":"mixed salad", "amount":"100", "unit":"grams"}   
                ]  
            }  
        ]
        ingredients1 = [
            ['bread','10','slices','25/12/2018'],
            ['cheese','10','slices','25/12/2014'],
            ['butter','250','grams','15/7/2018'],
            ['peanut butter','250','grams','11/7/2018'],
            ['mixed salad','150','grams','12/7/2018']
        ]
        ingredients2 = [
            ['bread','10','slices','25/12/2018'],
            ['cheese','10','slices','11/7/2018'],
            ['butter','250','grams','15/7/2018'],
            ['peanut butter','250','grams','31/12/2018'],
            ['mixed salad','150','grams','31/12/2018']
        ]
        ingredients3 = [
            ['bread','10','slices','2/7/2018'],
            ['cheese','10','slices','1/7/2018'],
            ['butter','250','grams','15/7/2018'],
            ['peanut butter','250','grams','3/7/2018'],
            ['mixed salad','150','grams','3/7/2018']
        ] 
        # one valid recipe and one invalid recipe, return the valid one
        recipe_name = best_recipe(ingredients1, recipes)
        self.assertEqual(recipe_name, 'salad sandwich')
        # two valid recipes return the one with the closest used-by ingredient
        recipe_name = best_recipe(ingredients2, recipes)
        self.assertEqual(recipe_name, 'grilled cheese on toast')
        # two invalid recipes return Order Takeout
        recipe_name = best_recipe(ingredients3, recipes)
        self.assertEqual(recipe_name, 'Order Takeout')


if __name__ == '__main__':
    unittest.main()