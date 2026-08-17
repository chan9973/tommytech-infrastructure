"""
Example API module for user management
Demonstrates the structure recognized by generate_code_docs.py
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    name: str
    email: EmailStr
    age: int


class UserResponse(BaseModel):
    """Schema for user API response"""
    id: int
    name: str
    email: EmailStr
    is_active: bool = True


def get_user(user_id: int) -> Optional[UserResponse]:
    """
    Fetch a user by ID.
    
    Args:
        user_id: The unique identifier for the user
        
    Returns:
        UserResponse if found, None otherwise
    """
    # Implementation would query database
    return None


def create_user(user: UserCreate) -> UserResponse:
    """
    Create a new user in the system.
    
    Args:
        user: User creation data
        
    Returns:
        Created user response with generated ID
    """
    # Implementation would insert into database
    return UserResponse(id=1, **user.dict())


def list_users(limit: int = 100, offset: int = 0) -> List[UserResponse]:
    """
    List users with pagination support.
    
    Args:
        limit: Maximum number of users to return
        offset: Number of users to skip
        
    Returns:
        List of user responses
    """
    return []


class UserService:
    """
    Service class for user operations.
    
    Coordinates user-related business logic and data access.
    """
    
    def __init__(self, repository: Optional[Any] = None):
        """
        Initialize user service.
        
        Args:
            repository: Optional data repository for testing
        """
        self.repository = repository
    
    def get_active_users(self) -> List[UserResponse]:
        """Get all active users in the system"""
        return list_users()
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate a user account.
        
        Returns:
            True if successful, False otherwise
        """
        return True