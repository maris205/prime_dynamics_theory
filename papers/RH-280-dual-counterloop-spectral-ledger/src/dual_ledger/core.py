SPECTRAL_VECTOR = (False, False, False, True, True)
COUNTERLOOP_VECTOR = (True, True, False, True, True)


def complete(vector: tuple[bool, ...]) -> bool:
    return all(vector)
