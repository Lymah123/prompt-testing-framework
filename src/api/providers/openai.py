import openai
import os
from typing import Optional

class OpenAIProvider:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found")
        openai.api_key = self.api_key

    
    def generate(
        self,
        prompt: str,
        model: str = "gpt-4",
        system_prompt: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 1024
    ) -> str:
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content