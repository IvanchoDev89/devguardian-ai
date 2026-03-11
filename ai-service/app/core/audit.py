from datetime import datetime
from typing import Dict, Any, Optional
from collections import defaultdict
import json
import hashlib
import os


class AuditLogger:
    def __init__(self, log_file: str = "/tmp/devguardian_audit.log"):
        self.log_file = log_file
        self.in_memory_logs = []
        self.max_in_memory = 1000
        
    def log_event(
        self,
        event_type: str,
        user_id: Optional[str],
        ip_address: str,
        action: str,
        resource: str,
        success: bool,
        metadata: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "ip_address": ip_address,
            "action": action,
            "resource": resource,
            "success": success,
            "metadata": metadata or {},
            "error_message": error_message,
            "event_hash": ""
        }
        
        entry["event_hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        self.in_memory_logs.append(entry)
        if len(self.in_memory_logs) > self.max_in_memory:
            self.in_memory_logs = self.in_memory_logs[-self.max_in_memory:]
        
        self._write_to_file(entry)
        
    def _write_to_file(self, entry: Dict[str, Any]):
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass
            
    def get_logs(
        self,
        user_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> list:
        logs = self.in_memory_logs
        
        if user_id:
            logs = [l for l in logs if l.get("user_id") == user_id]
        if event_type:
            logs = [l for l in logs if l.get("event_type") == event_type]
            
        return logs[-limit:]
        
    def get_failed_logins(self, hours: int = 24) -> list:
        cutoff = datetime.now().timestamp() - (hours * 3600)
        return [
            l for l in self.in_memory_logs
            if l.get("event_type") == "login" 
            and not l.get("success")
            and datetime.fromisoformat(l["timestamp"]).timestamp() > cutoff
        ]
        
    def get_suspicious_activity(self, threshold: int = 5) -> Dict[str, Any]:
        ip_counts = defaultdict(int)
        user_counts = defaultdict(int)
        
        for log in self.in_memory_logs:
            if not log.get("success") and log.get("event_type") in ["login", "auth"]:
                ip_counts[log.get("ip_address", "unknown")] += 1
                user_counts[log.get("user_id", "unknown")] += 1
                
        return {
            "suspicious_ips": {ip: count for ip, count in ip_counts.items() if count >= threshold},
            "suspicious_users": {user: count for user, count in user_counts.items() if count >= threshold}
        }


_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    global _audit_logger
    if _audit_logger is None:
        log_file = os.getenv("AUDIT_LOG_FILE", "/tmp/devguardian_audit.log")
        _audit_logger = AuditLogger(log_file)
    return _audit_logger
