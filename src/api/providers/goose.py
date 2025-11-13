import os
from typing import Optional
from .claude import ClaudeProvider
from .openai import OpenAIProvider

class GooseProvider:
    """
    Goose Provider - Routes to underlying model providers.
    
    Goose is a framework that uses Claude/OpenAI under the hood.
    This provider routes requests to the appropriate backend.
    
    Set GOOSE_BACKEND env var to 'claude' or 'openai' (default: claude)
    """
    
    def __init__(self, backend: Optional[str] = None):
        self.backend = backend or os.getenv("GOOSE_BACKEND", "claude")
        
        if self.backend == "claude":
            self.provider = ClaudeProvider()
        elif self.backend == "openai":
            self.provider = OpenAIProvider()
        else:
            raise ValueError(f"Unknown Goose backend: {self.backend}")
        
        print(f"🪿 Goose using backend: {self.backend}")
    
    def generate(
        self,
        prompt: str,
        model: str = "claude-sonnet-4-20250514",
        system_prompt: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 1024
    ) -> str:
        """
        Generate using Goose's underlying provider.
        
        Goose adds agentic capabilities, but for simple prompt testing
        we can route to the underlying model directly.
        """
        # Optionally enhance prompt with Goose-style instructions
        enhanced_prompt = prompt
        if system_prompt:
            enhanced_system = system_prompt
        else:
            enhanced_system = "You are Goose, a helpful AI assistant."
        
        return self.provider.generate(
            prompt=enhanced_prompt,
            model=model,
            system_prompt=enhanced_system,
            temperature=temperature,
            max_tokens=max_tokens
        )