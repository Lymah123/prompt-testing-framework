import time
from typing import Optional
from src.core.models import TestCase, TestResult
from src.core.evaluator import Evaluator
from src.api.providers.claude import ClaudeProvider
from src.api.providers.goose import GooseProvider

class TestRunner:
    def __init__(self):
        self.evaluator = Evaluator()
        self.providers = {}
    
    def _get_provider(self, provider_name: str):
       if provider_name not in self.providers:
           if provider_name == "claude":
                self.providers[provider_name] = ClaudeProvider()
           elif provider_name == "openai":
                self.providers[provider_name] = OpenAIProvider()
           elif provider_name == "goose":  
                self.providers[provider_name] = GooseProvider()
           else:
                raise ValueError(f"Unknown provider: {provider_name}")
       return self.providers[provider_name]
    
    def run_test(self, test_case: TestCase) -> TestResult:
        """Execute a single test case"""
        start_time = time.time()
        
        try:
            provider = self._get_provider(test_case.provider)
            
            response = provider.generate(
                prompt=test_case.prompt,
                model=test_case.model,
                system_prompt=test_case.system_prompt,
                temperature=test_case.temperature,
                max_tokens=test_case.max_tokens
            )
            
            execution_time = time.time() - start_time
            
            # Evaluate response
            passed, evaluation_results = self.evaluator.evaluate(
                response, test_case.expectations
            )
            
            return TestResult(
                test_id=test_case.id,
                test_name=test_case.name,
                prompt=test_case.prompt,
                response=response,
                provider=test_case.provider,
                model=test_case.model,
                passed=passed,
                evaluation_results=evaluation_results,
                execution_time=execution_time
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                test_id=test_case.id,
                test_name=test_case.name,
                prompt=test_case.prompt,
                response="",
                provider=test_case.provider,
                model=test_case.model,
                passed=False,
                evaluation_results=[],
                execution_time=execution_time,
                error=str(e)
            )