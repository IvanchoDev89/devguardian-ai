import torch
import torch.nn as nn
import numpy as np
from typing import List, Dict, Any, Tuple
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import joblib
import os
from datetime import datetime

class SecurityMLDetector:
    """Machine Learning-based security threat detector"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.clustering_model = DBSCAN(eps=0.5, min_samples=5)
        self.model_trained = False
        
        # Neural network for pattern recognition
        self.pattern_classifier = self._build_pattern_classifier()
        
    def _build_pattern_classifier(self) -> nn.Module:
        """Build neural network for security pattern classification"""
        class SecurityPatternNet(nn.Module):
            def __init__(self, input_size: int = 100, hidden_size: int = 256, num_classes: int = 7):
                super(SecurityPatternNet, self).__init__()
                self.network = nn.Sequential(
                    nn.Linear(input_size, hidden_size),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(hidden_size, hidden_size // 2),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(hidden_size // 2, num_classes),
                    nn.Softmax(dim=1)
                )
            
            def forward(self, x):
                return self.network(x)
        
        return SecurityPatternNet().to(self.device)
    
    def extract_features(self, code_content: str, file_path: str = "") -> np.ndarray:
        """Extract features from code for ML analysis"""
        features = []
        
        # Code complexity features
        lines = code_content.split('\n')
        features.append(len(lines))  # Number of lines
        features.append(len(code_content))  # Total characters
        features.append(sum(len(line) for line in lines) / len(lines))  # Average line length
        
        # Security-sensitive keywords
        security_keywords = [
            'password', 'secret', 'key', 'token', 'auth', 'login', 'exec',
            'eval', 'system', 'shell', 'cmd', 'sql', 'query', 'database',
            'file', 'read', 'write', 'upload', 'download', 'include', 'require'
        ]
        
        for keyword in security_keywords:
            features.append(code_content.lower().count(keyword))
        
        # Code structure features
        features.append(code_content.count('('))  # Function calls
        features.append(code_content.count('{'))  # Code blocks
        features.append(code_content.count(';'))  # Statements
        features.append(code_content.count('"') + code_content.count("'"))  # String literals
        
        # Risk indicators
        risk_patterns = [
            'http://', 'https://', 'ftp://',  # URLs
            '<?php', '<%', '<script',  # Script tags
            'SELECT', 'INSERT', 'UPDATE', 'DELETE',  # SQL
            'eval(', 'exec(', 'system(',  # Dangerous functions
        ]
        
        for pattern in risk_patterns:
            features.append(code_content.upper().count(pattern))
        
        # File extension risk
        file_extensions = ['.php', '.js', '.py', '.rb', '.pl', '.sh', '.bat']
        ext_features = [1 if file_path.endswith(ext) else 0 for ext in file_extensions]
        features.extend(ext_features)
        
        # Pad or truncate to fixed size
        feature_array = np.array(features, dtype=np.float32)
        if len(feature_array) < 100:
            feature_array = np.pad(feature_array, (0, 100 - len(feature_array)))
        elif len(feature_array) > 100:
            feature_array = feature_array[:100]
        
        return feature_array
    
    def detect_anomalies(self, features: np.ndarray) -> Dict[str, Any]:
        """Detect anomalous patterns in code"""
        if not self.model_trained:
            # Train on the current data if not trained
            self.anomaly_detector.fit(features.reshape(1, -1))
            self.model_trained = True
        
        # Predict anomalies
        anomaly_score = self.anomaly_detector.decision_function(features.reshape(1, -1))[0]
        is_anomaly = self.anomaly_detector.predict(features.reshape(1, -1))[0] == -1
        
        return {
            'is_anomaly': bool(is_anomaly),
            'anomaly_score': float(anomaly_score),
            'risk_level': 'high' if is_anomaly else 'normal'
        }
    
    def classify_security_patterns(self, features: np.ndarray) -> Dict[str, Any]:
        """Classify security patterns using neural network"""
        # Normalize features
        if not self.model_trained:
            features_normalized = features.reshape(1, -1)
        else:
            features_normalized = self.scaler.transform(features.reshape(1, -1))
        
        # Convert to tensor
        features_tensor = torch.FloatTensor(features_normalized).to(self.device)
        
        # Predict
        with torch.no_grad():
            self.pattern_classifier.eval()
            predictions = self.pattern_classifier(features_tensor)
            predicted_class = torch.argmax(predictions, dim=1).item()
            confidence = torch.max(predictions).item()
        
        # Map class to vulnerability type
        vulnerability_types = [
            'sql_injection', 'xss', 'path_traversal', 'command_injection',
            'insecure_deserialization', 'hardcoded_credentials', 'weak_crypto'
        ]
        
        predicted_vulnerability = vulnerability_types[predicted_class] if predicted_class < len(vulnerability_types) else 'unknown'
        
        return {
            'predicted_type': predicted_vulnerability,
            'confidence': float(confidence),
            'all_probabilities': predictions.cpu().numpy().tolist()[0]
        }
    
    def analyze_code_batch(self, code_samples: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze multiple code samples"""
        all_features = []
        results = []
        
        for sample in code_samples:
            features = self.extract_features(sample['content'], sample.get('file_path', ''))
            all_features.append(features)
            
            # Individual analysis
            anomaly_result = self.detect_anomalies(features)
            pattern_result = self.classify_security_patterns(features)
            
            result = {
                'file_path': sample.get('file_path', ''),
                'anomaly_detection': anomaly_result,
                'pattern_classification': pattern_result,
                'timestamp': datetime.now().isoformat()
            }
            results.append(result)
        
        # Batch analysis
        all_features_array = np.array(all_features)
        
        # Train models if not trained
        if not self.model_trained:
            self.scaler.fit(all_features_array)
            self.anomaly_detector.fit(all_features_array)
            self.model_trained = True
        
        # Clustering analysis
        clustering_labels = self.clustering_model.fit_predict(all_features_array)
        
        # Add clustering results
        for i, result in enumerate(results):
            result['cluster_id'] = int(clustering_labels[i])
            result['is_outlier'] = clustering_labels[i] == -1
        
        # Summary statistics
        summary = {
            'total_samples': len(code_samples),
            'anomalies_detected': sum(1 for r in results if r['anomaly_detection']['is_anomaly']),
            'outliers_detected': sum(1 for r in results if r['is_outlier']),
            'most_common_pattern': self._get_most_common_pattern(results),
            'average_confidence': np.mean([r['pattern_classification']['confidence'] for r in results])
        }
        
        return {
            'summary': summary,
            'individual_results': results,
            'clustering_analysis': {
                'num_clusters': len(set(clustering_labels)) - (1 if -1 in clustering_labels else 0),
                'cluster_sizes': {int(label): int(list(clustering_labels).count(label)) 
                                for label in set(clustering_labels)}
            }
        }
    
    def _get_most_common_pattern(self, results: List[Dict[str, Any]]) -> str:
        """Get the most commonly detected security pattern"""
        patterns = [r['pattern_classification']['predicted_type'] for r in results]
        if patterns:
            return max(set(patterns), key=patterns.count)
        return 'none'
    
    def train_model(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train the ML models with provided data"""
        # Extract features from training data
        training_features = []
        training_labels = []
        
        for data_point in training_data:
            features = self.extract_features(data_point['content'], data_point.get('file_path', ''))
            training_features.append(features)
            training_labels.append(data_point.get('label', 0))  # 0 for safe, 1 for vulnerable
        
        # Convert to arrays
        X = np.array(training_features)
        y = np.array(training_labels)
        
        # Train scaler
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        
        # Train anomaly detector
        self.anomaly_detector.fit(X_scaled)
        
        # Train neural network (if we have labeled data)
        if len(set(y)) > 1:  # Only train if we have multiple classes
            X_tensor = torch.FloatTensor(X_scaled).to(self.device)
            y_tensor = torch.LongTensor(y).to(self.device)
            
            # Simple training loop
            criterion = nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(self.pattern_classifier.parameters(), lr=0.001)
            
            self.pattern_classifier.train()
            for epoch in range(100):  # Simple training
                optimizer.zero_grad()
                outputs = self.pattern_classifier(X_tensor)
                loss = criterion(outputs, y_tensor)
                loss.backward()
                optimizer.step()
        
        self.model_trained = True
        
        return {
            'training_samples': len(training_data),
            'features_extracted': X.shape[1],
            'model_trained': True,
            'training_accuracy': self._evaluate_training(X_scaled, y)
        }
    
    def _evaluate_training(self, X: np.ndarray, y: np.ndarray) -> float:
        """Evaluate model training accuracy"""
        predictions = self.anomaly_detector.predict(X)
        accuracy = np.mean(predictions == y)
        return float(accuracy)
    
    def save_models(self, model_dir: str = "models") -> Dict[str, str]:
        """Save trained models"""
        os.makedirs(model_dir, exist_ok=True)
        
        # Save models
        joblib.dump(self.scaler, f"{model_dir}/scaler.pkl")
        joblib.dump(self.anomaly_detector, f"{model_dir}/anomaly_detector.pkl")
        joblib.dump(self.clustering_model, f"{model_dir}/clustering_model.pkl")
        torch.save(self.pattern_classifier.state_dict(), f"{model_dir}/pattern_classifier.pth")
        
        return {
            'scaler': f"{model_dir}/scaler.pkl",
            'anomaly_detector': f"{model_dir}/anomaly_detector.pkl",
            'clustering_model': f"{model_dir}/clustering_model.pkl",
            'pattern_classifier': f"{model_dir}/pattern_classifier.pth"
        }
    
    def load_models(self, model_dir: str = "models") -> bool:
        """Load pre-trained models"""
        try:
            self.scaler = joblib.load(f"{model_dir}/scaler.pkl")
            self.anomaly_detector = joblib.load(f"{model_dir}/anomaly_detector.pkl")
            self.clustering_model = joblib.load(f"{model_dir}/clustering_model.pkl")
            self.pattern_classifier.load_state_dict(torch.load(f"{model_dir}/pattern_classifier.pth"))
            self.model_trained = True
            return True
        except FileNotFoundError:
            return False
