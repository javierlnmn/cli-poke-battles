from dataclasses import dataclass
from typing import TypedDict

from core.schemas.common import NamedResourceJson


class PokemonStatJson(TypedDict):
    base_stat: int
    effort: int
    stat: NamedResourceJson


class PokemonTypeSlotJson(TypedDict):
    slot: int
    type: NamedResourceJson


class PokemonAbilityJson(TypedDict):
    ability: NamedResourceJson
    is_hidden: bool
    slot: int


class MoveLearnDetailJson(TypedDict):
    move_learn_method: str
    level_learned_at: int


class PokemonMoveJson(TypedDict):
    name: str
    learn_details: list[MoveLearnDetailJson]


class PokemonJson(TypedDict):
    id: int
    name: str
    height: int
    weight: int
    base_experience: int
    stats: list[PokemonStatJson]
    types: list[PokemonTypeSlotJson]
    abilities: list[PokemonAbilityJson]
    moves: list[PokemonMoveJson]
    color: str


@dataclass(frozen=True)
class PokemonPreview:
    key: str
    name: str
    type: str
    color: str
    base_experience: int
    stats: list[PokemonStatJson]
