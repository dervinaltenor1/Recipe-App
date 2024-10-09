import tkinter as tk
import requests
from py_edamam import Recipe
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import messagebox
import webbrowser
from const import WINDOW_TITLE, RECIPE_IMAGE_HEIGHT, RECIPE_IMAGE_WIDTH, RECIPE_WINDOW_BG_COLOR, RECIPE_INFO_BOX_COLOR, IMAGE_NOT_FOUND_URL

class Menu:
    def __init__(self, recipe_app_instance):
        self.recipe_url = ""
        self.window = tk.Tk()

        self.recipe_app_instance = recipe_app_instance

        self.window.geometry("")
        self.window.configure(bg = RECIPE_WINDOW_BG_COLOR)
        self.window.title(WINDOW_TITLE)

        self.search_text_box = tk.Entry(master = self.window, width = 100)
        self.search_text_box.grid(column = 0, row = 0, padx = 5, pady = 10)

        self.search_btn = tk.Button(self.window, text = "Search")
        self.search_btn.grid(column = 1, row = 0, padx = 5)

        self.recipe_link_btn = tk.Button(self.window, text = "Open Recipe")
        self.recipe_link_btn.config(command = lambda: self.open_link(self.recipe_url))
        

        self.frame = tk.Frame(self.window, bg = RECIPE_WINDOW_BG_COLOR)
        self.frame.grid(column = 0, row = 6, columnspan = 2)

        self.ingredients_box = tk.Text(master = self.window, height = 15, width = 70, bg = RECIPE_INFO_BOX_COLOR, relief = tk.FLAT, font = ("Helvetica", 12))
        self.ingredients_box.grid(column = 0, row = 2, pady = 10, columnspan = 2, padx = (5,0))
        self.ingredients_box.config(state = tk.DISABLED, cursor = "arrow")
        self.ingredients_box.bind("<B1-Motion>", self.disable_highlight)
        self.ingredients_box.bind("<Double-1>", self.disable_highlight)

        self.next_action = tk.Text(self.frame, height = 1, width = 4, background = RECIPE_WINDOW_BG_COLOR, relief = tk.FLAT)
        self.next_action.insert(tk.END, "NEXT")
        self.next_action.tag_add("link1", "1.0", "1.4")
        self.next_action.tag_config("link1", foreground = "blue", underline = True)
        self.next_action.bind("<Button-1>", lambda event: self.on_click(event, link_name = "link1", action_type = self.next_action))
        self.next_action.bind("<B1-Motion>", self.disable_highlight)
        self.next_action.bind("<Double-1>", self.disable_highlight)
        self.next_action.config(state = tk.DISABLED, cursor = "hand2")

        self.back_action = tk.Text(self.frame, height = 1, width = 8, background = RECIPE_WINDOW_BG_COLOR, relief = tk.FLAT)
        self.back_action.insert(tk.END, "PREVIOUS")
        self.back_action.tag_add("link2", "1.0", "1.8")
        self.back_action.tag_config("link2", foreground = "blue", underline = True)
        self.back_action.bind("<Button-1>", lambda event: self.on_click(event, link_name = "link2", action_type = self.back_action))
        self.back_action.bind("<B1-Motion>", self.disable_highlight)
        self.back_action.bind("<Double-1>", self.disable_highlight)
        self.back_action.config(state = tk.DISABLED, cursor = "hand2")



    def load_recipe_data(self, recipe: Recipe = None, ingredients = None) -> None:
        self.ingredients_box.config(state = tk.NORMAL)
        self.ingredients_box.delete("1.0", tk.END)

        if not recipe:
            self.ingredients_box.insert(tk.END, "No recipe found for search criteria")
            image = IMAGE_NOT_FOUND_URL
            self.load_image(image)
            self.recipe_url = ""
            return
        
        self.ingredients_box.insert(tk.END, "\n" + recipe.label + "\n")
        for ingredient in ingredients:
            self.ingredients_box.insert(tk.END, "\n" + ingredient)

        self.ingredients_box.config(state = tk.DISABLED)

        image = self.get_image(recipe)
        self.load_image(image)

        self.recipe_url = self.get_url(recipe)

    def load_image(self, image_url: str) -> None:
        response = requests.get(image_url)

        img = Image.open(BytesIO(response.content))
        img = img.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT), Image.Resampling.LANCZOS)

        image = ImageTk.PhotoImage(img)

        image_box = tk.Label(self.frame, image = image, relief = tk.RIDGE)
        image_box.photo = image
        image_box.grid(column = 1, row = 0, columnspan = 1, pady = 20)

        self.next_action.grid(column = 2, row = 0, padx = (50, 0))
        self.back_action.grid(column = 0, row = 0, padx = (0, 50))

        self.recipe_link_btn.grid(column = 0, row = 7, pady = 15, columnspan = 2)

        
    def open_link(self, recipe_url) -> None:
        if recipe_url:
            import webbrowser
            webbrowser.open(recipe_url)
        else:
            print("none available")

    def on_click(self, event, link_name: str, action_type):

        click_pos = "@%s,%s" % (event.x, event.y)


        try:
            index = action_type.index(click_pos)
            link_ranges = action_type.tag_ranges(link_name)

            if not link_ranges:
                return
            
            start, end = link_ranges[0], link_ranges[1]

            # Convert Tcl_Obj to string for comparison
            index_str = str(index)
            start_str = str(start)
            end_str = str(end)

            if start_str <= index_str or index_str <= end_str:
                if link_name == "link1":
                    direction: int = 1
                elif link_name == "link2":
                    direction: int = -1

                self.recipe_app_instance.cycle(direction)

        except ValueError:
            print("I SUCK")


    def get_image(self, recipe: Recipe) -> str:
        if recipe:
            return recipe.image
        else:
            return IMAGE_NOT_FOUND_URL

    def get_url(self, recipe: Recipe) -> str:
        if recipe:
            return recipe.url
        else:
            return ""   
        

    def disable_highlight(self, event):
        return "break"  # Prevents the default behavior of selecting text

    def run_app(self) -> None:
        self.window.mainloop()

