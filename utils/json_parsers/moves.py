from game.pokemon.moves import MoveMeta, PokemonMoveData


def parse_move_json_data(data) -> PokemonMoveData:
    visible_name = None

    for lang_name in data["names"]:
        if lang_name["language"]["name"] == "en":
            visible_name = lang_name["name"]
            break

    meta = data["meta"]

    return PokemonMoveData(
        id=data["id"],
        name=data["name"],
        visible_name=visible_name,
        type=data["type"]["name"],
        damage_class=data["damage_class"]["name"],
        power=data["power"],
        accuracy=data["accuracy"],
        pp=data["pp"],
        priority=data["priority"],
        effect_chance=data["effect_chance"],
        target=data["target"]["name"],
        generation=data["generation"]["name"],
        meta=MoveMeta(
            ailment=meta["ailment"]["name"],
            ailment_chance=meta["ailment_chance"],
            category=meta["category"]["name"],
            crit_rate=meta["crit_rate"],
            drain=meta["drain"],
            flinch_chance=meta["flinch_chance"],
            healing=meta["healing"],
            max_hits=meta["max_hits"],
            max_turns=meta["max_turns"],
            min_hits=meta["min_hits"],
            min_turns=meta["min_turns"],
            stat_chance=meta["stat_chance"],
        ),
        stat_changes=data["stat_changes"],
        past_values=data["past_values"],
        effect_changes=data["effect_changes"],
    )
