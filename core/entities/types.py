from dataclasses import dataclass


@dataclass(frozen=True)
class PokemonType:
    id: int
    key: str
    name: str
    double_damage_from: list[str]
    double_damage_to: list[str]
    half_damage_from: list[str]
    half_damage_to: list[str]
    no_damage_from: list[str]
    no_damage_to: list[str]
