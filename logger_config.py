import logging


def setup_logger() -> None:
    logging.basicConfig(
        filename = "RecipeApp.log",
        level = logging.DEBUG,
        format = "%(asctime)s - %(levelname)s - %(message)s",
        filemode = "a"
    )