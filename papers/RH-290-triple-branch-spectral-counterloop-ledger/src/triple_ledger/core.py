from __future__ import annotations


def score(vector: tuple[bool, ...]) -> int:
    return sum(bool(value) for value in vector)


def complete_count(vectors: list[tuple[bool, ...]]) -> int:
    return sum(all(vector) for vector in vectors)


def coordinatewise_union(*vectors: tuple[bool, ...]) -> tuple[bool, ...]:
    if not vectors or len({len(vector) for vector in vectors}) != 1:
        raise ValueError("nonempty equal-length vectors required")
    return tuple(any(vector[index] for vector in vectors) for index in range(len(vectors[0])))
