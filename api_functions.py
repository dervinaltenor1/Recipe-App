from const import APP_ID, APP_KEY
from py_edamam import PyEdamam, Recipe
from typing import Iterator

class Api_functions:

    @staticmethod
    def get_recipe(query: str) -> Iterator[Recipe]:

        edamam_object = PyEdamam(
            recipes_appid = APP_ID, 
            recipes_appkey = APP_KEY 
            )  
          
        query_result = edamam_object.search_recipe(query)
        
        for recipe in query_result:
            yield recipe
            
    @staticmethod
    def get_ingredients(recipe: Recipe) -> Iterator[any]:
        if recipe == None:
            print("None found")
            return
        
        for ingredient in recipe.ingredient_names:
            yield ingredient