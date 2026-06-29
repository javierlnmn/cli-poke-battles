from dataclasses import dataclass
from enum import Enum

from core.entities.stats import PokemonStatEnum, PokemonStats


class StageLimit(Enum):
    TOP = "top"
    BOTTOM = "bottom"


@dataclass
class BattlePokemonStatsStages:
    base_stats: PokemonStats

    # Stat stages range from -6 to 6, and are used to calculate the multipliers
    # affecting the actual stats, resulting in the effective stats.
    attack_stage: int = 0
    defense_stage: int = 0
    sp_attack_stage: int = 0
    sp_defense_stage: int = 0
    speed_stage: int = 0
    accuracy_stage: int = 0
    evasion_stage: int = 0

    _STAT_STAGE_FIELD_MAP = {
        PokemonStatEnum.ATTACK: "attack_stage",
        PokemonStatEnum.DEFENSE: "defense_stage",
        PokemonStatEnum.SP_ATTACK: "sp_attack_stage",
        PokemonStatEnum.SP_DEFENSE: "sp_defense_stage",
        PokemonStatEnum.SPEED: "speed_stage",
        PokemonStatEnum.ACCURACY: "accuracy_stage",
        PokemonStatEnum.EVASION: "evasion_stage",
    }

    def update_stat_stage(self, stat: PokemonStatEnum, change: int) -> StageLimit | None:
        field = self._STAT_STAGE_FIELD_MAP[stat]
        current = getattr(self, field)
        limit = self._check_stage_limit(current, change)
        if limit:
            return limit
        setattr(self, field, current + change)

    def _check_stage_limit(self, stage: int, change: int) -> StageLimit | None:
        if stage <= -6 and change < 0:
            return StageLimit.BOTTOM
        if stage >= 6 and change > 0:
            return StageLimit.TOP

    def restore_stages(self) -> None:
        for field in self._STAT_STAGE_FIELD_MAP.values():
            setattr(self, field, 0)

    def get_effective_stat(self, stat: PokemonStatEnum) -> int:
        field = self._STAT_STAGE_FIELD_MAP[stat]
        stage = getattr(self, field)
        base_val = self.base_stats.get_stat(stat)
        return self.calculate_stage_multiplier(base_val, stage)

    def calculate_stage_multiplier(self, stat_val: int, stage: int) -> int:
        multiplier = self._get_multiplier_for_stage(stage)
        return round(stat_val * multiplier)

    def _get_multiplier_for_stage(self, stage: int) -> float:
        return (2 + stage) / 2 if stage >= 0 else 2 / (2 + (stage * -1))
