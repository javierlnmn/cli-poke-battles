from dataclasses import dataclass
from typing import ClassVar

from repositories import TypeRepository
from schemas import NamedResourceJson, TypeJson


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

        damage_relations = data["damage_relations"]

        return cls(
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

    @classmethod
    def get(cls, name_id: str) -> "PokemonType":
        key = name_id.lower()

        if key not in cls._cache:
            type_data = TypeRepository.get_types_data().get(key)
            if not type_data:
                raise ValueError(f"PokemonType '{name_id}' not found")

            cls._cache[key] = cls.from_json_data(type_data)

        return cls._cache[key]


def _extract_damage_relation_name(damage_relation: list[NamedResourceJson]) -> list[str]:
    return [relation_type["name"] for relation_type in damage_relation]
