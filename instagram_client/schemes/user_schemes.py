from pydantic import BaseModel, Field
from typing_extensions import Any


class UserBaseScheme(BaseModel):
    user_id: int = None

    model_config = {
        "extra": "allow",
    }

class LoginResponse(UserBaseScheme):
    access_token: str = None
    permissions: list[str] = None

class UserResponse(UserBaseScheme):
    id: int = None
    username: str = None
    name: str = None
    profile_picture_url: str = None
    followers_count: int = None
    follows_count: int = None
    media_count: int = None

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="The access token provided by the API.")
    token_type: str = Field(..., description="The type of the token (e.g., 'bearer').")
    expires_in: int = Field(..., description="Number of seconds until the token expires.")


class UserProfile(BaseModel):
    id: Any = None
    name: str = None
    username: str
    profile_pic: str = None
    follower_count: int
    is_user_follow_business: bool
    is_business_follow_user: bool

    @property
    def get_name(self):
        return self.username
