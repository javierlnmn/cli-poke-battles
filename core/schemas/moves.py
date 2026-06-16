from typing import TypedDict

from core.schemas.common import LocalizedNameJson, NamedResourceJson


class MoveMetaJson(TypedDict):
    ailment: NamedResourceJson
    ailment_chance: int
    category: NamedResourceJson
    crit_rate: int
    drain: int
    flinch_chance: int
    healing: int
    max_hits: int | None
    max_turns: int | None
    min_hits: int | None
    min_turns: int | None
    stat_chance: int


class MoveJson(TypedDict):
    id: int
    name: str
    names: list[LocalizedNameJson]
    accuracy: int | None
    power: int | None
    pp: int | None
    priority: int
    effect_chance: int | None
    damage_class: NamedResourceJson
    type: NamedResourceJson
    target: NamedResourceJson
    generation: NamedResourceJson
    meta: MoveMetaJson
    stat_changes: list
    past_values: list
    effect_changes: list
