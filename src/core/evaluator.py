import re
from typing import List, Dict, Any
from src.core.models import Expectation, EvaluationType

class Evaluator:
    @staticmethod
    def evaluate(response: str, expectations: List[Expectation]) -> tuple[bool, List[Dict[str, Any]]]:
        """
        Evaluate a response against expectations.
        Returns (overall_passed, detailed_results)
        """
        if not expectations:
            return None, []  # No expectations = manual review needed
        
        results = []
        all_passed = True
        
        for exp in expectations:
            result = Evaluator._evaluate_single(response, exp)
            results.append(result)
            if not result['passed']:
                all_passed = False
        
        return all_passed, results
    
    @staticmethod
    def _evaluate_single(response: str, expectation: Expectation) -> Dict[str, Any]:
        result = {
            'type': expectation.type,
            'description': expectation.description or f"{expectation.type}: {expectation.value}",
            'passed': False,
            'details': ''
        }
        
        if expectation.type == EvaluationType.CONTAINS:
            result['passed'] = expectation.value.lower() in response.lower()
            result['details'] = f"Looking for: '{expectation.value}'"
        
        elif expectation.type == EvaluationType.NOT_CONTAINS:
            result['passed'] = expectation.value.lower() not in response.lower()
            result['details'] = f"Should not contain: '{expectation.value}'"
        
        elif expectation.type == EvaluationType.REGEX:
            match = re.search(expectation.value, response)
            result['passed'] = match is not None
            result['details'] = f"Pattern: {expectation.value}"
        
        elif expectation.type == EvaluationType.LENGTH_MIN:
            result['passed'] = len(response) >= expectation.value
            result['details'] = f"Min length: {expectation.value}, Actual: {len(response)}"
        
        elif expectation.type == EvaluationType.LENGTH_MAX:
            result['passed'] = len(response) <= expectation.value
            result['details'] = f"Max length: {expectation.value}, Actual: {len(response)}"
        
        elif expectation.type == EvaluationType.MANUAL:
            result['passed'] = None  # Requires manual review
            result['details'] = "Manual review required"
        
        return result