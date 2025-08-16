"""
Cognitive Data Management System
Handles JSON storage, retrieval, and analysis of cognitive processing results
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import numpy as np
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class CognitiveAnalysisResult:
    """Structured representation of cognitive analysis results"""
    timestamp: str
    session_id: str
    input_data_hash: str
    
    # Circle Method Results
    major_arc_average: float
    minor_arc_average: float
    major_minor_ratio: float
    major_arc_count: int
    minor_arc_count: int
    
    # Laurent Expansion Results
    cognitive_zeta: float
    local_structure_richness: float
    laurent_coefficients: Dict[int, float]
    
    # Sieve Theory Results
    sieve_dimension: float
    filtered_data_count: int
    original_data_count: int
    twin_pairs_count: int
    retention_rate: float
    
    # Gap Analysis
    gaps_detected: int
    average_gap_size: float
    max_gap_size: float
    
    # Metadata
    processing_time_ms: float
    framework_version: str
    parameters: Dict[str, Any]

class CognitiveDataManager:
    """Manages storage and retrieval of cognitive analysis data"""
    
    def __init__(self, base_path: str = "data/cognitive_analysis"):
        """
        Initialize data manager
        
        Args:
            base_path: Base directory for storing cognitive data
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.results_path = self.base_path / "results"
        self.sessions_path = self.base_path / "sessions"
        self.exports_path = self.base_path / "exports"
        self.visualizations_path = self.base_path / "visualizations"
        
        for path in [self.results_path, self.sessions_path, 
                    self.exports_path, self.visualizations_path]:
            path.mkdir(exist_ok=True)
        
        self.framework_version = "1.0.0"
    
    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now(timezone.utc).isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:12]
    
    def compute_data_hash(self, data: List[float]) -> str:
        """Compute hash of input data for tracking"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def save_analysis_result(self, result: CognitiveAnalysisResult, 
                           session_name: Optional[str] = None) -> str:
        """
        Save cognitive analysis result to JSON
        
        Args:
            result: Analysis result to save
            session_name: Optional custom session name
            
        Returns:
            Path to saved file
        """
        # Generate filename
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        if session_name:
            filename = f"{session_name}_{timestamp}_{result.session_id}.json"
        else:
            filename = f"cognitive_analysis_{timestamp}_{result.session_id}.json"
        
        filepath = self.results_path / filename
        
        # Convert to dictionary and save
        result_dict = asdict(result)
        
        with open(filepath, 'w') as f:
            json.dump(result_dict, f, indent=2, default=self._json_serializer)
        
        print(f"Analysis result saved to: {filepath}")
        return str(filepath)
    
    def save_raw_data(self, data: List[float], metadata: Dict[str, Any], 
                     session_id: str) -> str:
        """
        Save raw cognitive input data
        
        Args:
            data: Raw cognitive data
            metadata: Additional metadata
            session_id: Session identifier
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        data_hash = self.compute_data_hash(data)
        
        raw_data = {
            "timestamp": timestamp,
            "session_id": session_id,
            "data_hash": data_hash,
            "data": data,
            "metadata": metadata,
            "data_stats": {
                "count": len(data),
                "mean": float(np.mean(data)),
                "std": float(np.std(data)),
                "min": float(np.min(data)),
                "max": float(np.max(data))
            }
        }
        
        filename = f"raw_data_{session_id}_{data_hash}.json"
        filepath = self.sessions_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(raw_data, f, indent=2, default=self._json_serializer)
        
        return str(filepath)
    
    def load_analysis_result(self, filepath: str) -> CognitiveAnalysisResult:
        """
        Load cognitive analysis result from JSON
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Loaded analysis result
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return CognitiveAnalysisResult(**data)
    
    def load_raw_data(self, filepath: str) -> Dict[str, Any]:
        """
        Load raw cognitive data from JSON
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Raw data dictionary
        """
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """
        List all available analysis sessions
        
        Returns:
            List of session information dictionaries
        """
        sessions = []
        
        for filepath in self.results_path.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                session_info = {
                    "filepath": str(filepath),
                    "filename": filepath.name,
                    "session_id": data.get("session_id", "unknown"),
                    "timestamp": data.get("timestamp", "unknown"),
                    "major_minor_ratio": data.get("major_minor_ratio", 0),
                    "cognitive_zeta": data.get("cognitive_zeta", 0),
                    "gaps_detected": data.get("gaps_detected", 0)
                }
                sessions.append(session_info)
                
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error reading {filepath}: {e}")
                continue
        
        # Sort by timestamp (newest first)
        sessions.sort(key=lambda x: x["timestamp"], reverse=True)
        return sessions
    
    def create_session_summary(self, session_ids: List[str]) -> Dict[str, Any]:
        """
        Create summary statistics across multiple sessions
        
        Args:
            session_ids: List of session IDs to include
            
        Returns:
            Summary statistics dictionary
        """
        results = []
        
        for filepath in self.results_path.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if data.get("session_id") in session_ids:
                    results.append(data)
                    
            except (json.JSONDecodeError, KeyError):
                continue
        
        if not results:
            return {"error": "No matching sessions found"}
        
        # Compute summary statistics
        summary = {
            "session_count": len(results),
            "date_range": {
                "earliest": min(r["timestamp"] for r in results),
                "latest": max(r["timestamp"] for r in results)
            },
            "statistics": {
                "major_minor_ratio": {
                    "mean": np.mean([r["major_minor_ratio"] for r in results]),
                    "std": np.std([r["major_minor_ratio"] for r in results]),
                    "min": min(r["major_minor_ratio"] for r in results),
                    "max": max(r["major_minor_ratio"] for r in results)
                },
                "cognitive_zeta": {
                    "mean": np.mean([r["cognitive_zeta"] for r in results]),
                    "std": np.std([r["cognitive_zeta"] for r in results]),
                    "min": min(r["cognitive_zeta"] for r in results),
                    "max": max(r["cognitive_zeta"] for r in results)
                },
                "local_structure_richness": {
                    "mean": np.mean([r["local_structure_richness"] for r in results]),
                    "std": np.std([r["local_structure_richness"] for r in results]),
                    "min": min(r["local_structure_richness"] for r in results),
                    "max": max(r["local_structure_richness"] for r in results)
                },
                "sieve_dimension": {
                    "mean": np.mean([r["sieve_dimension"] for r in results]),
                    "std": np.std([r["sieve_dimension"] for r in results]),
                    "min": min(r["sieve_dimension"] for r in results),
                    "max": max(r["sieve_dimension"] for r in results)
                }
            },
            "trends": self._compute_trends(results)
        }
        
        return summary
    
    def export_to_csv(self, session_ids: List[str], 
                     output_path: Optional[str] = None) -> str:
        """
        Export analysis results to CSV format
        
        Args:
            session_ids: List of session IDs to export
            output_path: Optional output path
            
        Returns:
            Path to exported CSV file
        """
        import pandas as pd
        
        results = []
        
        for filepath in self.results_path.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if data.get("session_id") in session_ids:
                    # Flatten nested dictionaries
                    flattened = self._flatten_dict(data)
                    results.append(flattened)
                    
            except (json.JSONDecodeError, KeyError):
                continue
        
        if not results:
            raise ValueError("No matching sessions found for export")
        
        # Create DataFrame and export
        df = pd.DataFrame(results)
        
        if output_path is None:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            output_path = self.exports_path / f"cognitive_analysis_export_{timestamp}.csv"
        
        df.to_csv(output_path, index=False)
        print(f"Data exported to: {output_path}")
        return str(output_path)
    
    def backup_data(self, backup_path: Optional[str] = None) -> str:
        """
        Create backup of all cognitive analysis data
        
        Args:
            backup_path: Optional backup directory path
            
        Returns:
            Path to backup directory
        """
        import shutil
        
        if backup_path is None:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_cognitive_data_{timestamp}"
        
        backup_dir = Path(backup_path)
        
        # Copy entire data directory
        shutil.copytree(self.base_path, backup_dir, dirs_exist_ok=True)
        
        print(f"Data backed up to: {backup_dir}")
        return str(backup_dir)
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for numpy types"""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', 
                     sep: str = '_') -> Dict[str, Any]:
        """Flatten nested dictionary for CSV export"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _compute_trends(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compute trend analysis across sessions"""
        # Sort by timestamp
        sorted_results = sorted(results, key=lambda x: x["timestamp"])
        
        if len(sorted_results) < 2:
            return {"error": "Need at least 2 sessions for trend analysis"}
        
        # Compute simple linear trends
        n = len(sorted_results)
        x = np.arange(n)
        
        trends = {}
        metrics = ["major_minor_ratio", "cognitive_zeta", 
                  "local_structure_richness", "sieve_dimension"]
        
        for metric in metrics:
            y = [r[metric] for r in sorted_results]
            
            # Simple linear regression
            slope = np.polyfit(x, y, 1)[0]
            
            trends[metric] = {
                "slope": float(slope),
                "direction": "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable",
                "magnitude": "strong" if abs(slope) > 0.1 else "moderate" if abs(slope) > 0.01 else "weak"
            }
        
        return trends

