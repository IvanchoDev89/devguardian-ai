from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import secrets
from app.core.auth import get_current_user, TokenData, get_password_hash

router = APIRouter(prefix="/api/teams", tags=["Team Management"])

teams_db: dict = {}
team_members_db: dict = {}
invitations_db: dict = {}


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


class MemberResponse(BaseModel):
    user_id: str
    email: str
    name: str
    role: str
    joined_at: str


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
    current_user: TokenData = Depends(get_current_user)
):
    """Create a new team"""
    team_id = f"team_{secrets.token_urlsafe(8)}"
    
    team_data = {
        "team_id": team_id,
        "name": team.name,
        "plan": team.plan,
        "owner_id": current_user.user_id,
        "created_at": datetime.now().isoformat()
    }
    
    teams_db[team_id] = team_data
    
    # Add owner as admin member
    member_id = f"member_{secrets.token_urlsafe(8)}"
    team_members_db[member_id] = {
        "member_id": member_id,
        "team_id": team_id,
        "user_id": current_user.user_id,
        "email": current_user.email,
        "name": current_user.email.split("@")[0],
        "role": "owner",
        "joined_at": datetime.now().isoformat()
    }
    
    return team_data


@router.get("/teams")
async def list_teams(current_user: TokenData = Depends(get_current_user)):
    """List all teams for the user"""
    user_teams = []
    for team in teams_db.values():
        # Check if user is a member
        is_member = any(m["team_id"] == team["team_id"] and m["user_id"] == current_user.user_id 
                       for m in team_members_db.values())
        if is_member:
            member_count = sum(1 for m in team_members_db.values() if m["team_id"] == team["team_id"])
            user_teams.append({
                **team,
                "member_count": member_count
            })
    return user_teams


@router.get("/teams/{team_id}")
async def get_team(
    team_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Get team details"""
    team = teams_db.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check membership
    is_member = any(m["team_id"] == team_id and m["user_id"] == current_user.user_id 
                   for m in team_members_db.values())
    if not is_member:
        raise HTTPException(status_code=403, detail="Not a member of this team")
    
    members = [m for m in team_members_db.values() if m["team_id"] == team_id]
    return {**team, "members": members}


@router.post("/teams/{team_id}/invite")
async def invite_member(
    team_id: str,
    invite: MemberInvite,
    current_user: TokenData = Depends(get_current_user)
):
    """Invite a member to the team"""
    team = teams_db.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is owner or admin
    membership = next((m for m in team_members_db.values() 
                     if m["team_id"] == team_id and m["user_id"] == current_user.user_id), None)
    if not membership or membership["role"] not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="Only owners and admins can invite members")
    
    valid_roles = ["admin", "member", "viewer"]
    if invite.role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {valid_roles}")
    
    invitation_id = f"inv_{secrets.token_urlsafe(12)}"
    
    invitation = {
        "invitation_id": invitation_id,
        "team_id": team_id,
        "email": invite.email,
        "role": invite.role,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now().timestamp() + 7*24*3600),  # 7 days
        "invited_by": current_user.user_id
    }
    
    invitations_db[invitation_id] = invitation
    
    return invitation


@router.get("/teams/{team_id}/invitations")
async def list_invitations(
    team_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """List pending invitations"""
    team = teams_db.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    membership = next((m for m in team_members_db.values() 
                     if m["team_id"] == team_id and m["user_id"] == current_user.user_id), None)
    if not membership or membership["role"] not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    team_invitations = [i for i in invitations_db.values() if i["team_id"] == team_id]
    return team_invitations


@router.post("/invitations/{invitation_id}/accept")
async def accept_invitation(
    invitation_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Accept a team invitation"""
    invitation = invitations_db.get(invitation_id)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    if invitation["email"] != current_user.email:
        raise HTTPException(status_code=403, detail="This invitation was not sent to you")
    
    if invitation["status"] != "pending":
        raise HTTPException(status_code=400, detail="Invitation already processed")
    
    # Add member
    member_id = f"member_{secrets.token_urlsafe(8)}"
    team_members_db[member_id] = {
        "member_id": member_id,
        "team_id": invitation["team_id"],
        "user_id": current_user.user_id,
        "email": current_user.email,
        "name": current_user.email.split("@")[0],
        "role": invitation["role"],
        "joined_at": datetime.now().isoformat()
    }
    
    invitation["status"] = "accepted"
    
    return {"message": "Invitation accepted"}


@router.delete("/teams/{team_id}/members/{member_id}")
async def remove_member(
    team_id: str,
    member_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Remove a member from the team"""
    team = teams_db.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is owner
    membership = next((m for m in team_members_db.values() 
                     if m["team_id"] == team_id and m["user_id"] == current_user.user_id), None)
    if not membership or membership["role"] != "owner":
        raise HTTPException(status_code=403, detail="Only the owner can remove members")
    
    member = team_members_db.get(member_id)
    if not member or member["team_id"] != team_id:
        raise HTTPException(status_code=404, detail="Member not found")
    
    if member["role"] == "owner":
        raise HTTPException(status_code=400, detail="Cannot remove the owner")
    
    del team_members_db[member_id]
    return {"message": "Member removed"}


@router.get("/teams/{team_id}/usage")
async def get_team_usage(
    team_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Get team usage statistics"""
    team = teams_db.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    membership = next((m for m in team_members_db.values() 
                     if m["team_id"] == team_id and m["user_id"] == current_user.user_id), None)
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this team")
    
    # In a real app, this would fetch from database
    return {
        "team_id": team_id,
        "plan": team["plan"],
        "scans_this_month": 0,
        "api_calls_this_month": 0,
        "members": sum(1 for m in team_members_db.values() if m["team_id"] == team_id)
    }
