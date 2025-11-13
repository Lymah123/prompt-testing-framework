import json
import os
from typing import List, Optional
from pathlib import Path
from src.core.models import TestCase, TestResult

class StorageManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.test_cases_file = self.data_dir / "test_cases.json"
        self.results_file = self.data_dir / "results.json"
        
        # Initialize files if they don't exist
        if not self.test_cases_file.exists():
            self._save_json(self.test_cases_file, [])
        if not self.results_file.exists():
            self._save_json(self.results_file, [])
    
    def _save_json(self, filepath: Path, data: List):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_json(self, filepath: Path) -> List:
        with open(filepath, 'r') as f:
            return json.load(f)
    
    # Test Cases
    def save_test_case(self, test_case: TestCase):
        cases = self.get_all_test_cases()
        # Remove existing case with same ID
        cases = [c for c in cases if c.get('id') != test_case.id]
        cases.append(test_case.model_dump())
        self._save_json(self.test_cases_file, cases)
    
    def get_all_test_cases(self) -> List[dict]:
        return self._load_json(self.test_cases_file)
    
    def get_test_case(self, test_id: str) -> Optional[dict]:
        cases = self.get_all_test_cases()
        return next((c for c in cases if c['id'] == test_id), None)
    
    def delete_test_case(self, test_id: str):
        cases = [c for c in self.get_all_test_cases() if c['id'] != test_id]
        self._save_json(self.test_cases_file, cases)
    
    # Results
    def save_result(self, result: TestResult):
        results = self._load_json(self.results_file)
        results.append(result.model_dump())
        self._save_json(self.results_file, results)
    
    def get_all_results(self) -> List[dict]:
        return self._load_json(self.results_file)
    
    def get_results_for_test(self, test_id: str) -> List[dict]:
        results = self.get_all_results()
        return [r for r in results if r['test_id'] == test_id]