class CognitiveDataAnalyzer:
    """Advanced analysis tools for stored cognitive data"""
    
    def __init__(self, data_manager: CognitiveDataManager):
        self.data_manager = data_manager
    
    def find_similar_sessions(self, target_session_id: str, 
                            similarity_threshold: float = 0.8) -> List[Dict[str, Any]]:
        """
        Find sessions similar to target session based on analysis results
        
        Args:
            target_session_id: Session to find similarities for
            similarity_threshold: Minimum similarity score (0-1)
            
        Returns:
            List of similar sessions with similarity scores
        """
        # Load target session
        target_data = None
        for filepath in self.data_manager.results_path.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                if data.get("session_id") == target_session_id:
                    target_data = data
                    break
            except (json.JSONDecodeError, KeyError):
                continue
        
        if target_data is None:
            return []
        
        # Compare with all other sessions
        similar_sessions = []
        metrics = ["major_minor_ratio", "cognitive_zeta", 
                  "local_structure_richness", "sieve_dimension"]
        
        for filepath in self.data_manager.results_path.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if data.get("session_id") == target_session_id:
                    continue  # Skip self
                
                # Compute similarity score
                similarity = self._compute_similarity(target_data, data, metrics)
                
                if similarity >= similarity_threshold:
                    similar_sessions.append({
                        "session_id": data.get("session_id"),
                        "timestamp": data.get("timestamp"),
                        "similarity_score": similarity,
                        "filepath": str(filepath)
                    })
                    
            except (json.JSONDecodeError, KeyError):
                continue
        
        # Sort by similarity score (highest first)
        similar_sessions.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similar_sessions
    
    def detect_anomalies(self, window_size: int = 10) -> List[Dict[str, Any]]:
        """
        Detect anomalous sessions based on statistical analysis
        
        Args:
            window_size: Size of rolling window for anomaly detection
            
        Returns:
            List of anomalous sessions
        """
        sessions = self.data_manager.list_sessions()
        
        if len(sessions) < window_size:
            return []
        
        anomalies = []
        metrics = ["major_minor_ratio", "cognitive_zeta", 
                  "local_structure_richness", "sieve_dimension"]
        
        # Load all session data
        session_data = []
        for session in sessions:
            try:
                with open(session["filepath"], 'r') as f:
                    data = json.load(f)
                session_data.append(data)
            except (json.JSONDecodeError, KeyError):
                continue
        
        # Compute rolling statistics and detect anomalies
        for i in range(window_size, len(session_data)):
            window_data = session_data[i-window_size:i]
            current_data = session_data[i]
            
            anomaly_scores = {}
            is_anomaly = False
            
            for metric in metrics:
                window_values = [d[metric] for d in window_data]
                current_value = current_data[metric]
                
                mean_val = np.mean(window_values)
                std_val = np.std(window_values)
                
                if std_val > 0:
                    z_score = abs(current_value - mean_val) / std_val
                    anomaly_scores[metric] = z_score
                    
                    if z_score > 2.5:  # Anomaly threshold
                        is_anomaly = True
            
            if is_anomaly:
                anomalies.append({
                    "session_id": current_data.get("session_id"),
                    "timestamp": current_data.get("timestamp"),
                    "anomaly_scores": anomaly_scores,
                    "max_z_score": max(anomaly_scores.values()),
                    "filepath": sessions[i]["filepath"]
                })
        
        # Sort by maximum z-score (most anomalous first)
        anomalies.sort(key=lambda x: x["max_z_score"], reverse=True)
        return anomalies
    
    def _compute_similarity(self, data1: Dict[str, Any], data2: Dict[str, Any], 
                          metrics: List[str]) -> float:
        """Compute similarity score between two sessions"""
        similarities = []
        
        for metric in metrics:
            val1 = data1.get(metric, 0)
            val2 = data2.get(metric, 0)
            
            # Compute normalized similarity (1 - normalized absolute difference)
            max_val = max(abs(val1), abs(val2), 1e-10)  # Avoid division by zero
            similarity = 1.0 - abs(val1 - val2) / max_val
            similarities.append(similarity)
        
        return np.mean(similarities)
