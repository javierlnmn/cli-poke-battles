import json
import time

import requests

from config.config import POKEMON_MOVES_FILE_PATH
from repositories import MoveRepository
from schemas import MoveJson
from utils.files import write_file_data


class MoveService:
    FIRST_GEN_MOVE_COUNT = 165

    EXCLUDED_CATEGORIES = {"force-switch", "unique"}

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
        moves = {}
        for ref in range(1, self.FIRST_GEN_MOVE_COUNT + 1):
            raw = self.session.get(f"https://pokeapi.co/api/v2/move/{ref}", timeout=20).json()
            if raw["meta"]["category"]["name"] in self.EXCLUDED_CATEGORIES:
                print(f"[{ref:3}] skip ({raw['meta']['category']['name']}): {raw['name']}")
                continue
            moves[raw["name"]] = self._trim_move(raw)
            print(f"[{ref:3}] {raw['name']}")
            time.sleep(0.05)
        return moves

    def update_data(self) -> None:
        moves = self.fetch()
        write_file_data(POKEMON_MOVES_FILE_PATH, json.dumps(moves, indent=4))
        MoveRepository.clear_cache()
        print(f"\nDone. {len(moves)} moves written to {POKEMON_MOVES_FILE_PATH}.")

    def _trim_move(self, raw) -> MoveJson:
        return {field: raw[field] for field in self.MOVE_FIELDS}


if __name__ == "__main__":
    MoveService().update_data()
