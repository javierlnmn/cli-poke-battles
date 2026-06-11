from typing import TypedDict


class NamedResourceJson(TypedDict):
    name: str
    url: str


class LocalizedNameJson(TypedDict):
    name: str
    language: NamedResourceJson
