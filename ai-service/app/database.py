from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./devguardian.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password_hash = Column(String)
    role = Column(String, default="user")
    plan = Column(String, default="free")
    is_active = Column(Boolean, default=True)
    
    # Free trial system
    free_trial_remaining = Column(Integer, default=3)
    free_trial_used = Column(Integer, default=0)
    has_used_free_trial = Column(Boolean, default=False)
    
    last_login = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    avatar_url = Column(String, nullable=True)
    company = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key_id = Column(String, unique=True, index=True)
    key_prefix = Column(String)
    hashed_key = Column(String)
    user_id = Column(String, index=True)
    name = Column(String)
    plan = Column(String, default="free")
    monthly_quota = Column(Integer, default=50)
    scans_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    last_used = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

class Webhook(Base):
    __tablename__ = "webhooks"
    
    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(String, unique=True, index=True)
    user_id = Column(String, index=True)
    url = Column(String)
    events = Column(Text)  # JSON string
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_triggered = Column(DateTime, nullable=True)

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, unique=True, index=True)
    name = Column(String)
    plan = Column(String, default="free")
    owner_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TeamMember(Base):
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(String, unique=True, index=True)
    team_id = Column(String, index=True)
    user_id = Column(String, index=True)
    email = Column(String)
    name = Column(String)
    role = Column(String, default="member")
    joined_at = Column(DateTime, default=datetime.utcnow)

class TeamInvitation(Base):
    __tablename__ = "team_invitations"
    
    id = Column(Integer, primary_key=True, index=True)
    invitation_id = Column(String, unique=True, index=True)
    team_id = Column(String, index=True)
    email = Column(String, index=True)
    role = Column(String, default="member")
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    invited_by = Column(String)

class Scan(Base):
    __tablename__ = "scans"
    __table_args__ = (
        Index('idx_scan_user_date', 'user_id', 'created_at'),
        Index('idx_scan_status', 'status'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, unique=True, index=True)
    user_id = Column(String, index=True)
    code = Column(Text)
    language = Column(String)
    score = Column(Integer)
    total_vulnerabilities = Column(Integer, default=0)
    status = Column(String, default="completed")
    duration_ms = Column(Integer, nullable=True)
    file_name = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    __table_args__ = (
        Index('idx_vuln_scan', 'scan_id'),
        Index('idx_vuln_status', 'status'),
        Index('idx_vuln_severity', 'severity'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, index=True)
    file = Column(String, nullable=True)
    line_number = Column(Integer)
    line_content = Column(String)
    vulnerability_type = Column(String)
    severity = Column(String)
    description = Column(Text)
    match = Column(Text)
    cwe_id = Column(String, nullable=True)
    owasp_category = Column(String, nullable=True)
    status = Column(String, default="open")
    assignee_id = Column(String, nullable=True)
    severity_score = Column(Integer, nullable=True)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    false_positive_reason = Column(Text, nullable=True)
    false_positive = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

class GitHubIntegration(Base):
    __tablename__ = "github_integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    integration_id = Column(String, unique=True, index=True)
    user_id = Column(String, index=True)
    repo_owner = Column(String)
    repo_name = Column(String)
    installation_id = Column(String)
    auto_scan_pr = Column(Boolean, default=True)
    auto_comment = Column(Boolean, default=True)
    scan_on_push = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_scan = Column(DateTime, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    user_id = Column(String, nullable=True)
    ip_address = Column(String)
    action = Column(String)
    resource = Column(String)
    success = Column(Boolean)
    extra_data = Column(Text)  # renamed from metadata
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class RateLimit(Base):
    __tablename__ = "rate_limits"
    
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    endpoint = Column(String)
    requests_count = Column(Integer, default=0)
    window_start = Column(DateTime, default=datetime.utcnow)
    blocked_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    user_id = Column(String, index=True)
    ip_address = Column(String)
    user_agent = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime)
    device_info = Column(String, nullable=True)
    location = Column(String, nullable=True)


class SecurityAuditLog(Base):
    __tablename__ = "security_audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    user_id = Column(String, nullable=True, index=True)
    ip_address = Column(String, index=True)
    action = Column(String, index=True)
    resource = Column(String)
    result = Column(String)
    details = Column(Text, nullable=True)
    severity = Column(String, default="INFO")
    user_agent = Column(String, nullable=True)


class APIKeyUsage(Base):
    __tablename__ = "api_key_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    key_id = Column(String, index=True)
    user_id = Column(String, nullable=True, index=True)
    endpoint = Column(String)
    method = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    response_code = Column(Integer)
    latency_ms = Column(Integer)
    ip_address = Column(String, nullable=True)
    request_size = Column(Integer, nullable=True)
    response_size = Column(Integer, nullable=True)


class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    type = Column(String)
    title = Column(String)
    message = Column(Text)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
