# AI Service Models Directory

This directory contains pre-trained models for the DevGuardian AI service.

## Model Files

- `security_classifier.pkl` - Security vulnerability classification model
- `code_analyzer.pkl` - Code analysis and pattern detection model
- `threat_detector.pkl` - Threat intelligence and anomaly detection model

## Model Loading

Models are loaded automatically by the ML detector service:

```python
from app.core.services.ml_detector import SecurityMLDetector

# Initialize with model loading
detector = SecurityMLDetector()
detector.load_models()
```

## Model Training

Models can be trained using the training endpoint:

```bash
curl -X POST http://localhost:8000/api/security/train/models \
  -H "Content-Type: application/json" \
  -d '{"model_directory": "models"}'
```

## Model Format

- Format: Pickle (.pkl) files
- Framework: PyTorch + scikit-learn
- Version: v1.0
- Last Updated: 2026-01-16
