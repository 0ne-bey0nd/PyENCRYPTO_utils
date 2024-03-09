from os import urandom
from .int_types import Uint64


def ceil_log2(x: Uint64) -> int:
    """
    计算 x 的向上取整的 log2
    :param x: 输入
    :return: 向上取整的 log2
    """
    if x == 0:
        return 0
    else:
        return (x - 1).bit_length()


def aby_rand():
    return int.from_bytes(urandom(4), byteorder='big', signed=False)
    ...
