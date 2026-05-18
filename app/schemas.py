from pydantic import BaseModel, EmailStr, Field


class RegisterSchema(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=20
    )

    email: EmailStr

    password: str = Field(
        min_length=6
    )


class LoginSchema(BaseModel):

    email: EmailStr

    password: str


class TicketSchema(BaseModel):

    title: str = Field(
        min_length=3,
        max_length=100
    )

    description: str = Field(
        min_length=5
    )

    priority: str


class FeedbackSchema(BaseModel):

    rating: int = Field(
        ge=1,
        le=5
    )

    comment: str = Field(
        min_length=3
    )


    