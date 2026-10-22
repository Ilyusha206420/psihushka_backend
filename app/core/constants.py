from enum import Enum, auto
from typing import override
from zlib import crc32

class _BaseHashedEnum(int, Enum):
    @override
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[int]) -> int:
        hash: int = crc32(name.encode())
        if hash in last_values:
            raise ValueError(f"Error! Key {name} generated hash {hash} which is already in use!")
        return hash


class Methods(_BaseHashedEnum):
    START_POS = auto()

