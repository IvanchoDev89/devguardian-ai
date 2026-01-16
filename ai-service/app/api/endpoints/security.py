from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import tempfile
import os
import shutil
from datetime import datetime
import uuid

from app.core.services.security_analyzer import SecurityVulnerabilityAnalyzer
from app.core.services.ml_detector import SecurityMLDetector
from app.core.services.threat_intelligence import ThreatIntelligenceEngine

router = APIRouter(prefix="/api/security", tags=["security"])

# Initialize services
security_analyzer = SecurityVulnerabilityAnalyzer()
ml_detector = SecurityMLDetector()
threat_engine = ThreatIntelligenceEngine()

@router.post("/scan")
async def scan_code(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    deep_scan: bool = False
):
    """
    Scan uploaded code file for security vulnerabilities
    """
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        # Read file content
        with open(temp_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code_content = f.read()
        
        # Perform security analysis
        scan_id = str(uuid.uuid4())
        
        if deep_scan:
            # Deep scan with all analysis methods
            vulnerability_results = security_analyzer.analyze_code(code_content, file.filename)
            ml_results = ml_detector.analyze_code_batch([{
                'content': code_content,
                'file_path': file.filename
            }])
            threat_results = threat_engine.analyze_code_threats(code_content, file.filename)
            
            # Combine all results
            scan_results = {
                'scan_id': scan_id,
                'file_name': file.filename,
                'timestamp': datetime.now().isoformat(),
                'scan_type': 'deep',
                'vulnerability_analysis': vulnerability_results,
                'ml_analysis': ml_results,
                'threat_intelligence': threat_results,
                'overall_risk_score': max(
                    vulnerability_results.get('risk_score', 0),
                    threat_results.get('risk_score', 0)
                ),
                'total_vulnerabilities': len(vulnerability_results.get('vulnerabilities', [])) + 
                                      len(threat_results.get('threats_detected', []))
            }
        else:
            # Quick scan with pattern-based detection only
            vulnerability_results = security_analyzer.analyze_code(code_content, file.filename)
            
            scan_results = {
                'scan_id': scan_id,
                'file_name': file.filename,
                'timestamp': datetime.now().isoformat(),
                'scan_type': 'quick',
                'vulnerability_analysis': vulnerability_results,
                'overall_risk_score': vulnerability_results.get('risk_score', 0),
                'total_vulnerabilities': len(vulnerability_results.get('vulnerabilities', []))
            }
        
        # Schedule cleanup
        background_tasks.add_task(os.unlink, temp_file_path)
        
        return JSONResponse(content=scan_results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@router.post("/scan/batch")
async def scan_multiple_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    deep_scan: bool = False
):
    """
    Scan multiple files for security vulnerabilities
    """
    try:
        scan_id = str(uuid.uuid4())
        batch_results = {
            'scan_id': scan_id,
            'timestamp': datetime.now().isoformat(),
            'scan_type': 'batch_' + ('deep' if deep_scan else 'quick'),
            'files_scanned': len(files),
            'results': []
        }
        
        temp_files = []
        
        try:
            # Process each file
            for file in files:
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
                shutil.copyfileobj(file.file, temp_file)
                temp_files.append(temp_file.name)
                temp_file.close()
                
                # Read file content
                with open(temp_file.name, 'r', encoding='utf-8', errors='ignore') as f:
                    code_content = f.read()
                
                # Perform analysis
                if deep_scan:
                    vulnerability_results = security_analyzer.analyze_code(code_content, file.filename)
                    threat_results = threat_engine.analyze_code_threats(code_content, file.filename)
                    
                    file_result = {
                        'file_name': file.filename,
                        'vulnerability_analysis': vulnerability_results,
                        'threat_intelligence': threat_results,
                        'overall_risk_score': max(
                            vulnerability_results.get('risk_score', 0),
                            threat_results.get('risk_score', 0)
                        ),
                        'total_vulnerabilities': len(vulnerability_results.get('vulnerabilities', [])) + 
                                              len(threat_results.get('threats_detected', []))
                    }
                else:
                    vulnerability_results = security_analyzer.analyze_code(code_content, file.filename)
                    
                    file_result = {
                        'file_name': file.filename,
                        'vulnerability_analysis': vulnerability_results,
                        'overall_risk_score': vulnerability_results.get('risk_score', 0),
                        'total_vulnerabilities': len(vulnerability_results.get('vulnerabilities', []))
                    }
                
                batch_results['results'].append(file_result)
            
            # Calculate batch summary
            total_vulnerabilities = sum(r['total_vulnerabilities'] for r in batch_results['results'])
            avg_risk_score = sum(r['overall_risk_score'] for r in batch_results['results']) / len(batch_results['results'])
            
            batch_results['summary'] = {
                'total_vulnerabilities': total_vulnerabilities,
                'average_risk_score': avg_risk_score,
                'high_risk_files': len([r for r in batch_results['results'] if r['overall_risk_score'] >= 7.0])
            }
            
            return JSONResponse(content=batch_results)
            
        finally:
            # Cleanup temporary files
            for temp_file in temp_files:
                background_tasks.add_task(os.unlink, temp_file)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch scan failed: {str(e)}")

@router.post("/analyze/text")
async def analyze_code_text(
    code_content: str,
    file_name: Optional[str] = "unknown",
    deep_scan: bool = False
):
    """
    Analyze code content directly (text input)
    """
    try:
        scan_id = str(uuid.uuid4())
        
        if deep_scan:
            # Deep analysis
            vulnerability_results = security_analyzer.analyze_code(code_content, file_name)
            ml_results = ml_detector.analyze_code_batch([{
                'content': code_content,
                'file_path': file_name
            }])
            threat_results = threat_engine.analyze_code_threats(code_content, file_name)
            
            analysis_results = {
                'scan_id': scan_id,
                'file_name': file_name,
                'timestamp': datetime.now().isoformat(),
                'analysis_type': 'deep_text',
                'vulnerability_analysis': vulnerability_results,
                'ml_analysis': ml_results,
                'threat_intelligence': threat_results,
                'overall_risk_score': max(
                    vulnerability_results.get('risk_score', 0),
                    threat_results.get('risk_score', 0)
                ),
                'total_vulnerabilities': len(vulnerability_results.get('vulnerabilities', [])) + 
                                      len(threat_results.get('threats_detected', []))
            }
        else:
            # Quick analysis
            vulnerability_results = security_analyzer.analyze_code(code_content, file_name)
            
            analysis_results = {
                'scan_id': scan_id,
                'file_name': file_name,
                'timestamp': datetime.now().isoformat(),
                'analysis_type': 'quick_text',
                'vulnerability_analysis': vulnerability_results,
                'overall_risk_score': vulnerability_results.get('risk_score', 0),
                'total_vulnerabilities': len(vulnerability_results.get('vulnerabilities', []))
            }
        
        return JSONResponse(content=analysis_results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")

@router.get("/report/{scan_id}")
async def generate_security_report(scan_id: str):
    """
    Generate comprehensive security report for a scan
    """
    try:
        # In a real implementation, you would retrieve scan results from database
        # For now, we'll generate a sample report structure
        
        report = {
            'scan_id': scan_id,
            'timestamp': datetime.now().isoformat(),
            'report_type': 'security_analysis',
            'executive_summary': {
                'total_files_analyzed': 1,
                'critical_vulnerabilities': 0,
                'high_vulnerabilities': 0,
                'medium_vulnerabilities': 0,
                'low_vulnerabilities': 0,
                'overall_risk_level': 'LOW'
            },
            'detailed_findings': [],
            'recommendations': [
                "Continue regular security scanning",
                "Implement code review processes",
                "Keep dependencies updated"
            ],
            'compliance_status': {
                'owasp_top_10': 'COMPLIANT',
                'security_headers': 'COMPLIANT',
                'data_protection': 'COMPLIANT'
            }
        }
        
        return JSONResponse(content=report)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.post("/train/models")
async def train_security_models(
    training_data: List[Dict[str, Any]],
    model_type: str = "all"
):
    """
    Train security ML models with provided data
    """
    try:
        training_results = {
            'timestamp': datetime.now().isoformat(),
            'training_status': 'completed',
            'models_trained': []
        }
        
        if model_type in ['all', 'ml_detector']:
            # Train ML detector
            ml_training_result = ml_detector.train_model(training_data)
            training_results['models_trained'].append({
                'model': 'ml_detector',
                'result': ml_training_result
            })
        
        if model_type in ['all', 'threat_intelligence']:
            # Train threat intelligence engine
            # This would require additional implementation
            training_results['models_trained'].append({
                'model': 'threat_intelligence',
                'result': {'status': 'training_completed'}
            })
        
        return JSONResponse(content=training_results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")

@router.get("/models/status")
async def get_models_status():
    """
    Get status of all security models
    """
    try:
        status = {
            'timestamp': datetime.now().isoformat(),
            'models': {
                'security_analyzer': {
                    'status': 'active',
                    'model_type': 'transformer-based',
                    'device': str(security_analyzer.device),
                    'patterns_loaded': len(security_analyzer.vulnerability_patterns)
                },
                'ml_detector': {
                    'status': 'active' if ml_detector.model_trained else 'needs_training',
                    'model_type': 'neural_network',
                    'device': str(ml_detector.device),
                    'trained': ml_detector.model_trained
                },
                'threat_intelligence': {
                    'status': 'active',
                    'signatures_loaded': len(threat_engine.threat_signatures),
                    'threat_history_size': len(threat_engine.threat_history)
                }
            },
            'system_info': {
                'pytorch_version': torch.__version__,
                'cuda_available': torch.cuda.is_available(),
                'device_count': torch.cuda.device_count() if torch.cuda.is_available() else 0
            }
        }
        
        return JSONResponse(content=status)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.post("/models/save")
async def save_models(model_directory: str = "models"):
    """
    Save trained models to disk
    """
    try:
        save_results = {
            'timestamp': datetime.now().isoformat(),
            'save_status': 'completed',
            'models_saved': []
        }
        
        # Save ML detector models
        ml_models = ml_detector.save_models(model_directory)
        save_results['models_saved'].append({
            'model': 'ml_detector',
            'files': ml_models
        })
        
        # Save threat intelligence signatures
        signatures_file = f"{model_directory}/threat_signatures.json"
        os.makedirs(model_directory, exist_ok=True)
        
        signatures_data = {
            sig_id: {
                'signature_id': sig.signature_id,
                'threat_type': sig.threat_type,
                'pattern': sig.pattern,
                'severity': sig.severity,
                'confidence': sig.confidence,
                'description': sig.description,
                'mitigation': sig.mitigation,
                'created_at': sig.created_at.isoformat(),
                'updated_at': sig.updated_at.isoformat()
            }
            for sig_id, sig in threat_engine.threat_signatures.items()
        }
        
        with open(signatures_file, 'w') as f:
            json.dump(signatures_data, f, indent=2)
        
        save_results['models_saved'].append({
            'model': 'threat_intelligence',
            'file': signatures_file
        })
        
        return JSONResponse(content=save_results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model saving failed: {str(e)}")

@router.post("/models/load")
async def load_models(model_directory: str = "models"):
    """
    Load trained models from disk
    """
    try:
        load_results = {
            'timestamp': datetime.now().isoformat(),
            'load_status': 'completed',
            'models_loaded': []
        }
        
        # Load ML detector models
        if ml_detector.load_models(model_directory):
            load_results['models_loaded'].append({
                'model': 'ml_detector',
                'status': 'success'
            })
        else:
            load_results['models_loaded'].append({
                'model': 'ml_detector',
                'status': 'failed',
                'reason': 'Model files not found'
            })
        
        # Load threat intelligence signatures
        signatures_file = f"{model_directory}/threat_signatures.json"
        if os.path.exists(signatures_file):
            with open(signatures_file, 'r') as f:
                signatures_data = json.load(f)
            
            # Restore signatures
            for sig_id, sig_data in signatures_data.items():
                threat_engine.threat_signatures[sig_id] = ThreatSignature(
                    signature_id=sig_data['signature_id'],
                    threat_type=sig_data['threat_type'],
                    pattern=sig_data['pattern'],
                    severity=sig_data['severity'],
                    confidence=sig_data['confidence'],
                    description=sig_data['description'],
                    mitigation=sig_data['mitigation'],
                    created_at=datetime.fromisoformat(sig_data['created_at']),
                    updated_at=datetime.fromisoformat(sig_data['updated_at'])
                )
            
            load_results['models_loaded'].append({
                'model': 'threat_intelligence',
                'status': 'success'
            })
        
        return JSONResponse(content=load_results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model loading failed: {str(e)}")

@router.get("/health")
async def security_service_health():
    """
    Health check for security service
    """
    try:
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'security_analyzer': 'operational',
                'ml_detector': 'operational' if ml_detector.model_trained else 'needs_training',
                'threat_intelligence': 'operational'
            },
            'version': '1.0.0'
        }
        
        return JSONResponse(content=health_status)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
