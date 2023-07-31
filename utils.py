def if_negative_convert_to_zero(value: int | float) -> int | float:
    if value < 0:
        return 0
    return value
