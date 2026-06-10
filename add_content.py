import time

import clear_screen
import questionary
from colorama import Fore

from config.config import (
    POKEMON_DATA_FILE_PATH,
    POKEMON_TYPES_FILE_PATH,
)
from utils.ascii_art import save_pokemon_ascii_art
from utils.general import add_file_data, is_positive_integer, read_file_data
from utils.pokemon import get_pokemon_data_by_name


def add_new_pokemon():
    identifyer_name, visible_name = get_name()
    pokemon_types = get_pokemon_type()
    color = get_color()
    stats = get_stats()
    ascii_art = get_ascii_art()

    time.sleep(0.5)
    cofirm_add_pokemon = questionary.confirm(
        "Do you want to add " + visible_name + " to the Pokèmon list?"
    ).ask()

    if cofirm_add_pokemon:
        pokemon_data = {
            "visible_name": visible_name,
            "type": pokemon_types,
            "color": color,
            "stats": stats,
            "moves": [],
        }

        add_file_data(POKEMON_DATA_FILE_PATH, identifyer_name, pokemon_data)
        save_pokemon_ascii_art(ascii_art, identifyer_name)

        time.sleep(0.8)
        print("\n\n\n" + visible_name + " saved.")


def get_name():
    while True:
        invalid_name = True

        while invalid_name:
            name = ""

            while not name:
                name = questionary.text("What's the Pokèmon's name?").ask()

            name_parts = name.split(" ")

            identifyer_name = ("_").join([word.lower() for word in name_parts])

            if not get_pokemon_data_by_name(identifyer_name):
                break

            print("This Pokèmon is already registered")

        visible_name = (" ").join([word.capitalize() for word in name_parts])

        print(
            "Identifyer: "
            + identifyer_name
            + "\n"
            + "Visible name: "
            + visible_name
            + "\n"
        )

        if questionary.confirm("Are these correct?").ask():
            return identifyer_name, visible_name


def get_pokemon_type():
    pokemon_type_list = read_file_data(POKEMON_TYPES_FILE_PATH)
    pokemon_type_list_formatted = [
        type.capitalize() for type in pokemon_type_list.keys()
    ]
    pokemon_types = []

    while True:
        pokemon_first_type = questionary.select(
            "What's the Pokèmon's type?", choices=pokemon_type_list_formatted
        ).ask()

        pokemon_second_type = None

        if questionary.confirm("Does the Pokèmon has a second type?").ask():
            pokemon_second_type = questionary.select(
                "What's the Pokèmon's type?", choices=pokemon_type_list_formatted
            ).ask()

        if pokemon_second_type:
            print(pokemon_first_type + ", " + pokemon_second_type)
        else:
            print(pokemon_first_type)

        confirmation = questionary.confirm("Is this correct?").ask()

        if confirmation and not pokemon_second_type:
            return [str.lower(pokemon_first_type)]

        elif confirmation and pokemon_second_type:
            return [str.lower(pokemon_first_type), str.lower(pokemon_second_type)]


def get_color():
    attributes_dict = vars(Fore)
    foreground_colors = [
        color.capitalize()
        for color in attributes_dict
        if "LIGHT" not in color and color != "RESET"
    ]

    while True:
        color = questionary.select(
            "What's the color of the Pokèmon?", choices=foreground_colors
        ).ask()

        print(color.capitalize())

        if questionary.confirm("Is this correct?").ask():
            return str.lower(color)


def get_stats():
    print("Now fill in the Pokèmon stats:")

    while True:
        hp = questionary.text("HP: ", validate=is_positive_integer).ask()
        attack = questionary.text("Attack: ", validate=is_positive_integer).ask()
        defense = questionary.text("Defense: ", validate=is_positive_integer).ask()
        sp_attack = questionary.text(
            "Special Attack: ", validate=is_positive_integer
        ).ask()
        sp_defense = questionary.text(
            "Special Defense: ", validate=is_positive_integer
        ).ask()
        speed = questionary.text("Speed: ", validate=is_positive_integer).ask()

        print(
            "HP:" + hp + "\n"
            "Attack:" + attack + "\n"
            "Defense:" + defense + "\n"
            "Special Attack:" + sp_attack + "\n"
            "Special Defense:" + sp_defense + "\n"
            "Speed:" + speed + "\n"
        )

        if questionary.confirm("Are these correct?").ask():
            stats = {
                "hp": int(hp),
                "attack": int(attack),
                "defense": int(defense),
                "sp_attack": int(sp_attack),
                "sp_defense": int(sp_defense),
                "speed": int(speed),
            }

            return stats


def get_ascii_art():
    if not questionary.confirm("Do you have the Pokèmon's ascii art?").ask():
        print(
            "It is recommended to save the Pokèmon's ascii art for the game to render the battle correctly. Please considering adding it in the future (.assets/ascii_art/pokemon_ascii/)"
        )
        return

    while True:
        pokemon_ascii_art = questionary.text(
            "Please paste the ascii art (35 lines 70 characters long recommended):"
        ).ask()

        if questionary.confirm("Is this correct?").ask():
            return pokemon_ascii_art


def add_new_move():
    pass


clear_screen.clear()

content_options = ["Add new Pokèmon", "Add new move"]

selected_option = questionary.select(
    message="What do you want to do?", choices=content_options
).ask()

if selected_option is content_options[0]:
    add_new_pokemon()
else:
    add_new_move()
