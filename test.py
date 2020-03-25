# 格式转换
"""
hex string to bytes
eg:
'01 23 45 67 89 AB CD EF 01 23 45 67 89 AB CD EF'
b'\x01#Eg\x89\xab\xcd\xef\x01#Eg\x89\xab\xcd\xef'
"""


def hexStringTobytes(str):
    str = str.replace(" ", "")
    return bytes.fromhex(str)
    # return a2b_hex(str)