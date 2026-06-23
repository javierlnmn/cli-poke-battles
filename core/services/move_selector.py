import random
from dataclasses import dataclass

from core.entities.battle import BattlePokemonMove
from core.entities.moves import DamageClassEnum
from core.entities.pokemon import Pokemon, PokemonMoveMetadata


@dataclass(frozen=True)
class ScoredMove:
    metadata: PokemonMoveMetadata
    score: float


class MoveSelector:
    STAB_BONUS = 30.0
    CLASS_MATCH_BONUS = 15.0
    MAX_POWER = 70.0
    POWER_WEIGHT = 20.0
    ACCURACY_WEIGHT = 5.0
    PP_WEIGHT = 0.25
    HIGH_LEVEL_THRESHOLD = 34
    HIGH_LEVEL_PENALTY = 15.0

    SLOT_COUNT = 4
    TIER_RATIO = 0.7

    def __init__(self, *, rng: random.Random | None = None) -> None:
        self.rng = rng or random.Random()

    def select(self, pokemon: Pokemon) -> tuple[BattlePokemonMove, ...]:
        moves = pokemon.moves_metadata

        if not moves:
            return ()

        if len(moves) <= self.SLOT_COUNT:
            return tuple(
                BattlePokemonMove(move=metadata.move, current_pp=metadata.move.pp or 0) for metadata in moves
            )

        scored = sorted(
            (self._score(metadata, pokemon) for metadata in moves),
            key=lambda s: s.score,
            reverse=True,
        )

        top_score = scored[0].score
        tier = [s for s in scored if s.score >= top_score * self.TIER_RATIO]

        slot_count = min(self.SLOT_COUNT, len(moves))
        chosen = self._weighted_sample_without_replacement(tier, min(slot_count, len(tier)))

        if len(chosen) < slot_count:
            remaining = [s for s in scored if s not in chosen]
            chosen.extend(self._weighted_sample_without_replacement(remaining, slot_count - len(chosen)))

        return tuple(
            BattlePokemonMove(move=s.metadata.move, current_pp=s.metadata.move.pp or 0) for s in chosen
        )

    def _score(self, metadata: PokemonMoveMetadata, pokemon: Pokemon) -> ScoredMove:
        move = metadata.move
        score = 0.0

        pokemon_type_keys = {t.key for t in pokemon.types}
        if move.type.key in pokemon_type_keys:
            score += self.STAB_BONUS

        preferred_class = self._preferred_damage_class(pokemon)
        if move.damage_class == preferred_class:
            score += self.CLASS_MATCH_BONUS

        if move.power:
            score += min(move.power, self.MAX_POWER) / self.MAX_POWER * self.POWER_WEIGHT

        if move.accuracy is not None:
            score += move.accuracy / 100 * self.ACCURACY_WEIGHT

        if move.pp:
            score += min(move.pp, 40) * self.PP_WEIGHT

        level = metadata.level_learned_at
        if isinstance(level, list):
            level = max((d.get("level_learned_at", 0) for d in level), default=0)
        if isinstance(level, int) and level >= self.HIGH_LEVEL_THRESHOLD:
            score -= self.HIGH_LEVEL_PENALTY

        return ScoredMove(metadata=metadata, score=score)

    @staticmethod
    def _preferred_damage_class(pokemon: Pokemon) -> DamageClassEnum:
        if pokemon.stats.sp_attack >= pokemon.stats.attack:
            return DamageClassEnum.SPECIAL
        return DamageClassEnum.PHYSICAL

    def _weighted_sample_without_replacement(
        self,
        scored: list[ScoredMove],
        k: int,
    ) -> list[ScoredMove]:
        pool = list(scored)
        picked: list[ScoredMove] = []
        for _ in range(k):
            weights = [max(s.score, 0.01) for s in pool]
            chosen_idx = self.rng.choices(range(len(pool)), weights=weights, k=1)[0]
            picked.append(pool.pop(chosen_idx))
        return picked
