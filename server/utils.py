import asyncio
from typing import List

class APIKeyRotator:
    def __init__(self, keys: List[str]):
        self.keys = keys
        self.index = 0
        self.lock = asyncio.Lock()

    async def get_key(self) -> str:
        async with self.lock:
            return self.keys[self.index]

    async def rotate_key(self):
        async with self.lock:
            self.index = (self.index + 1) % len(self.keys)
            print(f"Rotated to API key index: {self.index}")
