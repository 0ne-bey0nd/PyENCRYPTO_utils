from .int_types import Uint64
from .utils import ceil_log2

UGATE_T = Uint64  # 64 bits
REGISTER_SIZE = Uint64  # 64 bits


class SECURITYLEVELS:
    def __init__(self, statbits: int, symbits: int, ifcbits: int):
        self.statbits = statbits
        self.symbits = symbits
        self.ifcbits = ifcbits

    def __str__(self):
        return f"SECURITYLEVELS(statbits={self.statbits}, symbits={self.symbits}, ifcbits={self.ifcbits})"

    def __repr__(self):
        return f"SECURITYLEVELS(statbits={self.statbits}, symbits={self.symbits}, ifcbits={self.ifcbits})"


seclvl = SECURITYLEVELS

GATE_T_BITS = UGATE_T.size  # todo: UGATE_T 占用的位数
REGSIZE = REGISTER_SIZE

# LOG2_REGISTER_SIZE = ceil_log2(sizeof(REGISTER_SIZE) << 3)
LOG2_REGISTER_SIZE = ceil_log2(REGISTER_SIZE.size << 3)

RETRY_CONNECT = 1000

AES_BITS = 128
OTEXT_BLOCK_SIZE_BITS = AES_BITS


def rem(a: int, b: int) -> int:
    return (a % b) if a > 0 else (a % b) + (b if b > 0 else b * -1)


def sub(a: int, b: int, m: int) -> int:
    return (a + m - b) if b > a else (a - b)


if __name__ == '__main__':
    a = uint64_t(2 ** 64 - 1)
    b = uint64_t(123)
    print(a + b)
    print(a + 1)
    print(1 + a)
    ...
