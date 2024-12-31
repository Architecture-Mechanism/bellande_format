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

from typing import List, Dict, Tuple
import heapq
from dataclasses import dataclass
from collections import Counter

@dataclass
class HuffmanNode:
    char: str
    freq: int
    left: 'HuffmanNode' = None
    right: 'HuffmanNode' = None

    def __lt__(self, other):
        return self.freq < other.freq

class Compression:
    def __init__(self):
        self.huffman_codes: Dict[str, str] = {}

    def build_huffman_tree(self, data: bytes) -> HuffmanNode:
        # Count frequency of each byte
        freq = Counter(data)
        
        # Create heap of HuffmanNodes
        heap: List[HuffmanNode] = []
        for char, frequency in freq.items():
            node = HuffmanNode(char=char, freq=frequency)
            heapq.heappush(heap, node)
        
        # Build the tree
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            internal = HuffmanNode(
                char=None,
                freq=left.freq + right.freq,
                left=left,
                right=right
            )
            heapq.heappush(heap, internal)
            
        return heap[0]

    def generate_codes(self, node: HuffmanNode, code: str = ""):
        if node is None:
            return
            
        if node.char is not None:
            self.huffman_codes[node.char] = code
            return
            
        self.generate_codes(node.left, code + "0")
        self.generate_codes(node.right, code + "1")

    def encode_data(self, data: bytes) -> Tuple[bytes, Dict]:
        # Build Huffman tree and generate codes
        root = self.build_huffman_tree(data)
        self.huffman_codes.clear()
        self.generate_codes(root)
        
        # Encode the data
        encoded = "".join(self.huffman_codes[char] for char in data)
        
        # Convert binary string to bytes
        padding = 8 - (len(encoded) % 8)
        encoded += "0" * padding
        
        result = bytearray()
        for i in range(0, len(encoded), 8):
            result.append(int(encoded[i:i+8], 2))
            
        return bytes(result), {"codes": self.huffman_codes, "padding": padding}

    def decode_data(self, data: bytes, metadata: Dict) -> bytes:
        # Convert bytes to binary string
        binary = "".join(format(byte, '08b') for byte in data)
        
        # Remove padding
        binary = binary[:-metadata["padding"]]
        
        # Create reverse lookup table
        reverse_codes = {code: char for char, code in metadata["codes"].items()}
        
        # Decode the data
        decoded = bytearray()
        current_code = ""
        
        for bit in binary:
            current_code += bit
            if current_code in reverse_codes:
                decoded.append(reverse_codes[current_code])
                current_code = ""
                
        return bytes(decoded)
