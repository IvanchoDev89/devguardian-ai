"""
0-Day Detection Model Training Pipeline
Trains ML models for vulnerability detection
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from typing import List, Dict, Tuple
import numpy as np
from datetime import datetime
import json
import os


class VulnerabilityTrainingPipeline:
    """
    Training pipeline for vulnerability detection models
    """
    
    def __init__(
        self,
        model,
        learning_rate: float = 1e-4,
        batch_size: int = 16,
        num_epochs: int = 10
    ):
        self.model = model
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        
        # Loss functions
        self.vuln_criterion = nn.BCELoss()
        self.anomaly_criterion = nn.MSELoss()
        self.severity_criterion = nn.CrossEntropyLoss()
        
        # Optimizer
        self.optimizer = optim.AdamW(
            self.model.parameters(),
            lr=learning_rate,
            weight_decay=0.01
        )
        
        # Learning rate scheduler
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode='min',
            patience=3,
            factor=0.5
        )
        
        self.training_history = {
            'train_loss': [],
            'val_loss': [],
            'train_accuracy': [],
            'val_accuracy': []
        }
    
    def generate_synthetic_data(
        self,
        num_samples: int = 1000
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Generate synthetic training data for vulnerability detection
        In production, use real labeled datasets
        """
        train_samples = []
        val_samples = []
        
        # Vulnerable code patterns
        vulnerable_patterns = [
            ("SELECT * FROM users WHERE id = " + "$id", "SQL Injection"),
            ('eval($_POST["cmd"])', "Code Injection"),
            ('system($_GET["cmd"])', "Command Injection"),
            ('innerHTML = $user_input', "XSS"),
            ('exec($command)', "Command Injection"),
            ('preg_replace($pattern, $replace, $input)', "Code Injection"),
            ('file_get_contents($filename)', "Path Traversal"),
            ('unserialize($data)', "Deserialization")
        ]
        
        # Safe code patterns
        safe_patterns = [
            "$stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?')",
            "const sanitized = encodeForHTML(userInput)",
            "const { execFile } = require('child_process')",
            "const safeCmd = allowedCommands.find(c => c === input)",
            "await queryBuilder.where('id', '=', userId).first()",
            "const escaped = db.escape(userInput)",
            "const cleanInput = input.replace(/[^a-zA-Z0-9]/g, '')",
            "const validated = validator.validate(userInput)"
        ]
        
        # Generate samples
        for i in range(num_samples):
            is_vulnerable = i % 2 == 0
            
            if is_vulnerable:
                pattern, vuln_type = vulnerable_patterns[i % len(vulnerable_patterns)]
                # Add some variations
                code = f"""<?php
function processUser($id) {{
    $user = db->query("SELECT * FROM users WHERE id = $id");
    return $user;
}}

function handleInput($input) {{
    echo $input;
}}

{pattern}
?>"""
            else:
                code = f"""<?php
function processUser($id) {{
    $stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?');
    $stmt->execute([$id]);
    return $stmt->fetch();
}}

function handleInput($input) {{
    echo htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
}}

{safe_patterns[i % len(safe_patterns)]}
?>"""
            
            sample = {
                'code': code,
                'is_vulnerable': is_vulnerable,
                'vulnerability_type': vulnerable_patterns[i % len(vulnerable_patterns)][1] if is_vulnerable else 'none'
            }
            
            if i < num_samples * 0.8:
                train_samples.append(sample)
            else:
                val_samples.append(sample)
        
        return train_samples, val_samples
    
    def train_epoch(self, train_loader: DataLoader) -> Dict:
        """Train for one epoch"""
        self.model.train()
        
        total_loss = 0
        correct = 0
        total = 0
        
        for batch in train_loader:
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['label'].to(self.device)
            
            self.optimizer.zero_grad()
            
            # Forward pass
            outputs = self.model(input_ids, attention_mask)
            
            # Calculate losses
            vuln_loss = self.vuln_criterion(
                outputs['vulnerability_probs'].squeeze(),
                labels
            )
            
            anomaly_loss = self.anomaly_detector_forward(
                outputs['embeddings'],
                labels
            )
            
            # Combined loss
            loss = vuln_loss + 0.3 * anomaly_loss
            
            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()
            
            total_loss += loss.item()
            
            # Calculate accuracy
            predictions = (outputs['vulnerability_probs'] > 0.5).float()
            correct += (predictions.squeeze() == labels).sum().item()
            total += labels.size(0)
        
        return {
            'loss': total_loss / len(train_loader),
            'accuracy': correct / total
        }
    
    def anomaly_detector_forward(self, embeddings, labels):
        """Forward pass for anomaly detector"""
        # Simplified anomaly detection loss
        # In production, use contrastive learning or autoencoder
        anomaly_scores = torch.randn(embeddings.size(0), device=self.device)
        return nn.functional.mse_loss(anomaly_scores, labels.float())
    
    def validate(self, val_loader: DataLoader) -> Dict:
        """Validate model"""
        self.model.eval()
        
        total_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['label'].to(self.device)
                
                outputs = self.model(input_ids, attention_mask)
                
                loss = self.vuln_criterion(
                    outputs['vulnerability_probs'].squeeze(),
                    labels
                )
                
                total_loss += loss.item()
                
                predictions = (outputs['vulnerability_probs'] > 0.5).float()
                correct += (predictions.squeeze() == labels).sum().item()
                total += labels.size(0)
        
        return {
            'loss': total_loss / len(val_loader),
            'accuracy': correct / total
        }
    
    def train(self, train_loader: DataLoader, val_loader: DataLoader):
        """Full training loop"""
        best_val_loss = float('inf')
        
        for epoch in range(self.num_epochs):
            print(f"\nEpoch {epoch + 1}/{self.num_epochs}")
            
            # Train
            train_metrics = self.train_epoch(train_loader)
            self.training_history['train_loss'].append(train_metrics['loss'])
            self.training_history['train_accuracy'].append(train_metrics['accuracy'])
            
            # Validate
            val_metrics = self.validate(val_loader)
            self.training_history['val_loss'].append(val_metrics['loss'])
            self.training_history['val_accuracy'].append(val_metrics['accuracy'])
            
            # Update scheduler
            self.scheduler.step(val_metrics['loss'])
            
            print(f"Train Loss: {train_metrics['loss']:.4f}, Accuracy: {train_metrics['accuracy']:.4f}")
            print(f"Val Loss: {val_metrics['loss']:.4f}, Accuracy: {val_metrics['accuracy']:.4f}")
            
            # Save best model
            if val_metrics['loss'] < best_val_loss:
                best_val_loss = val_metrics['loss']
                self.save_checkpoint(f'best_model_epoch_{epoch + 1}.pt')
                print("Saved best model!")
        
        return self.training_history
    
    def save_checkpoint(self, path: str):
        """Save model checkpoint"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'training_history': self.training_history
        }, path)
    
    def load_checkpoint(self, path: str):
        """Load model checkpoint"""
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        self.training_history = checkpoint.get('training_history', {})


class ZeroDayModelManager:
    """
    Manages multiple 0-day detection models
    """
    
    def __init__(self, models_dir: str = "./models"):
        self.models_dir = models_dir
        self.models = {}
        self.active_model = None
        
        os.makedirs(models_dir, exist_ok=True)
    
    def register_model(self, name: str, model, metadata: Dict = None):
        """Register a new model"""
        self.models[name] = {
            'model': model,
            'metadata': metadata or {},
            'created_at': datetime.now().isoformat()
        }
    
    def set_active_model(self, name: str):
        """Set the active model for inference"""
        if name in self.models:
            self.active_model = self.models[name]['model']
            return True
        return False
    
    def get_model_info(self, name: str) -> Dict:
        """Get model information"""
        if name in self.models:
            return self.models[name]['metadata']
        return {}
    
    def list_models(self) -> List[Dict]:
        """List all registered models"""
        return [
            {
                'name': name,
                'created_at': info['created_at'],
                'metadata': info['metadata']
            }
            for name, info in self.models.items()
        ]
    
    def export_model(self, name: str, path: str):
        """Export model to file"""
        if name in self.models:
            torch.save(self.models[name]['model'].state_dict(), path)
    
    def import_model(self, name: str, path: str):
        """Import model from file"""
        # Implementation depends on model architecture
        pass


def generate_training_report(history: Dict, output_path: str = "training_report.json"):
    """Generate training report"""
    report = {
        'training_date': datetime.now().isoformat(),
        'final_train_loss': history['train_loss'][-1] if history['train_loss'] else None,
        'final_val_loss': history['val_loss'][-1] if history['val_loss'] else None,
        'final_train_accuracy': history['train_accuracy'][-1] if history['train_accuracy'] else None,
        'final_val_accuracy': history['val_accuracy'][-1] if history['val_accuracy'] else None,
        'epochs_completed': len(history['train_loss']),
        'history': history
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    return report


if __name__ == "__main__":
    # Example training
    from zero_day_detector import CodeBERTVulnerabilityDetector, AnomalyDetector, CodeDataset
    from transformers import AutoTokenizer
    
    print("Initializing 0-Day Detection Model Training...")
    
    # Initialize model
    model = CodeBERTVulnerabilityDetector()
    
    # Initialize pipeline
    pipeline = VulnerabilityTrainingPipeline(
        model=model,
        learning_rate=1e-4,
        batch_size=8,
        num_epochs=5
    )
    
    # Generate synthetic data
    print("Generating synthetic training data...")
    train_samples, val_samples = pipeline.generate_synthetic_data(num_samples=500)
    
    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    
    # Create datasets
    train_dataset = CodeDataset(train_samples, tokenizer)
    val_dataset = CodeDataset(val_samples, tokenizer)
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=8)
    
    # Train
    print("Starting training...")
    history = pipeline.train(train_loader, val_loader)
    
    # Generate report
    print("Generating training report...")
    report = generate_training_report(history)
    print(f"Training complete! Report saved.")
    print(f"Final validation accuracy: {report['final_val_accuracy']:.2%}")
