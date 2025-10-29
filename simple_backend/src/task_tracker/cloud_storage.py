import requests
from typing import List

class JSONBinStorage:
    def __init__(self, bin_id: str, api_key: str):
        self.bin_id = bin_id
        self.api_key = api_key
        self.base_url = f'https://api.jsonbin.io/v3/b/{self.bin_id}'
        self.headers = {
            'X-Master-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    def load_data(self) -> List[dict]:
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('record', [])
        return []

    def save_data(self, data: List[dict]) -> bool:
        response = requests.put(self.base_url, json=data, headers=self.headers)
        return response.status_code == 200