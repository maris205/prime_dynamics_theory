PAPER_NUMBERS = tuple(range(272, 282))


def spectral_vector() -> tuple[bool, ...]:
    return (False, False, False, True, True)


def counterloop_vector() -> tuple[bool, ...]:
    return (True, True, False, True, True)
