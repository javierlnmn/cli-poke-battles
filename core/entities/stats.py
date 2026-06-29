from dataclasses import dataclass
from enum import Enum


class PokemonStatEnum(Enum):
    HP = "hp"
    ATTACK = "attack"
    DEFENSE = "defense"
    SP_ATTACK = "special-attack"
    SP_DEFENSE = "special-defense"
    SPEED = "speed"
    ACCURACY = "accuracy"
    EVASION = "evasion"


@dataclass
class PokemonStats:
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int

    _STAT_ENUM_FIELD_OVERRIDES = {
        PokemonStatEnum.SP_ATTACK: "sp_attack",
        PokemonStatEnum.SP_DEFENSE: "sp_defense",
    }

    def get_stat(self, stat: PokemonStatEnum) -> int:
        field = self._STAT_ENUM_FIELD_OVERRIDES.get(stat, stat.value)
        return getattr(self, field)
