import tkinter as tk
import requests
import logging
from py_edamam import Recipe
from io import BytesIO
from PIL import Image, ImageTk
from const import WINDOW_TITLE, RECIPE_IMAGE_HEIGHT, RECIPE_IMAGE_WIDTH, RECIPE_WINDOW_BG_COLOR, RECIPE_INFO_BOX_COLOR, IMAGE_NOT_FOUND_URL

class Menu:
    def __init__(self, recipe_app_instance):
        """Initialize the menu UI and bind actions."""

        self.window = tk.Tk()
        self.recipe_app_instance = recipe_app_instance

        # Auto-resize based on content
        self.window.geometry("")
        self.window.configure(bg = RECIPE_WINDOW_BG_COLOR)
        self.window.resizable(False, False)
        self.window.title(WINDOW_TITLE)

        self._create_widgets()
        

    def _create_widgets(self) -> None:
        """Create and layout UI components"""

        # Search Text Box
        self.search_text_box = tk.Entry(master = self.window, width = 100)
        self.search_text_box.grid(column = 0, row = 0, padx = 5, pady = 10)

        # Search Button
        self.search_btn = tk.Button(self.window, text = "Search")
        self.search_btn.config(command=self.recipe_app_instance.search_recipes)
        self.search_btn.grid(column = 1, row = 0, padx = 5)

        # Ingredients Text Box
        self.ingredients_box = tk.Text(master = self.window, height = 15, width = 70, bg = RECIPE_INFO_BOX_COLOR, relief = tk.FLAT, font = ("Helvetica", 12))
        self.ingredients_box.grid(column = 0, row = 2, pady = 10, columnspan = 2, padx = (5,0))
        self.ingredients_box.config(state = tk.DISABLED, cursor = "arrow")
        self.ingredients_box.bind("<B1-Motion>", self._disable_highlight)
        self.ingredients_box.bind("<Double-1>", self._disable_highlight)

        # Image and Action Link Frame
        self.frame = tk.Frame(self.window, bg = RECIPE_WINDOW_BG_COLOR)
        self.frame.grid(column = 0, row = 6, columnspan = 2)

        # Action Texts
        self.next_action = self.create_action_text("NEXT")
        self.back_action = self.create_action_text("PREVIOUS")

        # Open Recipe Link Button
        self.recipe_link_btn = tk.Button(self.window, text = "Open Recipe")
        self.recipe_link_btn.config(command = lambda: self._open_link(self.recipe_url))

    def create_action_text(self, text: str):
        """Create clickable text for cycling through recipes."""

        action_text = tk.Text(self.frame, height = 1, width = 8, background = RECIPE_WINDOW_BG_COLOR, relief = tk.FLAT)
        action_text.insert(tk.END, text)
        action_text.tag_add(text, "1.0", f"1.{len(text)}")
        action_text.tag_config(text, foreground = "blue", underline = True)
        action_text.bind("<Button-1>", lambda event: self.recipe_app_instance.cycle(text))
        action_text.bind("<B1-Motion>", self._disable_highlight)
        action_text.bind("<Double-1>", self._disable_highlight)
        action_text.config(state = tk.DISABLED, cursor = "hand2")
        return action_text

    def load_recipe_data(self, recipe: Recipe = None, ingredients = None) -> None:
        """Load recipe data into the UI."""

        # Enables ingredients box to be auto filled
        self.ingredients_box.config(state = tk.NORMAL)

        # Removes previous text in ingredients box
        self.ingredients_box.delete("1.0", tk.END)

        # Displays blank if no recipe was found
        if not recipe:
            self.ingredients_box.insert(tk.END, "No recipe found for search criteria")
            self.ingredients_box.config(state = tk.DISABLED)
            self._load_image(IMAGE_NOT_FOUND_URL)
            self.recipe_url = ""
            logging.warning(f"No recipe found for search criteria: {self.search_text_box.get()}")
            return
        
        self._display_recipe_details(recipe, ingredients)
        logging.info(f"Recipe data loaded successfully for: {recipe.label}")

    def _display_recipe_details(self, recipe: Recipe, ingredients) -> None:
        """Helper method to display recipe details and ingredients."""

        # Adds each ingredient to ingredients box on a new line
        self.ingredients_box.insert(tk.END, f"\n{recipe.label}\n")
        for ingredient in ingredients:
            self.ingredients_box.insert(tk.END, f"\n{ingredient}")

        self.ingredients_box.config(state = tk.DISABLED)

        # Load the recipe image
        self._load_image(recipe.image)

        self.recipe_url = recipe.url

        # Displays action texts and open recipe button
        self.next_action.grid(column = 2, row = 0, padx = (50, 0))
        self.back_action.grid(column = 0, row = 0, padx = (0, 50))
        self.recipe_link_btn.grid(column = 0, row = 7, pady = 15, columnspan = 2)

    def _load_image(self, image_url: str) -> None:
        """Load an image from a URL and display it."""

        try:
            logging.info(f"Attempting to load image from URL: {image_url}")
            response = requests.get(image_url)
            response.raise_for_status() # Raise an exception for invalid responses
            img = Image.open(BytesIO(response.content))
            logging.info("Image loaded successfully.")

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            img = Image.open(IMAGE_NOT_FOUND_URL)

        except Exception as e:
            logging.error(f"An error occurred while loading the image: {e}")
            img = Image.open(IMAGE_NOT_FOUND_URL)

        # Ensures all images are the same size
        img = img.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)

        # Creates image box to be displayed
        image_box = tk.Label(self.frame, image = image, relief = tk.RIDGE)
        image_box.photo = image
        image_box.grid(column = 1, row = 0, columnspan = 1, pady = 20)

        
    def _open_link(self, recipe_url: str) -> None:
        """Open the recipe link in the web browser."""

        if recipe_url:
            import webbrowser
            webbrowser.open(recipe_url) 
        

    def _disable_highlight(self, event):
        """Disable text highlighting."""

        return "break"

    def run_app(self) -> None:
        self.window.mainloop()

