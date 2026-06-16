from typing import TypedDict

from core.schemas.common import LocalizedNameJson, NamedResourceJson


class DamageRelationsJson(TypedDict):
    double_damage_from: list[NamedResourceJson]
    double_damage_to: list[NamedResourceJson]
    half_damage_from: list[NamedResourceJson]
    half_damage_to: list[NamedResourceJson]
    no_damage_from: list[NamedResourceJson]
    no_damage_to: list[NamedResourceJson]


class TypeJson(TypedDict):
    id: int
    name: str
    names: list[LocalizedNameJson]
    damage_relations: DamageRelationsJson
