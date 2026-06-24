from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import randrange

from core.entities.battle.move import BattlePokemonMove
from core.entities.battle.pokemon import BattlePokemon
from core.entities.moves import DamageClassEnum
from core.entities.types import PokemonType
from core.exceptions import StatusMoveDamageError, UnsupportedDamageClassError


@dataclass
class DamageCalculator(ABC):
    battle_move: BattlePokemonMove
    attacker: BattlePokemon
    target: BattlePokemon

    @abstractmethod
    def calculate_damage(self) -> int: ...


@dataclass
class Gen1DamageCalculator(DamageCalculator):
    """
    Gen. 1 formula:
    D = ((((((2 * L * CRIT) / 5) + 2) * P * At/Def)/50) + 2) * STAB * T1 * T2 * R
    Where:
        - L: Level of the attacker.
        - CRIT: 2 for a critical hit, 1 otherwise.
        - A: Attacker attack/sp. attack (see move class).
        - D: Target defense/sp. defense (see move class).
        - Power: Move power.
        - STAB: Same-Type Attack Bonus. Equal to 1.5 when the move's type matches the Pokémon type.
        - T1: Type effectiveness of the move against the target's first type.
        - T2: Type effectiveness of the move against the target's second type. 1 if target has only 1 type.
        - R: A multiplication by a random uniformly distributed integer between 217 and 255 (inclusive),
            followed by an integer division by 255. If the calculated damage thus far is 1, random is
            always 1.
    """

    def calculate_damage(self) -> int:
        crit = 2 if self._is_critical() else 1
        l2crit_over_5_plus_2 = ((2 * self.attacker.level * crit) / 5) + 2

        att_over_def = self._get_att_over_def()
        stab = 1.5 if self._has_same_type_attack_bonus() else 1
        t1 = self._get_type_effectiveness(self.target.pokemon.types[0])
        t2 = (
            self._get_type_effectiveness(self.target.pokemon.types[1])
            if len(self.target.pokemon.types) >= 2
            else 1
        )

        damage = (
            (((l2crit_over_5_plus_2 * self.battle_move.move.power * att_over_def) / 50) + 2) * stab * t1 * t2
        )

        r = 1 if damage == 1 else self._get_random_factor()

        return int(damage * r)

    def _is_critical(self) -> bool:
        """
        Gen. 1 critial hit calculation is determined by comparing a random number between 0 and 255 with a
        threshold value that also ranges from 0 to 255. If the random number is strictly lower than the
        threshold, the hit is critical.
        The threshold is calculated in several ways:
            - Under normal circumstances: T = (BaseSpeed/2)
            - If the move has critical-high ratio: T=min(8*(BaseSpeed/2), 255)
            - If the Pokémon used a move that increases crit chance, T is calculated differently, however
                this is not contemplated in the current implementation.
        """
        rand = randrange(256)
        threshold = (
            self.attacker.pokemon.stats.speed / 2
            if self.battle_move.move.crit_rate < 1
            else min(8 * (self.attacker.pokemon.stats.speed / 2), 255)
        )
        return True if rand < threshold else False

    def _get_att_over_def(self) -> float:
        if self.battle_move.move.damage_class == DamageClassEnum.STATUS:
            raise StatusMoveDamageError(self.battle_move.move.name)
        elif self.battle_move.move.damage_class == DamageClassEnum.PHYSICAL:
            att = self.attacker.current_stats.attack
            defn = self.target.current_stats.defense
        elif self.battle_move.move.damage_class == DamageClassEnum.SPECIAL:
            att = self.attacker.current_stats.sp_attack
            defn = self.target.current_stats.sp_defense
        else:
            raise UnsupportedDamageClassError(self.battle_move.move.damage_class.value)

        return att / defn

    def _has_same_type_attack_bonus(self) -> bool:
        return True if self.battle_move.move.type in self.attacker.pokemon.types else False

    def _get_type_effectiveness(self, target_type: PokemonType) -> float:
        return self.battle_move.move.type.get_attacking_multiplier(recieving_type=target_type)

    def _get_random_factor(self) -> float:
        return randrange(217, 256) / 255
