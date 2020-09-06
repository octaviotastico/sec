import struct
import binascii

# This a pure sha512 implementation from https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf

# This was tested using https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/SHA512.pdf
# and https://emn178.github.io/online-tools/sha512.html

class SHA512:

    def __init__(self):
        self.h = [
            0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
            0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179
        ]

        self.k = [
            0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc, 0x3956c25bf348b538,
            0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242, 0x12835b0145706fbe,
            0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2, 0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235,
            0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
            0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 0x983e5152ee66dfab,
            0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
            0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed,
            0x53380d139d95b3df, 0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
            0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218,
            0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8, 0x19a4c116b8d2d0c8, 0x1e376c085141ab53,
            0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373,
            0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
            0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b, 0xca273eceea26619c,
            0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba, 0x0a637dc5a2c898a6,
            0x113f9804bef90dae, 0x1b710b35131c471b, 0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc,
            0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
        ]

    def rotate_right(self, v, n):
        w = (v >> n) | (v << (64 - n))
        return w & 0xFFFFFFFFFFFFFFFF

    def compute_w(self, msg):
        w = list(struct.unpack('>16Q', msg))
        for _ in range(16, 80):
            a, b = w[-15], w[-2]
            s0 = self.rotate_right(a, 1) ^ self.rotate_right(a, 8) ^ (a >> 7)
            s1 = self.rotate_right(b, 19) ^ self.rotate_right(b, 61) ^ (b >> 6)
            s = (w[-16] + w[-7] + s0 + s1) & 0xFFFFFFFFFFFFFFFF
            w.append(s)
        return w

    def padding(self, msg: bytes) -> bytes:
        L = len(msg)
        K = (112 - L - 1) % 128
        F = 0xFFFFFFFFFFFFFFFF
        pad = struct.pack('>QQ', ((L * 8) >> 64) & F, (L * 8) & F)
        return msg + bytes([0x80]) + bytes(K) + pad

    def __compression_step(self, state, k_i, w_i):
        a, b, c, d, e, f, g, h = state
        ch = (e & f) ^ (~e & g)
        maj = (a & b) ^ (a & c) ^ (b & c)
        s0 = self.rotate_right(a, 28) ^ self.rotate_right(a, 34) ^ self.rotate_right(a, 39)
        s1 = self.rotate_right(e, 14) ^ self.rotate_right(e, 18) ^ self.rotate_right(e, 41)
        t1 = (h + s1 + ch + k_i + w_i) & 0xFFFFFFFFFFFFFFFF
        t2 = (t1 + s0 + maj) & 0xFFFFFFFFFFFFFFFF
        t3 = (d + t1) & 0xFFFFFFFFFFFFFFFF
        return t2, a, b, c, t3, e, f, g

    def __compression(self, state, w, round_keys = None):
        if round_keys is None:
            round_keys = self.k
        for i in range(80):
            state = self.__compression_step(state, round_keys[i], w[i])
        return state

    def __sha512_raw(self, msg, round_keys = None):
        if len(msg) % 128 != 0:
            raise ValueError('msg must be a multiple of 128 bytes')
        state = self.h
        for i in range(0, len(msg), 128):
            block = msg[i: i + 128]
            w = self.compute_w(block)
            s = self.__compression(state, w, round_keys)
            state = [(x + y) & 0xFFFFFFFFFFFFFFFF for x, y in zip(state, s)]
        return state

    def hash(self, msg: bytes, round_keys = None):
        msg_padded = self.padding(msg)
        state = self.__sha512_raw(msg_padded, round_keys)
        return struct.pack('>8Q', *state)


print(binascii.hexlify(SHA512().hash(b'secret')))