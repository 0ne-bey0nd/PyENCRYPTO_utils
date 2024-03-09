from PyENCRYPTO_utils.typedefs import *

# #define AES_KEY_BITS			128
# #define AES_KEY_BYTES			16
# #define AES_BITS				128
# #define AES_BYTES				16

AES_KEY_BITS = 128
AES_KEY_BYTES = 16
AES_BITS = 128
AES_BYTES = 16

# #define SHA1_OUT_BYTES 20
# #define SHA256_OUT_BYTES 32
# #define SHA512_OUT_BYTES 64
#
# #define MAX_NUM_COMM_CHANNELS 256
# #define ADMIN_CHANNEL MAX_NUM_COMM_CHANNELS-1

SHA1_OUT_BYTES = 20
SHA256_OUT_BYTES = 32
SHA512_OUT_BYTES = 64

MAX_NUM_COMM_CHANNELS = 256  # 通信通道的最大数量
ADMIN_CHANNEL = MAX_NUM_COMM_CHANNELS - 1  # 管理员通道

import enum

class field_type(enum.Enum):
    P_FIELD = 0
    ECC_FIELD = 1
    FIELD_LAST = 2


ST = seclvl(40, 80, 1024)
MT = seclvl(40, 112, 2048)
LT = seclvl(40, 128, 3072)
XLT = seclvl(40, 192, 7680)
XXLT = seclvl(40, 256, 15360)

m_vFixedKeyAESSeed = bytes(
    [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF])

m_vSeed = bytes([0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF])


def getFieldType(ftype: field_type) -> str:
    if ftype == field_type.P_FIELD:
        return "P_FIELD"
    elif ftype == field_type.ECC_FIELD:
        return "ECC_FIELD"
    else:
        return "unknown field"
