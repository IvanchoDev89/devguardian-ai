"""
PyTorch Vulnerability Scanner API Endpoints
Provides REST API endpoints for advanced vulnerability scanning using PyTorch
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import tempfile
import shutil
from pathlib import Path
import logging
import asyncio
from datetime import datetime
import uuid

# Try to import PyTorch - make it optional
try:
    import torch
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
    torch = None

try:
    from app.core.services.pytorch_vulnerability_scanner import PyTorchVulnerabilityScanner, VulnerabilityResult
    from app.core.models.scan_models import (
        ScanRequest, 
        ScanResponse, 
        VulnerabilityReport,
        ScanStatus
    )
    SCANNER_AVAILABLE = True
except ImportError:
    SCANNER_AVAILABLE = False
    PyTorchVulnerabilityScanner = None
    VulnerabilityResult = None
    ScanRequest = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/pytorch-scanner", tags=["PyTorch Scanner"])

# Global scanner instance
scanner = PyTorchVulnerabilityScanner()

# In-memory storage for scan results (in production, use Redis or database)
scan_results: Dict[str, Dict[str, Any]] = {}
scan_status: Dict[str, ScanStatus] = {}

@router.post("/scan/file", response_model=ScanResponse)
async def scan_file_endpoint(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Scan a single file for vulnerabilities using PyTorch models
    """
    try:
        # Generate scan ID
        scan_id = str(uuid.uuid4())
        
        # Initialize scan status
        scan_status[scan_id] = ScanStatus(
            scan_id=scan_id,
            status="scanning",
            progress=0,
            started_at=datetime.now(),
            file_name=file.filename
        )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        # Read file content
        with open(temp_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Perform scan in background
        background_tasks.add_task(
            perform_file_scan,
            scan_id,
            str(temp_file_path),
            content,
            file.filename
        )
        
        return ScanResponse(
            scan_id=scan_id,
            status="scanning",
            message="File scan started",
            estimated_time="30-60 seconds"
        )
        
    except Exception as e:
        logger.error(f"Error starting file scan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start scan: {str(e)}")

@router.post("/scan/directory", response_model=ScanResponse)
async def scan_directory_endpoint(
    directory_path: str,
    file_extensions: Optional[List[str]] = None,
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Scan an entire directory for vulnerabilities using PyTorch models
    """
    try:
        # Generate scan ID
        scan_id = str(uuid.uuid4())
        
        # Initialize scan status
        scan_status[scan_id] = ScanStatus(
            scan_id=scan_id,
            status="scanning",
            progress=0,
            started_at=datetime.now(),
            file_name=directory_path
        )
        
        # Validate directory exists
        if not Path(directory_path).exists():
            raise HTTPException(status_code=404, detail="Directory not found")
        
        # Perform scan in background
        background_tasks.add_task(
            perform_directory_scan,
            scan_id,
            directory_path,
            file_extensions
        )
        
        return ScanResponse(
            scan_id=scan_id,
            status="scanning",
            message="Directory scan started",
            estimated_time="2-5 minutes"
        )
        
    except Exception as e:
        logger.error(f"Error starting directory scan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start scan: {str(e)}")

@router.post("/scan/code", response_model=ScanResponse)
async def scan_code_endpoint(
    scan_request: ScanRequest,
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Scan code content directly without file upload
    """
    try:
        # Generate scan ID
        scan_id = str(uuid.uuid4())
        
        # Initialize scan status
        scan_status[scan_id] = ScanStatus(
            scan_id=scan_id,
            status="scanning",
            progress=0,
            started_at=datetime.now(),
            file_name=scan_request.file_name or "inline_code"
        )
        
        # Perform scan in background
        background_tasks.add_task(
            perform_code_scan,
            scan_id,
            scan_request.code,
            scan_request.file_name
        )
        
        return ScanResponse(
            scan_id=scan_id,
            status="scanning",
            message="Code scan started",
            estimated_time="10-30 seconds"
        )
        
    except Exception as e:
        logger.error(f"Error starting code scan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start scan: {str(e)}")

@router.get("/scan/{scan_id}/status", response_model=ScanStatus)
async def get_scan_status(scan_id: str):
    """
    Get the status of an ongoing scan
    """
    if scan_id not in scan_status:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return scan_status[scan_id]

@router.get("/scan/{scan_id}/results", response_model=VulnerabilityReport)
async def get_scan_results(scan_id: str):
    """
    Get the results of a completed scan
    """
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan results not found")
    
    scan_data = scan_results[scan_id]
    
    if scan_data['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Scan not completed yet")
    
    return VulnerabilityReport(
        scan_id=scan_id,
        scan_date=scan_data['scan_date'],
        total_vulnerabilities=scan_data['total_vulnerabilities'],
        severity_breakdown=scan_data['severity_breakdown'],
        type_breakdown=scan_data['type_breakdown'],
        risk_score=scan_data['risk_score'],
        vulnerabilities=scan_data['vulnerabilities'],
        recommendations=scan_data['recommendations']
    )

@router.get("/scan/{scan_id}/download")
async def download_scan_report(scan_id: str):
    """
    Download scan results as JSON file
    """
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan results not found")
    
    scan_data = scan_results[scan_id]
    
    if scan_data['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Scan not completed yet")
    
    # Create downloadable report
    report_data = {
        'scan_id': scan_id,
        'scan_date': scan_data['scan_date'],
        'summary': {
            'total_vulnerabilities': scan_data['total_vulnerabilities'],
            'severity_breakdown': scan_data['severity_breakdown'],
            'type_breakdown': scan_data['type_breakdown'],
            'risk_score': scan_data['risk_score']
        },
        'vulnerabilities': [
            {
                'file_path': vuln.file_path,
                'vulnerability_type': vuln.vulnerability_type.value,
                'severity': vuln.severity,
                'confidence': vuln.confidence,
                'line_number': vuln.line_number,
                'code_snippet': vuln.code_snippet,
                'description': vuln.description,
                'recommendation': vuln.recommendation,
                'cwe_id': vuln.cwe_id,
                'cvss_score': vuln.cvss_score
            }
            for vuln in scan_data['vulnerabilities']
        ],
        'recommendations': scan_data['recommendations']
    }
    
    return JSONResponse(
        content=report_data,
        headers={
            "Content-Disposition": f"attachment; filename=vulnerability_report_{scan_id}.json"
        }
    )

@router.post("/models/train")
async def train_models(
    training_data_path: str,
    epochs: int = 10,
    batch_size: int = 32,
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Train the PyTorch models on labeled vulnerability data
    """
    try:
        # Generate training ID
        training_id = str(uuid.uuid4())
        
        # Validate training data exists
        if not Path(training_data_path).exists():
            raise HTTPException(status_code=404, detail="Training data file not found")
        
        # Start training in background
        background_tasks.add_task(
            perform_model_training,
            training_id,
            training_data_path,
            epochs,
            batch_size
        )
        
        return {
            "training_id": training_id,
            "status": "training_started",
            "message": f"Model training started with {epochs} epochs",
            "estimated_time": f"{epochs * 2}-{epochs * 5} minutes"
        }
        
    except Exception as e:
        logger.error(f"Error starting model training: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start training: {str(e)}")

@router.post("/models/save")
async def save_models(save_path: str):
    """
    Save trained PyTorch models
    """
    try:
        scanner.save_models(save_path)
        return {"message": f"Models saved successfully to {save_path}"}
    except Exception as e:
        logger.error(f"Error saving models: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save models: {str(e)}")

@router.post("/models/load")
async def load_models(load_path: str):
    """
    Load pre-trained PyTorch models
    """
    try:
        scanner.load_models(load_path)
        return {"message": f"Models loaded successfully from {load_path}"}
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load models: {str(e)}")

@router.get("/models/status")
async def get_model_status():
    """
    Get the current status of the PyTorch models
    """
    return {
        "models_loaded": scanner.is_trained,
        "device": str(scanner.device),
        "model_types": ["feature_classifier", "sequence_detector"],
        "vulnerability_types": [vuln_type.value for vuln_type in scanner.vulnerability_patterns.keys()]
    }

# Background task functions
async def perform_file_scan(scan_id: str, file_path: str, content: str, file_name: str):
    """Background task to perform file scan"""
    try:
        # Update status
        scan_status[scan_id].progress = 25
        scan_status[scan_id].status = "analyzing"
        
        # Perform scan
        vulnerabilities = scanner.scan_file(file_path, content)
        
        # Update status
        scan_status[scan_id].progress = 75
        scan_status[scan_id].status = "generating_report"
        
        # Generate report
        scan_results_data = scanner.generate_report({file_path: vulnerabilities})
        
        # Store results
        scan_results[scan_id] = {
            'status': 'completed',
            'scan_date': scan_results_data['scan_date'],
            'total_vulnerabilities': scan_results_data['total_vulnerabilities'],
            'severity_breakdown': scan_results_data['severity_breakdown'],
            'type_breakdown': scan_results_data['type_breakdown'],
            'risk_score': scan_results_data['risk_score'],
            'vulnerabilities': vulnerabilities,
            'recommendations': generate_recommendations(vulnerabilities)
        }
        
        # Update final status
        scan_status[scan_id].status = "completed"
        scan_status[scan_id].progress = 100
        scan_status[scan_id].completed_at = datetime.now()
        
        logger.info(f"File scan completed for {file_name}: {len(vulnerabilities)} vulnerabilities found")
        
    except Exception as e:
        logger.error(f"Error in file scan: {str(e)}")
        scan_status[scan_id].status = "failed"
        scan_status[scan_id].error = str(e)
    
    finally:
        # Clean up temporary file
        try:
            Path(file_path).unlink()
        except:
            pass

async def perform_directory_scan(scan_id: str, directory_path: str, file_extensions: Optional[List[str]]):
    """Background task to perform directory scan"""
    try:
        # Update status
        scan_status[scan_id].progress = 10
        scan_status[scan_id].status = "scanning_files"
        
        # Perform scan
        results = scanner.scan_directory(directory_path, file_extensions)
        
        # Update status
        scan_status[scan_id].progress = 70
        scan_status[scan_id].status = "generating_report"
        
        # Generate report
        scan_results_data = scanner.generate_report(results)
        
        # Flatten all vulnerabilities
        all_vulnerabilities = []
        for file_vulns in results.values():
            all_vulnerabilities.extend(file_vulns)
        
        # Store results
        scan_results[scan_id] = {
            'status': 'completed',
            'scan_date': scan_results_data['scan_date'],
            'total_vulnerabilities': scan_results_data['total_vulnerabilities'],
            'severity_breakdown': scan_results_data['severity_breakdown'],
            'type_breakdown': scan_results_data['type_breakdown'],
            'risk_score': scan_results_data['risk_score'],
            'vulnerabilities': all_vulnerabilities,
            'recommendations': generate_recommendations(all_vulnerabilities)
        }
        
        # Update final status
        scan_status[scan_id].status = "completed"
        scan_status[scan_id].progress = 100
        scan_status[scan_id].completed_at = datetime.now()
        
        logger.info(f"Directory scan completed for {directory_path}: {len(all_vulnerabilities)} vulnerabilities found")
        
    except Exception as e:
        logger.error(f"Error in directory scan: {str(e)}")
        scan_status[scan_id].status = "failed"
        scan_status[scan_id].error = str(e)

async def perform_code_scan(scan_id: str, code: str, file_name: str):
    """Background task to perform code scan"""
    try:
        # Update status
        scan_status[scan_id].progress = 25
        scan_status[scan_id].status = "analyzing"
        
        # Perform scan
        vulnerabilities = scanner.scan_file(file_name, code)
        
        # Update status
        scan_status[scan_id].progress = 75
        scan_status[scan_id].status = "generating_report"
        
        # Generate report
        scan_results_data = scanner.generate_report({file_name: vulnerabilities})
        
        # Store results
        scan_results[scan_id] = {
            'status': 'completed',
            'scan_date': scan_results_data['scan_date'],
            'total_vulnerabilities': scan_results_data['total_vulnerabilities'],
            'severity_breakdown': scan_results_data['severity_breakdown'],
            'type_breakdown': scan_results_data['type_breakdown'],
            'risk_score': scan_results_data['risk_score'],
            'vulnerabilities': vulnerabilities,
            'recommendations': generate_recommendations(vulnerabilities)
        }
        
        # Update final status
        scan_status[scan_id].status = "completed"
        scan_status[scan_id].progress = 100
        scan_status[scan_id].completed_at = datetime.now()
        
        logger.info(f"Code scan completed: {len(vulnerabilities)} vulnerabilities found")
        
    except Exception as e:
        logger.error(f"Error in code scan: {str(e)}")
        scan_status[scan_id].status = "failed"
        scan_status[scan_id].error = str(e)

async def perform_model_training(training_id: str, training_data_path: str, epochs: int, batch_size: int):
    """Background task to train models"""
    try:
        # Load training data
        import json
        with open(training_data_path, 'r') as f:
            training_data = json.load(f)
        
        # Train models
        scanner.train_models(training_data, epochs, batch_size)
        
        logger.info(f"Model training completed with ID: {training_id}")
        
    except Exception as e:
        logger.error(f"Error in model training: {str(e)}")

def generate_recommendations(vulnerabilities: List[VulnerabilityResult]) -> List[str]:
    """Generate overall recommendations based on vulnerabilities"""
    recommendations = []
    
    # Count by severity
    critical_count = sum(1 for v in vulnerabilities if v.severity == 'critical')
    high_count = sum(1 for v in vulnerabilities if v.severity == 'high')
    
    # Generate recommendations based on findings
    if critical_count > 0:
        recommendations.append(f"URGENT: Address {critical_count} critical vulnerabilities immediately")
    
    if high_count > 5:
        recommendations.append(f"HIGH PRIORITY: {high_count} high-severity vulnerabilities require immediate attention")
    
    # Type-specific recommendations
    vuln_types = {}
    for vuln in vulnerabilities:
        vuln_types[vuln.vulnerability_type.value] = vuln_types.get(vuln.vulnerability_type.value, 0) + 1
    
    if 'sql_injection' in vuln_types and vuln_types['sql_injection'] > 3:
        recommendations.append("Implement comprehensive input validation and parameterized queries throughout the application")
    
    if 'hardcoded_credentials' in vuln_types:
        recommendations.append("Remove all hardcoded credentials and implement secure credential management")
    
    if 'weak_cryptography' in vuln_types:
        recommendations.append("Update all weak cryptographic implementations to use modern, secure algorithms")
    
    # General recommendations
    recommendations.append("Implement regular security scanning as part of CI/CD pipeline")
    recommendations.append("Conduct security code reviews for all new features")
    recommendations.append("Keep all dependencies and frameworks updated to latest secure versions")
    
    return recommendations
