from dataclasses import dataclass
from typing import ClassVar

from config.config import POKEMON_TYPES_FILE_PATH
from schemas import NamedResourceJson, TypeJson
from utils.general import read_file_data

types_file_data = read_file_data(POKEMON_TYPES_FILE_PATH)


@dataclass(frozen=True)
class PokemonType:
    id: int
    name: str
    visible_name: str
    double_damage_from: list[str]
    double_damage_to: list[str]
    half_damage_from: list[str]
    half_damage_to: list[str]
    no_damage_from: list[str]
    no_damage_to: list[str]

    _cache: ClassVar[dict] = {}

    @classmethod
    def from_json_data(cls, data: TypeJson) -> "PokemonType":
        visible_name = None

        for lang_name in data["names"]:
            if lang_name["language"]["name"] == "en":
                visible_name = lang_name["name"]
                break

        damage_relations_data = data["damage_relations"]
        damage_relations = {}

        for damage_relation_key, damage_relation_value in damage_relations_data.items():
            names = [pokemon_type["name"] for pokemon_type in damage_relation_value]
            damage_relations[damage_relation_key] = names

        return cls(
            id=data["id"],
            name=data["name"],
            visible_name=visible_name,
            **damage_relations,
        )

    @classmethod
    def get(cls, name_id: str) -> "PokemonType":
        key = name_id.lower()

        if key not in cls._cache:
            type_data = types_file_data.get(key)
            if not type_data:
                raise ValueError(f"PokemonType '{name_id}' not found")

            cls._cache[key] = cls.from_json_data(type_data)

        return cls._cache[key]
