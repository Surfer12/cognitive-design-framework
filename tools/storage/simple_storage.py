"""
Simple JSON Storage for Cognitive Analysis Results
Basic save/load functionality for cognitive data
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class SimpleCognitiveStorage:
    """Basic storage for cognitive analysis results"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def save_results(self, results: Dict[str, Any], 
                    session_name: str = None) -> str:
        """Save analysis results to JSON file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if session_name:
            filename = f"{session_name}_{timestamp}.json"
        else:
            filename = f"cognitive_results_{timestamp}.json"
        
        filepath = self.data_dir / filename
        
        # Add metadata
        results_with_meta = {
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        
        with open(filepath, 'w') as f:
            json.dump(results_with_meta, f, indent=2)
        
        print(f"Results saved to: {filepath}")
        return str(filepath)
    
    def load_results(self, filepath: str) -> Dict[str, Any]:
        """Load results from JSON file"""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def list_saved_results(self) -> List[str]:
        """List all saved result files"""
        return [str(f) for f in self.data_dir.glob("*.json")]
