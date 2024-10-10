from logger_config import setup_logger
from api_functions import Api_functions
from py_edamam import Recipe
from menu import Menu
import logging
setup_logger()


class RecipeApp:

    def __init__(self):
        """Initialize the RecipeApp with a menu instance, an empty recipe list, and counters."""
        
        self.menu_instance = Menu(self) # Create an instance of the menu class
        self.recipe_list: list[Recipe] = [] # List to store fetched recipes
        self.current_index: int = 0 # Tracks the index of the currently displayed recipe
        self.count: int = 0 # Number of recipes in the current list

    def search_recipes(self) -> None:
        """Fetch and display recipes based on the search query entered by the user."""

        # Get the search query from the UI
        query: str = self.menu_instance.search_text_box.get()

        # Exit if the query is empty
        if not query:
            return
        
        try:
            # Fetch recipes from the API using the query
            recipes = Api_functions.get_recipe(query)
        except Exception:
            return
        
        # Clear the previous recipe list
        self.recipe_list.clear()

        # Add new recipes to the recipe list and update the count
        self.recipe_list = list(recipes)
        self.count = len(self.recipe_list)

        if not self.recipe_list:
            # If no recipes are found, update the UI with an empty state or message
            self.menu_instance.load_recipe_data()
        else:
            # Display the first recipe if results are found
            self._display_recipe(0)

    def _correct_index_bounds(self, index: int) -> int:
        """Ensure the recipe index stays within valid bounds (wraps around)."""

        # Wrap to the last recipe if index is below 0
        if index < 0: return self.count -1

        # Wrap to the first recipe if index exceeds the count
        elif index >= self.count: return 0

        # Return the index if it's within valid bounds
        else: return index

    def _display_recipe(self, index: int) -> None:
        """Display the recipe at the given index, ensuring the index is valid."""

        # # Update the current index
        index = self._correct_index_bounds(index)
        self.current_index = index

        # Get the recipe for the current index
        recipe = self.recipe_list[index]

        # Fetch ingredients for the recipe
        ingredients = Api_functions.get_ingredients(recipe)

        # Update the UI with the recipe and its ingredients
        self.menu_instance.load_recipe_data(recipe, ingredients)

    def cycle(self, action) -> None:
        """Navigate between recipes based on user action ('NEXT' or 'PREVIOUS')."""

        # Exit if there are no recipes to cycle through
        if not self.recipe_list:
            logging.warning("No recipes to cycle through.")
            return
        
        if action == "NEXT":  # NEXT
            self._display_recipe(self.current_index + 1)
        elif action == "PREVIOUS":  # PREVIOUS
            self._display_recipe(self.current_index - 1)
                
    def run_app(self):
        self.menu_instance.run_app()


if __name__ == "__main__":
    recipe_app = RecipeApp()
    recipe_app.run_app()