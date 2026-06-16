from typing import ClassVar

from core.config import POKEMON_TYPES_FILE_PATH
from core.entities.types import PokemonType
from core.schemas import NamedResourceJson, TypeJson
from core.utils.files import read_file_data_json


class TypeRepository:
    _types_data: ClassVar[dict[str, TypeJson] | None] = None
    _types: ClassVar[dict[str, PokemonType]] = {}

    @classmethod
    def load_types_data(cls) -> dict[str, TypeJson]:
        if cls._types_data is None:
            cls._types_data = read_file_data_json(POKEMON_TYPES_FILE_PATH)
        return cls._types_data

    @classmethod
    def get_types(cls) -> list[PokemonType]:
        return [cls.get(key) for key in cls.load_types_data()]

    @classmethod
    def get(cls, name_id: str) -> PokemonType:
        key = name_id.lower()

        if key not in cls._types:
            type_data = cls.load_types_data().get(key)
            if not type_data:
                raise ValueError(f"PokemonType '{name_id}' not found")

            cls._types[key] = cls._build(type_data)

        return cls._types[key]

    @classmethod
    def clear_cache(cls) -> None:
        cls._types_data = None
        cls._types = {}

    @staticmethod
    def _build(data: TypeJson) -> PokemonType:
        visible_name = None

        for lang_name in data["names"]:
            if lang_name["language"]["name"] == "en":
                visible_name = lang_name["name"]
                break

        damage_relations = data["damage_relations"]

        return PokemonType(
            id=data["id"],
            name=data["name"],
            visible_name=visible_name,
            double_damage_from=_extract_damage_relation_name(damage_relations["double_damage_from"]),
            double_damage_to=_extract_damage_relation_name(damage_relations["double_damage_to"]),
            half_damage_from=_extract_damage_relation_name(damage_relations["half_damage_from"]),
            half_damage_to=_extract_damage_relation_name(damage_relations["half_damage_to"]),
            no_damage_from=_extract_damage_relation_name(damage_relations["no_damage_from"]),
            no_damage_to=_extract_damage_relation_name(damage_relations["no_damage_to"]),
        )


def _extract_damage_relation_name(damage_relation: list[NamedResourceJson]) -> list[str]:
    return [relation_type["name"] for relation_type in damage_relation]
