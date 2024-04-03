from pydantic import BaseModel, Field, EmailStr

class TextToSpeechSchema(BaseModel):
    model: str = Field(default="gpt-4-1106-preview")
    role: str = Field(default="user")
    voice: str = Field(default="alloy")
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "model": "gpt-4-1106-preview",
                "role": "user",
                # có các voice alloy|echo|fable|onyx|nova|shimmer
                "voice": "alloy",
                "content": "Xin chào các bạn nhé"
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@xyz.com",
                "password": "any"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        }
