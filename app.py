import pandas as pd
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# ================= LOAD DATA =================

FILE_PATH = "smartcheck_nlp_qa.xlsx"

df = pd.read_excel(FILE_PATH)

questions = df["Question"].astype(str).tolist()
answers = df["Answer"].astype(str).tolist()

# ================= LOAD MODEL =================

model = SentenceTransformer("all-MiniLM-L6-v2")

question_embeddings = model.encode(
    questions,
    convert_to_tensor=True
)

# ================= FASTAPI APP =================

app = FastAPI(title="Semantic Q&A System")

@app.post("/ask")
def ask_question(user_question: str):
    user_embedding = model.encode(user_question, convert_to_tensor=True)

    scores = cos_sim(user_embedding, question_embeddings)[0]
    best_idx = scores.argmax().item()

    # Top 2 related questions
    top_indices = scores.argsort(descending=True)[1:3]
    related_questions = [questions[i] for i in top_indices]

    return {
        "answer": answers[best_idx],
        "related_questions": related_questions
    }
