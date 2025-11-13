import anthropic
import os
from typing import Optional

class ClaudeProvider:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def generate(
        self,
        prompt: str,
        model: str = "claude-sonnet-4-20250514",
        system_prompt: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 1024
    ) -> str:
        messages = [{"role": "user", "content": prompt}]
        
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        response = self.client.messages.create(**kwargs)
        return response.content[0].text