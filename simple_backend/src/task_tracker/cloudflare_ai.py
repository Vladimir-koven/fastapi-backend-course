import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv('passwords.env')

class AIRequest(BaseModel):
    messages: list

class AIResponse(BaseModel):
    response: str

class CloudflareAI:
    def __init__(self):
        self.api_token = os.getenv("CF_API_TOKEN")
        self.account_id = os.getenv("CF_ACCOUNT_ID")
        if not self.api_token or not self.account_id:
            raise ValueError("CF_API_TOKEN или CF_ACCOUNT_ID не найдены в .env")
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/"

    def generate_solution(self, task_text: str) -> str:
        """Отправка текста задачи в LLM - модель"""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
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
        try:
            response = requests.post(
                self.base_url + "@cf/meta/llama-3-8b-instruct",
                json=payload.model_dump(),  # Преобразуем в dict
                headers=headers,
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                ai_response = AIResponse(**result["result"])
                return ai_response.response
            else:
                raise Exception(f"Ошибка Cloudflare AI: {response.status_code} {response.text}")
        except requests.RequestException as e:
            raise Exception(f"Сетевой сбой: {e}")