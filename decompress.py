#! /usr/bin/env python3

import binascii

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

def decompress_pubkey(pk):
    x = int.from_bytes(pk[1:33], byteorder='big')
    y_sq = (pow(x, 3, p) + 7) % p
    y = pow(y_sq, (p + 1) // 4, p)
    if y % 2 != pk[0] % 2:
        y = p - y
    y = y.to_bytes(32, byteorder='big')
    return b'\x04' + pk[1:33] + y

print(binascii.hexlify(decompress_pubkey(binascii.unhexlify('03e7579404be98ac23188463cf47cea128f95bd0efdc75fe70cd9c3ba0d2cf8f44'))).decode())
print(binascii.hexlify(decompress_pubkey(binascii.unhexlify('03e7579404be98ac23188463cf47cea128f95bd0efdc75fe70cd9c3ba0d2cf8f44'))).decode())