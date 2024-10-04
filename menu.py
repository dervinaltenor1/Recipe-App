import tkinter as tk
import requests
from py_edamam import Recipe
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import messagebox
from const import WINDOW_TITLE, RECIPE_IMAGE_HEIGHT, RECIPE_IMAGE_WIDTH, RECIPE_WINDOW_BG_COLOR, RECIPE_INFO_BOX_COLOR, IMAGE_NOT_FOUND_URL

class Menu:
    def __init__(self, recipe_app_instance):
        self.window = tk.Tk()

        self.recipe_app_instance: recipe_app_instance

        self.window.geometry("")
        self.window.configure(bg = RECIPE_WINDOW_BG_COLOR)
        self.window.title(WINDOW_TITLE)

        self.search_text_box = tk.Entry(master = self.window, width = 100)
        self.search_text_box.grid(column = 0, row = 0, padx = 5, pady = 10)

        self.search_btn = tk.Button(self.window, text = "Search")
        self.search_btn.grid(column = 1, row = 0, padx = 5, )

        self.test = tk.ANCHOR

        self.ingredients_box = tk.Text(master = self.window, height = 15, width = 70, bg = RECIPE_INFO_BOX_COLOR, relief = tk.FLAT, font = ("Helvetica", 12))
        self.ingredients_box.grid(column = 0, row = 2, pady = 10, columnspan = 2)


        self.next_action = tk.Text(self.window, height = 1, width = 11, background = RECIPE_WINDOW_BG_COLOR, relief=tk.FLAT)

        self.next_action.insert(tk.END, "Next recipe")
        self.next_action.tag_add("link", "1.0", "1.11")
        self.next_action.tag_config("link", foreground = "blue", underline= True)
        self.next_action.bind("<Button-1>", self.on_click)
        self.next_action.bind("<B1-Motion>", self.disable_highlight)
        self.next_action.bind("<Double-1>", self.disable_highlight)

        self.next_action.config(state= tk.DISABLED, cursor="hand2")


    def load_recipe_data(self, recipe: Recipe = None, ingredients = None) -> None:
        self.ingredients_box.delete("1.0", tk.END)

        if not recipe:
            self.ingredients_box.insert(tk.END, "No recipe found for search criteria")
            image = self.get_image(recipe)
            self.load_image(image)
            return
        
        self.ingredients_box.insert(tk.END, "\n" + recipe.label + "\n")
        for ingredient in ingredients:
            self.ingredients_box.insert(tk.END, "\n" + ingredient)

        image = self.get_image(recipe)
        self.load_image(image)
        self.next_action.grid(column = 1, row = 6)

    def load_image(self, image_url: str) -> None:
        response = requests.get(image_url)

        img = Image.open(BytesIO(response.content))
        img = img.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT), Image.Resampling.LANCZOS)

        image = ImageTk.PhotoImage(img)

        image_box = tk.Label(self.window, image = image, relief = tk.RIDGE)
        image_box.photo = image
        image_box.grid(column = 0, row = 6, pady = 10, columnspan = 2)


    def on_click(self, event):
        # Get the current position of the click
        index = self.next_action.index("@%s,%s" % (event.x, event.y))

        # Check if the click is within the link range
        link_ranges = self.next_action.tag_ranges("link")  # Get the start and end indices for the "link" tag
        
        if link_ranges:  # Ensure there are ranges defined for the tag
            start, end = link_ranges[0], link_ranges[1]  # Get start and end of the tag range

            # Convert Tcl_Obj to string for comparison
            index_str = str(index)
            start_str = str(start)
            end_str = str(end)

            # Check if the click index is within the link range using string comparison
            if start_str <= index_str or index_str <= end_str:
                self.recipe_app_instance.cycle()


    def get_image(self, recipe: Recipe) -> str:
        if recipe:
            return recipe.image
        else:
            return IMAGE_NOT_FOUND_URL
        
    def disable_highlight(self, event):
        return "break"  # Prevents the default behavior of selecting text

    def run_app(self) -> None:
        self.window.mainloop()

