#  AI Desktop Support Assistant

AI Desktop Support Assistant is a full-stack AI-powered IT helpdesk web application built using FastAPI, PostgreSQL, JavaScript, HTML, and CSS. The application helps users troubleshoot desktop and technical issues using AI-generated responses and includes real-world IT support features such as ticket management and system diagnostics.

---

# 🚀 Live Demo

🔗 Live Project: https://ai-desktop-support.onrender.com

🔗 GitHub Repository: https://github.com/rajat-gupta87/AI-Desktop-Support

---

#  Features

* AI-powered desktop troubleshooting
* JWT authentication system
* User registration and login
* User-wise chat history
* Screenshot upload support
* System diagnostics monitoring
* IT ticket management system
* Close and delete ticket functionality
* Delete chat history
* Responsive dark UI
* PostgreSQL database integration

---

#  Technologies Used

## Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication
* Groq API

## Frontend

* HTML
* CSS
* JavaScript

---

#  Project Structure

```text
backend/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   └── ai.py
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── requirements.txt
├── render.yaml
└── README.md
```

---

#  Installation

## Clone Repository

```bash
git clone https://github.com/rajat-gupta87/AI-Desktop-Support.git
```

## Open Project

```bash
cd backend
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

#  Run Project

```bash
python -m uvicorn app.main:app --reload
```

Open browser:

```text
http://127.0.0.1:8000
```

---

# 🌐 Deployment

This project is deployed using:

* Render
* Neon PostgreSQL

---

#  Future Improvements

* Voice assistant integration
* Admin dashboard
* Ticket assignment system
* Email notifications
* Live notifications
* AI analytics dashboard

---

#  Author

Rajat Gupta

---

#  License

This project is created for educational and portfolio purposes.
