import json

from config.config import POKEMON_DATA_FILE_PATH
from utils.general import read_file_data


def get_pokemon_data_by_name(pokemon_name):

    pokemon_data = read_file_data(POKEMON_DATA_FILE_PATH)

    for pokemon in pokemon_data:
        if pokemon == pokemon_name:
            return pokemon

    return None

def read_ascii_art(folder, pokemon):

    try:

        return open(folder + pokemon, 'r').read()

    except FileNotFoundError:
        print(f"Error: The file '{folder + pokemon}' does not exist.")

    except json.JSONDecodeError as e:
        print(f"Error: Failed decoding JSON in '{folder + pokemon}': {e}")

    return ""
