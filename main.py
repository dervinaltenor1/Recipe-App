from const import APP_ID
from const import APP_KEY
from api_functions import Api_functions
from py_edamam import Recipe
from menu import Menu


class RecipeApp(object):

    def __init__(self, recipe_app_id: str, recipe_app_key: str):
        self.recipe_app_id = recipe_app_id
        self.recipe_app_key = recipe_app_key
        self.menu_instance = Menu(self)
        self.recipe_list: list[Recipe] = []
        self.menu_instance.search_btn.config(command=self.test)
        self.iterator: int = 0
        self.count: int = 0

    def test(self) -> None:
        query: str = self.menu_instance.search_text_box.get()
        recipes = Api_functions.get_recipe(query)
        
        # Clear the previous recipe list
        self.recipe_list.clear()

        for recipe in recipes:
            self.recipe_list.append(recipe)

        if not self.recipe_list:
            self.menu_instance.load_recipe_data()
            return
        
        self.count: int = len(self.recipe_list)
        self.display_recipes(self.recipe_list)

       
    def display_recipes(self, recipe_list: list[Recipe]) -> None:

        ingredients = Api_functions.get_ingredients(recipe_list[0])

        self.menu_instance.load_recipe_data(recipe_list[0], ingredients)

    def cycle(self, direction) -> None:

        if self.recipe_list:
            self.iterator += direction
            if self.iterator >= self.count:
                self.iterator = 0
            elif self.iterator < 0:
                self.iterator = self.count -1
            
            ingredients = Api_functions.get_ingredients(self.recipe_list[self.iterator])

            self.menu_instance.load_recipe_data(self.recipe_list[self.iterator], ingredients)
        else:
            print("Cant")
                



if __name__ == "__main__":
    recipe_app = RecipeApp(APP_ID, APP_KEY)
    recipe_app.menu_instance.recipe_app_instance = recipe_app
    recipe_app.menu_instance.run_app()
    recipe_app.test()