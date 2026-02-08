from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlite3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -------------------- APP --------------------
app = FastAPI(title="Digital Shadow FULL", version="2.0")

# -------------------- DATABASE --------------------
conn = sqlite3.connect("digital_shadow.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    aggression REAL,
    positivity REAL,
    risk REAL,
    dominant TEXT,
    comment TEXT,
    created_at TEXT
)
""")

conn.commit()

# -------------------- AI MODEL --------------------
TRAIN_TEXTS = [
    "nefret ediyorum rezil sistem aptal",
    "salak insanlar sinir bozucu",
    "herkes berbat",
    "harika bir gün çok mutluyum",
    "başardım gurur duyuyorum",
    "hayat güzel seviyorum",
    "risk almayı severim",
    "kumar bahis borç",
    "kolay para hızlı kazanç"
]

TRAIN_LABELS = [
    "aggressive", "aggressive", "aggressive",
    "positive", "positive", "positive",
    "risk", "risk", "risk"
]

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(TRAIN_TEXTS)

model = LogisticRegression()
model.fit(X_train, TRAIN_LABELS)

# -------------------- MODELS --------------------
class Register(BaseModel):
    username: str

class AnalyzeRequest(BaseModel):
    username: str
    texts: List[str]

class AnalysisResult(BaseModel):
    aggression: float
    positivity: float
    risk: float
    dominant_trait: str
    ai_comment: str

# -------------------- HELPERS --------------------
def get_user_id(username: str):
    cur.execute("SELECT id FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    return row[0] if row else None

def ai_analyze(texts: List[str]):
    joined = " ".join(texts).lower()
    X = vectorizer.transform([joined])
    probs = model.predict_proba(X)[0]
    labels = model.classes_

    scores = dict(zip(labels, probs))

    aggr = float(scores.get("aggressive", 0))
    pos = float(scores.get("positive", 0))
    risk = float(scores.get("risk", 0))

    dominant = max(scores, key=scores.get)

    if dominant == "aggressive":
        comment = "Sert, tepkisel ve çatışmaya açık bir dijital profil."
    elif dominant == "positive":
        comment = "Pozitif, yapıcı ve sosyal bir dijital iz."
    else:
        comment = "Risk almaya yatkın, hızlı kazanç odaklı bir profil."

    return round(aggr,2), round(pos,2), round(risk,2), dominant, comment

# -------------------- API --------------------
@app.post("/register")
def register(data: Register):
    try:
        cur.execute("INSERT INTO users(username) VALUES(?)", (data.username,))
        conn.commit()
        return {"status": "ok", "message": "User created"}
    except:
        raise HTTPException(400, "Username already exists")

@app.post("/analyze", response_model=AnalysisResult)
def analyze(data: AnalyzeRequest):
    user_id = get_user_id(data.username)
    if not user_id:
        raise HTTPException(404, "User not found")

    aggr, pos, risk, dom, comment = ai_analyze(data.texts)

    cur.execute("""
    INSERT INTO analyses(user_id, aggression, positivity, risk, dominant, comment, created_at)
    VALUES(?,?,?,?,?,?,?)
    """, (user_id, aggr, pos, risk, dom, comment, datetime.utcnow().isoformat()))
    conn.commit()

    return {
        "aggression": aggr,
        "positivity": pos,
        "risk": risk,
        "dominant_trait": dom,
        "ai_comment": comment
    }

@app.get("/history/{username}")
def history(username: str):
    user_id = get_user_id(username)
    if not user_id:
        raise HTTPException(404, "User not found")

    cur.execute("""
    SELECT aggression, positivity, risk, dominant, comment, created_at
    FROM analyses WHERE user_id=?
    ORDER BY created_at DESC
    """, (user_id,))

    return cur.fetchall()
