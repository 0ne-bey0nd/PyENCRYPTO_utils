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

# uint32_t floor_log2(int bits) {
# 	if (bits == 1)
# 		return 1;
# 	int targetlevel = 0;
# 	while (bits >>= 1)
# 		++targetlevel;
# 	return targetlevel;
# }

def floor_log2(x: Uint64) -> int:
    """
    计算 x 的向下取整的 log2
    :param x: 输入
    :return: 向下取整的 log2
    """
    if x == 0:
        return 0
    else:
        return x.bit_length()

def ceil_divide(a: Uint64, b: Uint64) -> Uint64:
    """
    向上取整的除法
    :param a: 被除数
    :param b: 除数
    :return: 商
    """
    return (a + b - 1) // b

def aby_prng(bitlen: Uint64) -> Uint64:
    byte_count = ceil_divide(bitlen, Uint64(8))
    data = urandom(byte_count)
    rnd = int.from_bytes(data, byteorder='big', signed=False)
    return rnd



def aby_rand():
    return int.from_bytes(urandom(4), byteorder='big', signed=False)
    ...
