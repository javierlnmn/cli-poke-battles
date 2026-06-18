import json
from pathlib import Path


def read_file_data(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def read_file_data_json(file_path: str) -> str:
    return json.loads(read_file_data(file_path))


def write_file_data(file_path: str, data: str) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data)
