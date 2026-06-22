import json
import time

import requests

from core.config import POKEMON_MOVES_FILE_PATH
from core.repositories import MoveRepository, TypeRepository
from core.schemas import MoveJson
from core.utils.files import write_file_data


class MoveService:
    FIRST_GEN_MOVE_COUNT = 165

    EXCLUDED_CATEGORIES = {
        "force-switch",
        "unique",
        "whole-field-effect",
        "field-effect",
    }

    EXCLUDED_AILMENTS = {
        "leech-seed",
    }

    MOVE_FIELDS = [
        "accuracy",
        "damage_class",
        "generation",
        "id",
        "meta",
        "name",
        "names",
        "power",
        "pp",
        "priority",
        "stat_changes",
        "target",
        "type",
    ]

    def __init__(self):
        self.session = requests.Session()

    def fetch(self) -> dict[str, MoveJson]:
        type_catalog = self._type_catalog()

        moves = {}
        for ref in range(1, self.FIRST_GEN_MOVE_COUNT + 1):
            raw = self.session.get(f"https://pokeapi.co/api/v2/move/{ref}", timeout=20).json()

            category = raw["meta"]["category"]["name"]
            if category in self.EXCLUDED_CATEGORIES:
                print(f"[{ref:3}] skip ({category}): {raw['name']}")
                continue

            ailment = raw["meta"]["ailment"]["name"]
            if ailment in self.EXCLUDED_AILMENTS:
                print(f"[{ref:3}] skip (ailment {ailment}): {raw['name']}")
                continue

            move_type = raw["type"]["name"]
            if type_catalog and move_type not in type_catalog:
                print(f"[{ref:3}] skip (type {move_type}): {raw['name']}")
                continue

            moves[raw["name"]] = self._trim_move(raw)
            print(f"[{ref:3}] {raw['name']}")
            time.sleep(0.05)
        return moves

    def update_data(self) -> None:
        moves = self.fetch()
        write_file_data(POKEMON_MOVES_FILE_PATH, json.dumps(moves, indent=4))
        MoveRepository.clear_cache()

    @staticmethod
    def _type_catalog() -> dict:
        try:
            return TypeRepository.load_types_data()
        except FileNotFoundError:
            return {}

    def _trim_move(self, raw) -> MoveJson:
        return {field: raw[field] for field in self.MOVE_FIELDS}


if __name__ == "__main__":
    MoveService().update_data()
