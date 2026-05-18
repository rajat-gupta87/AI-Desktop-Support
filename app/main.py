from fastapi import FastAPI, Header, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.database import SessionLocal, Base, engine
from app.schemas import RegisterSchema, LoginSchema, TicketSchema

from app.models import User, ChatHistory, Ticket
from app.auth import create_access_token, verify_token

from app.ai import ask_ai
from passlib.context import CryptContext
import shutil
import os
import uuid
import psutil
import platform


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



def get_current_user_id(authorization):

    if not authorization:
        return None

    try:

        token = authorization.split(" ")[1]

        payload = verify_token(token)

        if not payload:
            return None

        return payload.get("user_id")

    except:
        return None


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/login-page")
def login_page():
    return FileResponse("static/login.html")


@app.get("/register-page")
def register_page():
    return FileResponse("static/register.html")



class ChatRequest(BaseModel):

    message: str

    screenshot: str | None = None


@app.post("/chat")
def chat(
    data: ChatRequest,
    authorization: str = Header(None)
):

    user_id = get_current_user_id(
        authorization
    )

    if not user_id:
        return {
            "message": "Invalid token"
        }

    db = SessionLocal()

    ai_response = ask_ai(
        data.message,
        data.screenshot
    )

    new_chat = ChatHistory(
        user_message=data.message,
        ai_response=ai_response,
        user_id=user_id
    )

    db.add(new_chat)

    db.commit()

    return {
        "response": ai_response
    }



@app.post("/register")
def register(user: RegisterSchema):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        return {
            "message": "Email already registered"
        }

    hashed_password = pwd_context.hash(
        user.password
    )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }



@app.post("/login")
def login(user: LoginSchema):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:

        return {
            "message": "User not found"
        }

    password_verified = pwd_context.verify(
        user.password,
        existing_user.password
    )

    if not password_verified:

        return {
            "message": "Invalid password"
        }

    token = create_access_token({
        "user_id": existing_user.id
    })

    return {
        "message": "Login successful",
        "access_token": token
    }


@app.get("/history")
def get_history(
    authorization: str = Header(None)
):

    user_id = get_current_user_id(
        authorization
    )

    if not user_id:
        return {
            "message": "Invalid token"
        }

    db = SessionLocal()

    chats = db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).all()

    history = []

    for chat in chats:

        history.append({
            "id": chat.id,
            "user_message": chat.user_message,
            "ai_response": chat.ai_response
        })

    return history



@app.delete("/delete-chat/{chat_id}")
def delete_chat(chat_id: int):

    db = SessionLocal()

    chat = db.query(ChatHistory).filter(
        ChatHistory.id == chat_id
    ).first()

    if not chat:

        return {
            "message": "Chat not found"
        }

    db.delete(chat)

    db.commit()

    return {
        "message": "Chat deleted"
    }



@app.post("/upload-screenshot")
async def upload_screenshot(
    file: UploadFile = File(...)
):

    os.makedirs("uploads", exist_ok=True)

    unique_name = f"{uuid.uuid4()}_{file.filename}"

    file_path = f"uploads/{unique_name}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Screenshot uploaded",
        "filename": unique_name
    }



@app.get("/system-info")
def system_info():

    return {

        "os": platform.system(),

        "os_version": platform.version(),

        "processor": platform.processor(),

        "cpu_usage": psutil.cpu_percent(),

        "ram_usage": psutil.virtual_memory().percent,

        "disk_usage": psutil.disk_usage(
            'C:\\'
        ).percent
    }



@app.post("/create-ticket")
def create_ticket(
    data: TicketSchema,
    authorization: str = Header(None)
):

    user_id = get_current_user_id(
        authorization
    )

    if not user_id:
        return {
            "message": "Invalid token"
        }

    db = SessionLocal()

    new_ticket = Ticket(
        title=data.title,
        description=data.description,
        priority=data.priority,
        user_id=user_id
    )

    db.add(new_ticket)

    db.commit()

    return {
        "message": "Ticket created successfully"
    }



@app.get("/tickets")
def get_tickets(
    authorization: str = Header(None)
):

    user_id = get_current_user_id(
        authorization
    )

    if not user_id:
        return {
            "message": "Invalid token"
        }

    db = SessionLocal()

    tickets = db.query(Ticket).filter(
        Ticket.user_id == user_id
    ).all()

    result = []

    for ticket in tickets:

        result.append({
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority
        })

    return result


@app.put("/close-ticket/{ticket_id}")
def close_ticket(ticket_id: int):

    db = SessionLocal()

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:

        return {
            "message":"Ticket not found"
        }

    ticket.status = "Closed"

    db.commit()

    return {
        "message":"Ticket closed successfully"
    }

@app.delete("/delete-ticket/{ticket_id}")
def delete_ticket(ticket_id: int):

    db = SessionLocal()

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:

        return {
            "message":"Ticket not found"
        }

    db.delete(ticket)

    db.commit()

    return {
        "message":"Ticket deleted successfully"
    }


