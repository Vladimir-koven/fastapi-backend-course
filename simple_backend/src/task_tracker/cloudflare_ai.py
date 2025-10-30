import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Dict, Any

load_dotenv('passwords.env')


class BaseHTTPClient(ABC):
    def __init__(self, base_url: str, headers: Dict[str, str], timeout: int = 30):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def _make_request(self, method: str, endpoint: str = "", **kwargs) -> Dict[str, Any]:
        """Общий метод для выполнения HTTP запросов"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"HTTP Error {response.status_code}: {response.text}")
        except requests.RequestException as e:
            raise Exception(f"Network error: {e}")

    @abstractmethod
    def validate_credentials(self):
        pass

    @abstractmethod
    def get_service_name(self) -> str:
        pass

class AIRequest(BaseModel):
    messages: list

class AIResponse(BaseModel):
    response: str

class CloudflareAI(BaseHTTPClient):
    def __init__(self):
        self.api_token = os.getenv("CF_API_TOKEN")
        self.account_id = os.getenv("CF_ACCOUNT_ID")
        self.validate_credentials()
        base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        super().__init__(base_url, headers)

    def validate_credentials(self):
        if not self.api_token or not self.account_id:
            raise ValueError("CF_API_TOKEN или CF_ACCOUNT_ID не найдены в .env")

    def get_service_name(self) -> str:
        return "Cloudflare AI"

    def generate_solution(self, task_text: str) -> str:
        payload = AIRequest(
            messages=[
                {"role": "system",
                 "content": "Ты — опытный проектный менеджер. Предложи 3–5 конкретных шагов для решения задачи. Формат: нумерованный список."
                 },
                {"role": "user",
                 "content": task_text
                 }
            ]
        )
        result = self._make_request("POST", "@cf/meta/llama-3-8b-instruct", json=payload.model_dump())
        ai_response = AIResponse(**result["result"])
        return ai_response.response