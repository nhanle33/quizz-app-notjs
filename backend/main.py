import sqlite3
import hashlib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allow CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QUESTIONS = [
    {
        "id": 1,
        "question": "React là thư viện của ngôn ngữ nào?",
        "options": ["Python", "JavaScript", "Java", "C#"],
        "correct_answer": "JavaScript"
    },
    {
        "id": 2,
        "question": "Thẻ nào sau đây dùng để tạo một liên kết (link) trong HTML?",
        "options": ["<a>", "<link>", "<href>", "<nav>"],
        "correct_answer": "<a>"
    },
    {
        "id": 3,
        "question": "FastAPI được viết bằng ngôn ngữ lập trình nào?",
        "options": ["Go", "NodeJS", "JavaScript", "Python"],
        "correct_answer": "Python"
    },
    {
        "id": 4,
        "question": "Cổng mặc định (port) khi chạy uvicorn FastAPI là gì?",
        "options": ["8000", "3000", "8080", "5000"],
        "correct_answer": "8000"
    },
    {
        "id": 5,
        "question": "Trong React, hook nào dùng để quản lý state của component?",
        "options": ["useEffect", "useMemo", "useState", "useContext"],
        "correct_answer": "useState"
    }

]

class Answer(BaseModel):
    question_id: int
    selected_answer: str

class SubmitRequest(BaseModel):
    answers: List[Answer]

# --- Database & Auth Setup ---
def init_db():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password: str) -> str:
    # Trả về trực tiếp mật khẩu gốc thay vì mã hóa để có thể xem trong DB theo yêu cầu
    return password

class UserAuth(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: UserAuth):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (user.username, hash_password(user.password)))
        conn.commit()
        return {"message": "Đăng ký thành công!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại")
    finally:
        conn.close()

@app.post("/login")
def login(user: UserAuth):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", 
                   (user.username, hash_password(user.password)))
    user_record = cursor.fetchone()
    conn.close()
    
    if user_record:
        return {"message": "Đăng nhập thành công", "username": user.username}
    raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu")

@app.get("/questions")
def get_questions():
    # Không trả về correct_answer để bảo mật
    return [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        }
        for q in QUESTIONS
    ]

@app.post("/submit")
def submit_answers(request: SubmitRequest):
    correct_count = 0
    results = []
    
    questions_dict = {q["id"]: q for q in QUESTIONS}

    for answer in request.answers:
        q_id = answer.question_id
        selected = answer.selected_answer
        correct_answer = questions_dict.get(q_id, {}).get("correct_answer")
        
        is_correct = (selected == correct_answer)
        if is_correct:
            correct_count += 1
            
        results.append({
            "question_id": q_id,
            "selected_answer": selected,
            "is_correct": is_correct,
            "correct_answer": correct_answer
        })
        
    score = (correct_count / len(QUESTIONS)) * 10
    
    return {
        "correct_count": correct_count,
        "total": len(QUESTIONS),
        "score": round(score, 1),
        "results": results
    }
