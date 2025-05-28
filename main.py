from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into environment


# --- Set up LangChain QA engine only once ---
conn = sqlite3.connect('face_recognition.db')

# Load tables
reg_df = pd.read_sql_query("SELECT name, registration_time FROM registrations", conn)
reg_df['registration_time'] = pd.to_datetime(reg_df['registration_time']).astype(str)
reg_df = reg_df.drop_duplicates()

recog_df = pd.read_sql_query("SELECT name, recognized_at FROM recognition_logs", conn)
recog_df['recognized_at'] = pd.to_datetime(recog_df['recognized_at']).astype(str)
recog_df = recog_df.drop_duplicates()

conn.close()

# Format to plain text
reg_text = "\n".join([f"{row['name']} registered at {row['registration_time']}." for _, row in reg_df.iterrows()])
recog_text = "\n".join([f"{row['name']} was recognized at {row['recognized_at']}." for _, row in recog_df.iterrows()])
combined_text = reg_text + "\n" + recog_text

# Vectorization
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
documents = text_splitter.create_documents([combined_text])
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = FAISS.from_documents(documents, embedding_model)

# LLM + QA chain
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.4,
    max_output_tokens=512,
)


qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vector_db.as_retriever())

# --- FastAPI ---
app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    

@app.post("/ask")
async def ask_question(request: QueryRequest):
    result = qa_chain.invoke({"query": request.query})
    return {"answer": result["result"]}
