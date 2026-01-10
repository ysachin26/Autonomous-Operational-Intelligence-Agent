"""
AOIA ML Engine - Anomaly Detection Service
Uses Isolation Forest for outlier detection.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Dict, Any, Optional
from datetime import datetime


class AnomalyDetector:
    """
    Anomaly detection service using Isolation Forest algorithm.
    Designed for real-time operational metric analysis.
    """
    
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42,
        )
        self.is_trained = False
        self.thresholds = {
            "UTILIZATION": {"low": 40, "high": 95},
            "THROUGHPUT": {"low": 60, "high": None},
            "IDLE_TIME": {"low": None, "high": 20},
            "RESPONSE_TIME": {"low": None, "high": 500},
            "QUALITY_SCORE": {"low": 85, "high": None},
            "DOWNTIME": {"low": None, "high": 10},
            "CALL_DURATION": {"low": None, "high": 600},
            "TASK_COMPLETION": {"low": 80, "high": None},
            "MACHINE_SPEED": {"low": 70, "high": None},
            "ERROR_RATE": {"low": None, "high": 5},
        }
    
    def detect_batch(
        self, 
        metrics: List[Any], 
        sensitivity: float = 0.8
    ) -> List[Dict[str, Any]]:
        """
        Detect anomalies in a batch of metrics.
        
        Args:
            metrics: List of MetricData objects
            sensitivity: Detection sensitivity (0-1)
        
        Returns:
            List of detection results
        """
        results = []
        
        # Group metrics by type for contextual analysis
        by_type: Dict[str, List[Any]] = {}
        for metric in metrics:
            mtype = metric.metric_type
            if mtype not in by_type:
                by_type[mtype] = []
            by_type[mtype].append(metric)
        
        for metric in metrics:
            mtype = metric.metric_type
            values = [m.value for m in by_type[mtype]]
            
            # Calculate statistics
            mean_val = np.mean(values)
            std_val = np.std(values) if len(values) > 1 else 0
            
            # Determine if anomaly using multiple methods
            is_anomaly = False
            score = 0.0
            
            # Method 1: Threshold-based
            thresholds = self.thresholds.get(mtype, {})
            if thresholds.get("low") and metric.value < thresholds["low"]:
                is_anomaly = True
                score = max(score, 0.7)
            if thresholds.get("high") and metric.value > thresholds["high"]:
                is_anomaly = True
                score = max(score, 0.7)
            
            # Method 2: Statistical (z-score)
            if std_val > 0:
                z_score = abs(metric.value - mean_val) / std_val
                if z_score > (3 - sensitivity * 1.5):  # Adjust threshold based on sensitivity
                    is_anomaly = True
                    score = max(score, min(1.0, z_score / 4))
            
            if is_anomaly:
                deviation = ((metric.value - mean_val) / mean_val * 100) if mean_val != 0 else 0
                severity = self._calculate_severity(score, deviation)
                
                results.append({
                    "is_anomaly": True,
                    "score": round(score, 3),
                    "severity": severity,
                    "description": self._generate_description(metric, deviation),
                    "expected_value": round(mean_val, 2),
                    "deviation_percent": round(deviation, 2),
                    "metric": metric,
                })
        
        return results
    
    def detect_single(
        self, 
        metric: Any, 
        context: List[float]
    ) -> Dict[str, Any]:
        """
        Detect anomaly for a single metric with optional context.
        
        Args:
            metric: Single MetricData object
            context: Recent values for comparison
        
        Returns:
            Detection result
        """
        mtype = metric.metric_type
        value = metric.value
        
        # Use context if available, otherwise use thresholds
        if context and len(context) >= 5:
            mean_val = np.mean(context)
            std_val = np.std(context)
            z_score = abs(value - mean_val) / std_val if std_val > 0 else 0
            is_anomaly = z_score > 2.5
            score = min(1.0, z_score / 4)
        else:
            # Threshold-based detection
            thresholds = self.thresholds.get(mtype, {})
            is_anomaly = False
            score = 0.0
            mean_val = value
            
            if thresholds.get("low") and value < thresholds["low"]:
                is_anomaly = True
                score = 0.6 + (thresholds["low"] - value) / thresholds["low"] * 0.4
                mean_val = thresholds["low"]
            elif thresholds.get("high") and value > thresholds["high"]:
                is_anomaly = True
                score = 0.6 + (value - thresholds["high"]) / thresholds["high"] * 0.4
                mean_val = thresholds["high"]
        
        deviation = ((value - mean_val) / mean_val * 100) if mean_val != 0 else 0
        severity = self._calculate_severity(score, deviation)
        
        result = {
            "is_anomaly": is_anomaly,
            "score": round(min(1.0, score), 3),
            "severity": severity,
            "description": self._generate_description(metric, deviation) if is_anomaly else "Normal operations",
        }
        
        if is_anomaly:
            result["recommendation"] = self._generate_recommendation(mtype, deviation)
        
        return result
    
    def train(self, metrics: List[Any]) -> bool:
        """
        Train the Isolation Forest model on historical data.
        
        Args:
            metrics: Historical metrics for training
        
        Returns:
            Success status
        """
        try:
            # Prepare feature matrix
            values = np.array([m.value for m in metrics]).reshape(-1, 1)
            
            # Fit the model
            self.model.fit(values)
            self.is_trained = True
            
            return True
        except Exception as e:
            print(f"Training error: {e}")
            return False
    
    def _calculate_severity(self, score: float, deviation: float) -> str:
        """Calculate severity based on anomaly score and deviation."""
        abs_dev = abs(deviation)
        
        if score > 0.9 or abs_dev > 50:
            return "CRITICAL"
        elif score > 0.7 or abs_dev > 30:
            return "HIGH"
        elif score > 0.5 or abs_dev > 15:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_description(self, metric: Any, deviation: float) -> str:
        """Generate human-readable description of the anomaly."""
        mtype = metric.metric_type.replace("_", " ").lower()
        source = metric.source
        direction = "above" if deviation > 0 else "below"
        
        descriptions = {
            "UTILIZATION": f"Utilization on {source} is {abs(deviation):.1f}% {direction} normal",
            "THROUGHPUT": f"Throughput drop detected on {source} ({abs(deviation):.1f}% {direction} expected)",
            "IDLE_TIME": f"Idle time spike on {source} ({abs(deviation):.1f}% {direction} baseline)",
            "RESPONSE_TIME": f"Response time delay on {source} ({abs(deviation):.1f}% slower)",
            "QUALITY_SCORE": f"Quality decline on {source} ({abs(deviation):.1f}% below target)",
            "DOWNTIME": f"Downtime alert on {source}",
            "MACHINE_SPEED": f"Machine slowdown on {source} ({abs(deviation):.1f}% below optimal)",
        }
        
        return descriptions.get(
            metric.metric_type, 
            f"Anomaly detected on {source}: {mtype} is {abs(deviation):.1f}% {direction} expected"
        )
    
    def _generate_recommendation(self, mtype: str, deviation: float) -> str:
        """Generate actionable recommendation based on anomaly type."""
        recommendations = {
            "UTILIZATION": "Review workload distribution and consider rebalancing",
            "THROUGHPUT": "Investigate bottlenecks and check for resource constraints",
            "IDLE_TIME": "Analyze workflow gaps and optimize task scheduling",
            "RESPONSE_TIME": "Check system performance and network latency",
            "QUALITY_SCORE": "Review quality controls and calibration settings",
            "DOWNTIME": "Schedule maintenance check and review error logs",
            "MACHINE_SPEED": "Inspect mechanical components and calibrate settings",
            "OVERLOAD": "Redistribute workload or add temporary resources",
        }
        
        return recommendations.get(mtype, "Review operational parameters and investigate root cause")
