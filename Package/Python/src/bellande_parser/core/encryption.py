# Copyright (C) 2024 Bellande Architecture Mechanism Research Innovation Center, Ronaldson Bellande

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/env python3

from typing import List
import os

class AES:
    def __init__(self):
        self.block_size = 16

    def pad(self, text: bytes) -> bytes:
        padding_size = self.block_size - (len(text) % self.block_size)
        padding = bytes([padding_size] * padding_size)
        return text + padding

    def unpad(self, text: bytes) -> bytes:
        padding_size = text[-1]
        return text[:-padding_size]

    def expand_key(self, key: bytes, rounds: int) -> List[bytes]:
        expanded: List[bytes] = []
        # Key expansion logic here
        return expanded

    def encrypt_block(self, block: bytes, round_keys: List[bytes]) -> bytes:
        # AES block encryption implementation
        state = list(block)
        # Add round key
        # SubBytes
        # ShiftRows
        # MixColumns
        # Final round
        return bytes(state)

    def decrypt_block(self, block: bytes, round_keys: List[bytes]) -> bytes:
        # AES block decryption implementation
        state = list(block)
        # Inverse operations
        return bytes(state)

class Encryption:
    def __init__(self):
        self.aes = AES()

    def generate_key(self) -> bytes:
        return os.urandom(32)

    def encrypt(self, data: bytes, key: bytes) -> bytes:
        iv = os.urandom(16)  # Initialization vector
        padded_data = self.aes.pad(data)
        round_keys = self.aes.expand_key(key, 10)
        
        cipher = iv
        previous = iv
        
        for i in range(0, len(padded_data), 16):
            block = padded_data[i:i+16]
            block = bytes(a ^ b for a, b in zip(block, previous))
            encrypted_block = self.aes.encrypt_block(block, round_keys)
            cipher += encrypted_block
            previous = encrypted_block
            
        return cipher

    def decrypt(self, cipher: bytes, key: bytes) -> bytes:
        iv = cipher[:16]
        cipher = cipher[16:]
        round_keys = self.aes.expand_key(key, 10)
        
        plain = b""
        previous = iv
        
        for i in range(0, len(cipher), 16):
            block = cipher[i:i+16]
            decrypted_block = self.aes.decrypt_block(block, round_keys)
            plain_block = bytes(a ^ b for a, b in zip(decrypted_block, previous))
            plain += plain_block
            previous = block
            
        return self.aes.unpad(plain)
