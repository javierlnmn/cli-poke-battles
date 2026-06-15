import pandas as pd

from repositories import MoveRepository, PokemonRepository

STAT_COLUMNS = [
    "hp",
    "attack",
    "defense",
    "special-attack",
    "special-defense",
    "speed",
]


def load_pokemon_df() -> pd.DataFrame:
    raw = PokemonRepository.load_pokemon_data()

    rows = []
    for pokemon in raw.values():
        row = {
            "id": pokemon["id"],
            "name": pokemon["name"],
            "height": pokemon["height"],
            "weight": pokemon["weight"],
            "base_experience": pokemon["base_experience"],
            "color": pokemon.get("color"),
            "types": [entry["type"]["name"] for entry in pokemon["types"]],
        }
        for entry in pokemon["stats"]:
            row[entry["stat"]["name"]] = entry["base_stat"]
        rows.append(row)

    return pd.DataFrame(rows)


def load_moves_df() -> pd.DataFrame:
    raw = MoveRepository.load_moves_data()

    rows = [
        {
            "name": move["name"],
            "type": move["type"]["name"],
            "damage_class": move["damage_class"]["name"],
            "power": move["power"],
            "accuracy": move["accuracy"],
            "pp": move["pp"],
        }
        for move in raw.values()
    ]

    return pd.DataFrame(rows)


def pokemon_type_counts(pokemon_df: pd.DataFrame) -> pd.Series:
    return pokemon_df.explode("types")["types"].value_counts()


def move_type_counts(moves_df: pd.DataFrame) -> pd.Series:
    return moves_df["type"].value_counts()
