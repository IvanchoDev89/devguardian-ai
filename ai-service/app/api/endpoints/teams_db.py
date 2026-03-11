from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
import secrets
from sqlalchemy.orm import Session
from app.database import get_db, Team as DBTeam, TeamMember as DBTeamMember, TeamInvitation as DBTeamInvitation
from app.core.auth import get_current_user_optional, TokenData

router = APIRouter(prefix="/api/teams", tags=["Team Management"])


class TeamCreate(BaseModel):
    name: str
    plan: str = "free"


class TeamResponse(BaseModel):
    team_id: str
    name: str
    plan: str
    owner_id: str
    created_at: str
    member_count: int


class MemberInvite(BaseModel):
    email: EmailStr
    role: str = "member"


class InvitationResponse(BaseModel):
    invitation_id: str
    email: str
    role: str
    status: str
    created_at: str
    expires_at: str


@router.post("/teams")
async def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Create a new team"""
    user_id = current_user.user_id if current_user else "anonymous"
    user_email = current_user.email if current_user and hasattr(current_user, 'email') else "anonymous@devguardian.ai"
    team_id = f"team_{secrets.token_urlsafe(8)}"
    
    db_team = DBTeam(
        team_id=team_id,
        name=team.name,
        plan=team.plan,
        owner_id=user_id
    )
    db.add(db_team)
    
    # Add owner as admin member
    member_id = f"member_{secrets.token_urlsafe(8)}"
    db_member = DBTeamMember(
        member_id=member_id,
        team_id=team_id,
        user_id=user_id,
        email=user_email,
        name=user_email.split("@")[0],
        role="owner"
    )
    db.add(db_member)
    db.commit()
    
    return {
        "team_id": team_id,
        "name": team.name,
        "plan": team.plan,
        "owner_id": user_id,
        "created_at": datetime.now().isoformat()
    }


@router.get("/teams")
async def list_teams(
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """List all teams for the user"""
    user_id = current_user.user_id if current_user else "anonymous"
    members = db.query(DBTeamMember).filter(DBTeamMember.user_id == user_id).all()
    team_ids = [m.team_id for m in members]
    
    teams = db.query(DBTeam).filter(DBTeam.team_id.in_(team_ids)).all()
    
    result = []
    for team in teams:
        member_count = db.query(DBTeamMember).filter(DBTeamMember.team_id == team.team_id).count()
        result.append({
            "team_id": team.team_id,
            "name": team.name,
            "plan": team.plan,
            "owner_id": team.owner_id,
            "created_at": team.created_at.isoformat() if team.created_at else "",
            "member_count": member_count
        })
    
    return result


@router.get("/teams/{team_id}")
async def get_team(
    team_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Get team details"""
    user_id = current_user.user_id if current_user else "anonymous"
    team = db.query(DBTeam).filter(DBTeam.team_id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check membership
    membership = db.query(DBTeamMember).filter(
        DBTeamMember.team_id == team_id,
        DBTeamMember.user_id == user_id
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this team")
    
    members = db.query(DBTeamMember).filter(DBTeamMember.team_id == team_id).all()
    
    return {
        "team_id": team.team_id,
        "name": team.name,
        "plan": team.plan,
        "owner_id": team.owner_id,
        "created_at": team.created_at.isoformat() if team.created_at else "",
        "members": [{
            "user_id": m.user_id,
            "email": m.email,
            "name": m.name,
            "role": m.role,
            "joined_at": m.joined_at.isoformat() if m.joined_at else ""
        } for m in members]
    }


@router.post("/teams/{team_id}/invite")
async def invite_member(
    team_id: str,
    invite: MemberInvite,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Invite a member to the team"""
    user_id = current_user.user_id if current_user else "anonymous"
    team = db.query(DBTeam).filter(DBTeam.team_id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    membership = db.query(DBTeamMember).filter(
        DBTeamMember.team_id == team_id,
        DBTeamMember.user_id == user_id
    ).first()
    
    if not membership or membership.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="Only owners and admins can invite members")
    
    invitation_id = f"inv_{secrets.token_urlsafe(12)}"
    
    invitation = DBTeamInvitation(
        invitation_id=invitation_id,
        team_id=team_id,
        email=invite.email,
        role=invite.role,
        status="pending",
        expires_at=datetime.now() + timedelta(days=7),
        invited_by=user_id
    )
    db.add(invitation)
    db.commit()
    
    return {
        "invitation_id": invitation_id,
        "email": invite.email,
        "role": invite.role,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=7)).isoformat()
    }


@router.get("/teams/{team_id}/invitations")
async def list_invitations(
    team_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """List pending invitations"""
    user_id = current_user.user_id if current_user else "anonymous"
    team = db.query(DBTeam).filter(DBTeam.team_id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    invitations = db.query(DBTeamInvitation).filter(
        DBTeamInvitation.team_id == team_id,
        DBTeamInvitation.status == "pending"
    ).all()
    
    return [{
        "invitation_id": i.invitation_id,
        "email": i.email,
        "role": i.role,
        "status": i.status,
        "created_at": i.created_at.isoformat() if i.created_at else "",
        "expires_at": i.expires_at.isoformat() if i.expires_at else ""
    } for i in invitations]


@router.delete("/teams/{team_id}/members/{member_id}")
async def remove_member(
    team_id: str,
    member_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Remove a member from the team"""
    user_id = current_user.user_id if current_user else "anonymous"
    team = db.query(DBTeam).filter(DBTeam.team_id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    membership = db.query(DBTeamMember).filter(
        DBTeamMember.team_id == team_id,
        DBTeamMember.user_id == user_id
    ).first()
    
    if not membership or membership.role != "owner":
        raise HTTPException(status_code=403, detail="Only the owner can remove members")
    
    member = db.query(DBTeamMember).filter(
        DBTeamMember.member_id == member_id,
        DBTeamMember.team_id == team_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    if member.role == "owner":
        raise HTTPException(status_code=400, detail="Cannot remove the owner")
    
    db.delete(member)
    db.commit()
    
    return {"message": "Member removed"}


@router.get("/teams/{team_id}/usage")
async def get_team_usage(
    team_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Get team usage statistics"""
    user_id = current_user.user_id if current_user else "anonymous"
    team = db.query(DBTeam).filter(DBTeam.team_id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    member_count = db.query(DBTeamMember).filter(DBTeamMember.team_id == team_id).count()
    
    return {
        "team_id": team_id,
        "plan": team.plan,
        "scans_this_month": 0,
        "api_calls_this_month": 0,
        "members": member_count
    }
