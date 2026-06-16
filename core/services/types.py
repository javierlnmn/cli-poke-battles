import json
import time

import requests

from core.config import POKEMON_TYPES_FILE_PATH
from core.repositories import TypeRepository
from core.schemas import TypeJson
from core.utils.files import write_file_data


class TypeService:
    LAST_TYPE_ID = 16

    TYPE_FIELDS = [
        "id",
        "name",
        "names",
        "damage_relations",
    ]

    def __init__(self):
        self.session = requests.Session()

    def fetch(self) -> dict[str, TypeJson]:
        types = {}
        for ref in range(1, self.LAST_TYPE_ID + 1):
            raw = self.session.get(f"https://pokeapi.co/api/v2/type/{ref}", timeout=20).json()
            types[raw["name"]] = self._trim_type(raw)
            print(f"[{ref:3}] {raw['name']}")
            time.sleep(0.05)
        return types

    def update_data(self) -> None:
        types = self.fetch()
        write_file_data(POKEMON_TYPES_FILE_PATH, json.dumps(types, indent=4))
        TypeRepository.clear_cache()

    def _trim_type(self, raw) -> TypeJson:
        trimmed = {field: raw[field] for field in self.TYPE_FIELDS}
        trimmed["damage_relations"] = {
            relation: [t for t in types if self._is_gen1_type(t["url"])]
            for relation, types in raw["damage_relations"].items()
        }
        return trimmed

    def _is_gen1_type(self, url: str) -> bool:
        type_id = int(url.rstrip("/").split("/")[-1])
        return type_id <= self.LAST_TYPE_ID


if __name__ == "__main__":
    TypeService().update_data()
