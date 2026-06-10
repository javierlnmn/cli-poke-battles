from game.pokemon.types import PokemonTypeData


def parse_type_json_data(data) -> PokemonTypeData:
    visible_name = None

    for lang_name in data["names"]:
        if lang_name["language"]["name"] == "en":
            visible_name = lang_name["name"]

    damage_relations = data["damage_relations"]

    return PokemonTypeData(
        visible_name=visible_name,
        double_damage_from=_extract_damage_relation_name(damage_relations["double_damage_from"]),
        double_damage_to=_extract_damage_relation_name(damage_relations["double_damage_to"]),
        half_damage_from=_extract_damage_relation_name(damage_relations["half_damage_from"]),
        half_damage_to=_extract_damage_relation_name(damage_relations["half_damage_to"]),
        no_damage_from=_extract_damage_relation_name(damage_relations["no_damage_from"]),
        no_damage_to=_extract_damage_relation_name(damage_relations["no_damage_to"]),
    )


def _extract_damage_relation_name(damage_relation) -> list[str]:
    types = []
    for relation_type in damage_relation:
        types.append(relation_type["name"])
    return types
