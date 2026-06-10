import random
import time

import clear_screen
import questionary

from config.config import (
    DEFAULT_HEALTH_BAR_LENGTH,
    POKEMON_ASCII_ART_PATH,
    POKEMON_DATA_FILE_PATH,
)
from game.entities.moves import Move, pokemon_moves
from utils.ascii_art import (
    reset_console_ansi_escapes,
    reset_console_color,
    set_console_color,
    set_console_style,
)
from utils.general import read_file_data
from utils.pokemon import read_ascii_art

pokemon_list_data = read_file_data(POKEMON_DATA_FILE_PATH)


class Pokemon:
    def __init__(self, name, visible_name, type, color, stats, moves):
        self.name = name
        self.visible_name = visible_name
        self.type = type
        self.color = color
        self.stats = stats
        self.current_hp = int(stats["hp"])
        self.current_status = None
        self.moves = [
            Move(
                move,
                pokemon_moves[move]["visible_name"],
                pokemon_moves[move]["type"],
                pokemon_moves[move]["category"],
                pokemon_moves[move]["pokemon_affected"],
                pokemon_moves[move]["accuracy"],
            )
            for move in moves
        ]
        self.status = None

    def __repr__(self) -> str:
        return str(self.name) + "\n" + str(self.type) + "\n" + str(self.moves) + "\n" + str(self.stats)

    def __str__(self) -> str:
        return (
            set_console_style("bright")
            + set_console_color(self.color)
            + self.visible_name
            + reset_console_ansi_escapes()
        )

    def get_ascii_art(self) -> str:
        return read_ascii_art(POKEMON_ASCII_ART_PATH, self.name)

    def get_ascii_art_color(self) -> str:
        ascii_art = read_ascii_art(POKEMON_ASCII_ART_PATH, self.name)
        lines = ascii_art.split("\n")
        colored_lines = [f"{set_console_color(self.color)}{line}{reset_console_color()}" for line in lines]
        return "\n".join(colored_lines)

    def get_visual_stats_sprite(self) -> str:
        max_hp = self.stats["hp"]
        current_hp = self.current_hp
        health_percentage = int(
            (current_hp / max_hp) * DEFAULT_HEALTH_BAR_LENGTH - 2
        )  # we subtract 2 from the length to add the [] characters

        health_indicator = (
            "HP: "
            + set_console_style("bright")
            + set_console_color(self.color)
            + str(current_hp)
            + reset_console_ansi_escapes()
            + " / "
            + str(max_hp)
        )

        unstyled_health_indicator = "HP: " + str(current_hp) + " / " + str(max_hp)

        health_indicator += (" ") * ((DEFAULT_HEALTH_BAR_LENGTH) - len(unstyled_health_indicator))

        health_bar = (
            set_console_color(self.color)
            + "["
            + reset_console_color()
            + "#" * health_percentage
            + "-"
            * (
                (DEFAULT_HEALTH_BAR_LENGTH - 2) - health_percentage
            )  # we subtract 2 from the length to add the [] characters
            + set_console_color(self.color)
            + "]"
            + reset_console_color()
        )

        ascii_art = self.get_ascii_art_color()

        combined_sprite = ascii_art + "\n" + health_indicator + "\n" + health_bar

        return combined_sprite

    def get_moves_visible_name_list(self) -> list:
        return [move.visible_name for move in self.moves]

    def get_move_by_visible_name(self, move_visible_name) -> Move:
        return next(
            (move for move in self.moves if move.visible_name == move_visible_name),
            None,
        )

    def pick_random_move(self) -> Move:
        return random.choice(self.moves)

    def apply_status_effect(self, battle):
        return


def user_choose_pokemon() -> Pokemon:
    pokemon_list = []

    for name in pokemon_list_data:
        pokemon_data = pokemon_list_data[name]

        pokemon = Pokemon(
            name=name,
            visible_name=pokemon_data["visible_name"],
            type=pokemon_data["type"],
            color=pokemon_data["color"],
            stats=pokemon_data["stats"],
            moves=pokemon_data["moves"],
        )

        pokemon_list.append(pokemon)

    pokemon_choose_list = [pokemon.visible_name for pokemon in pokemon_list]

    confirmed = False

    while not confirmed:
        clear_screen.clear()
        time.sleep(0.8)

        print(
            "Select a "
            + set_console_color("blue")
            + "Pokè"
            + set_console_color("yellow")
            + "mon"
            + reset_console_ansi_escapes()
            + "\n"
        )

        selected_pokemon_name = questionary.select(
            "",
            qmark="",
            choices=pokemon_choose_list,
        ).ask()

        clear_screen.clear()
        time.sleep(0.8)

        confirmed = questionary.confirm("Do you want to choose " + str(selected_pokemon_name) + "?").ask()

        if confirmed:
            selected_pokemon = next(
                pokemon for pokemon in pokemon_list if pokemon.visible_name == selected_pokemon_name
            )
            break

    return selected_pokemon


def random_pokemon() -> Pokemon:
    pokemon_list_names = list(pokemon_list_data.keys())
    pokemon_index = random.randint(0, len(pokemon_list_data) - 1)
    selected_pokemon_name = pokemon_list_names[pokemon_index]
    pokemon_data = pokemon_list_data[selected_pokemon_name]

    pokemon = Pokemon(
        name=selected_pokemon_name,
        visible_name=pokemon_data["visible_name"],
        type=pokemon_data["type"],
        color=pokemon_data["color"],
        stats=pokemon_data["stats"],
        moves=pokemon_data["moves"],
    )

    return pokemon
