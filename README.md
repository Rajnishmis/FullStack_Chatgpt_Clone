# 💬 ChatGPT Clone – AI Conversational Platform

## 🧭 Overview

This project is a **ChatGPT-style conversational AI web application** built using **FastAPI**, **SQLAlchemy**, and **Streamlit**.
It demonstrates a modular architecture where the **backend** manages authentication, user sessions, and database interactions, while the **frontend** provides an interactive chat interface for end users.

The system integrates natural language capabilities using an LLM API (OpenAI or compatible) and serves as a foundation for experimenting with AI chat features, structured reasoning, and API-driven data extensions (like weather information).

---

## 🧩 Architecture

The application follows a **two-tier architecture**:

```
Client (Frontend)
└── Streamlit UI
      │
      ├── Sends user prompts → FastAPI endpoints
      ├── Displays model responses in chat layout
      └── Handles session state & message history

Server (Backend)
└── FastAPI App
      ├── Auth Router: Handles login & signup
      ├── Chat Router: Manages chat interaction & model response
      ├── Database Layer (SQLAlchemy + Alembic)
      ├── Weather Utility: External API example integration
      └── PostgreSQL: Stores user, session, and message data
```

This structure separates UI, business logic, and data persistence layers, enabling scalability and maintainability.

---

## ⚙️ Tech Stack

| Layer          | Technology            | Purpose                            |
| -------------- | --------------------- | ---------------------------------- |
| **Frontend**   | Streamlit             | Interactive chat interface         |
| **Backend**    | FastAPI               | Core API framework                 |
| **ORM**        | SQLAlchemy            | Object-relational mapping          |
| **Database**   | PostgreSQL            | Persistent data storage            |
| **Migrations** | Alembic               | Schema version control             |
| **Auth**       | OAuth2 + JWT          | Secure user login & token handling |
| **Utils**      | Custom Python modules | Weather API, password hashing      |

---

## 📁 Folder Structure

```
ChatGpt_Clone/
├── backend/
│   ├── alembic/                    # Database migration scripts
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── database.py             # PostgreSQL connection setup
│   │   ├── models.py               # SQLAlchemy models (User, Session, Message)
│   │   ├── schemas.py              # Pydantic models for request/response validation
│   │   ├── routers/
│   │   │   ├── auth_router.py      # Authentication endpoints (login/register)
│   │   │   └── chat_router.py      # Chat and message handling routes
│   │   ├── utils/
│   │   │   ├── hashing.py          # Password hashing and verification
│   │   │   ├── weather.py          # External Weather API integration
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env                        # Environment configuration variables
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ChatGPT_Clone.git
cd ChatGPT_Clone/backend
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend root:

```
DATABASE_URL=postgresql://username:password@localhost:5432/chatgpt_clone
SECRET_KEY=your_secret_key
ALGORITHM=HS256
OPENAI_API_KEY=your_openai_key
```

### 5. Run Alembic Migrations

```bash
alembic upgrade head
```

### 6. Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

### 7. Launch Streamlit Frontend

In a new terminal:

```bash
cd ../frontend
streamlit run app.py
```

Your ChatGPT clone should now be running at:
👉 **Frontend:** `http://localhost:8501`
👉 **Backend API:** `http://127.0.0.1:8000/docs`

---

## 💡 Key Features

* 🔐 **User Authentication:** Secure signup and login via JWT.
* 💬 **Conversational Chat:** Real-time dialogue using LLM APIs.
* 📜 **Chat History:** Session-based message tracking.
* 🌦️ **Weather Integration:** Example of dynamic API-based context enrichment.
* 🧱 **Modular Codebase:** Clear separation of routers, models, and utilities.
* 🧩 **Database Migrations:** Version-controlled schema management via Alembic.

---

## 🔮 Future Enhancements

* Integrate message streaming for live token updates.
* Add multi-model selection (GPT-3.5, GPT-4, custom fine-tuned).
* Enhance frontend UX with chat history sidebar.
* Introduce admin analytics dashboard (usage, token cost tracking).

---

## 🧑‍💻 Author

**Rajnish Mishra**
