from pydantic import BaseModel


class RegisterSchema(BaseModel):

    username: str

    email: str

    password: str


class LoginSchema(BaseModel):

    email: str

    password: str


class TicketSchema(BaseModel):

    title: str

    description: str

    priority: str