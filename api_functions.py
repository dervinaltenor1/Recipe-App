from const import APP_ID, APP_KEY
from py_edamam import PyEdamam, Recipe
from typing import Iterator
import logging

class Api_functions:

    @staticmethod
    def get_recipe(query: str) -> Iterator[Recipe]:
        """Fetch recipes matching the query using the Edamam API."""

        edamam_object = PyEdamam(
            recipes_appid = APP_ID, 
            recipes_appkey = APP_KEY 
            )  

        try:  
            query_result = edamam_object.search_recipe(query)
            logging.info(f"Fetched recipes for query: {query}")
        except Exception as e:
            logging.error(f"Error fetching recipes for query '{query}': {e}")
            return
        
        for recipe in query_result:
            yield recipe
            
    @staticmethod
    def get_ingredients(recipe: Recipe) -> Iterator[str]:
        """Fetch ingredient names from the recipe."""

        if recipe is None:
            logging.warning("No recipe provided for ingredient extraction.")
            return
        
        logging.info(f"Extracting ingredients for recipe: {recipe.label}")
        for ingredient in recipe.ingredient_names:
            yield ingredient