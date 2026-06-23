from dataclasses import dataclass
from enum import Enum


class TypeDamageMultiplierEnum(Enum):
    VERY_EFFECTIVE = 2
    NOT_VERY_EFFECTIVE = 0.5
    EFFECTIVE = 1
    NOT_AFFECT = 0


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

    def get_attacking_multiplier(self, *, recieving_type: "PokemonType") -> int:
        return self._get_multiplier_for(
            recieving_type.key,
            none_list=self.no_damage_to,
            half_list=self.half_damage_to,
            double_list=self.double_damage_to,
        )

    def get_recieving_multiplier(self, *, attacking_type: "PokemonType") -> int:
        return self._get_multiplier_for(
            attacking_type.key,
            none_list=self.no_damage_from,
            half_list=self.half_damage_from,
            double_list=self.double_damage_from,
        )

    def _get_multiplier_for(
        self,
        other_key: str,
        *,
        none_list: list[str],
        half_list: list[str],
        double_list: list[str],
    ):
        if other_key in none_list:
            return TypeDamageMultiplierEnum.NOT_AFFECT.value

        if other_key in half_list:
            return TypeDamageMultiplierEnum.NOT_VERY_EFFECTIVE.value

        if other_key in double_list:
            return TypeDamageMultiplierEnum.VERY_EFFECTIVE.value

        return TypeDamageMultiplierEnum.EFFECTIVE.value
