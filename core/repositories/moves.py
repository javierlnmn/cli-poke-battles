from typing import ClassVar

from core.config import POKEMON_MOVES_FILE_PATH
from core.entities.moves import (
    AilmentEnum,
    CategoryEnum,
    DamageClassEnum,
    MoveAilment,
    MoveHits,
    MoveStatChange,
    MoveTurns,
    PokemonMove,
    TargetEnum,
)
from core.repositories.types import TypeRepository
from core.schemas import MoveJson
from core.utils.files import read_file_data_json


class MoveRepository:
    _moves_data: ClassVar[dict[str, MoveJson] | None] = None
    _moves: ClassVar[dict[str, PokemonMove]] = {}

    @classmethod
    def load_moves_data(cls) -> dict[str, MoveJson]:
        if cls._moves_data is None:
            cls._moves_data = read_file_data_json(POKEMON_MOVES_FILE_PATH)
        return cls._moves_data

    @classmethod
    def get_moves(cls) -> list[PokemonMove]:
        return [cls.get(key) for key in cls.load_moves_data()]

    @classmethod
    def get(cls, name_id: str) -> PokemonMove:
        key = name_id.lower()

        if key not in cls._moves:
            move_data = cls.load_moves_data().get(key)
            if not move_data:
                raise ValueError(f"Move '{name_id}' not found")

            cls._moves[key] = cls._build(move_data)

        return cls._moves[key]

    @classmethod
    def clear_cache(cls) -> None:
        cls._moves_data = None
        cls._moves = {}

    @staticmethod
    def _build(data: MoveJson) -> PokemonMove:
        visible_name = None

        for lang_name in data["names"]:
            if lang_name["language"]["name"] == "en":
                visible_name = lang_name["name"]
                break

        meta = data["meta"]

        return PokemonMove(
            id=data["id"],
            name=data["name"],
            visible_name=visible_name,
            type=TypeRepository.get(data["type"]["name"]),
            damage_class=DamageClassEnum(data["damage_class"]["name"]),
            power=data["power"],
            accuracy=data["accuracy"],
            pp=data["pp"],
            priority=data["priority"],
            target=TargetEnum(data["target"]["name"]),
            category=CategoryEnum(meta["category"]["name"]),
            crit_rate=meta["crit_rate"],
            drain=meta["drain"],
            flinch_chance=meta["flinch_chance"],
            healing=meta["healing"],
            ailment_data=MoveAilment(
                ailment=AilmentEnum(meta["ailment"]["name"]),
                chance=meta["ailment_chance"],
            ),
            hits_limit=MoveHits(
                max_hits=meta["max_hits"],
                min_hits=meta["min_hits"],
            ),
            turns_limit=MoveTurns(
                max_turns=meta["max_turns"],
                min_turns=meta["min_turns"],
            ),
            stat_changes=[
                MoveStatChange(
                    change=stat_change["change"],
                    stat=stat_change["stat"]["name"],
                    chance=meta["stat_chance"],
                )
                for stat_change in data["stat_changes"]
            ],
        )
