from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from typing import Annotated, List, Dict, Any
import uvicorn
import tempfile
import os

from intake import VectorStore, embedding_model, pdf_loader
from retrieval import RAGRetriever
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client()

import json


class PromptRequest(BaseModel):
    prompt: str
@app.post("/ask")
def ask(request: PromptRequest):
    retriever_instance = RAGRetriever(vector_store=VectorStore(
        collection_name="indian_court_cases", 
        persist_directory="../data/sc_judgments_db"
    ), embedding_model=embedding_model())    
    # Call the retrieve method and store the results in a variable
    results = retriever_instance.retrieve(
        query=request.prompt, 
        top_k=3, 
        score_threshold=0.2 
    )
    case1 = case2 = case3 = None

    # Assign based on what was actually found
    if len(results) >= 1:
        case1 = results[0]
    if len(results) >= 2:
        case2 = results[1]
    if len(results) >= 3:
        case3 = results[2]
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""SYSTEM:
You are an elite legal strategist and assistant for an Indian Court lawyer. 
Your job is to analyze the provided Client Facts and the Retrieved Legal Precedents to help the lawyer prepare for a hearing. 

Do not invent laws or precedents. If the retrieved cases do not fully answer the question, state that clearly.

RETRIEVED PRECEDENTS:
{case1 if case1 else "No relevant precedent found."}
{case2 if case2 else "No relevant precedent found."}
{case3 if case3 else "No relevant precedent found."}

CLIENT FACTS:
{request.prompt}

YOUR TASK:
Based ONLY on the precedents and facts above, generate a preparation brief for the lawyer. You must structure your response exactly as follows:

1. EXECUTIVE SUMMARY: A 2-paragraph summary of the client's legal standing.
2. APPLICABLE SECTIONS/ARTICLES: List the specific Indian laws or sections relevant to this case.
3. KEY ARGUMENTS: 3 to 5 strong arguments the lawyer should make in court.
4. JUDGE'S QUESTIONS: 3 difficult questions the judge is likely to ask, and how the lawyer should answer them.
5. PRECEDENT SUMMARY: A brief 1-sentence summary of how each of the 3 retrieved cases applies to the client's situation, including citations."""
    )

    return {"answer": response.text}

@app.post("/api/generate-brief")
def generate_brief(request: PromptRequest):
    retriever_instance = RAGRetriever(vector_store=VectorStore(), embedding_model=embedding_model())    
    results = retriever_instance.retrieve(
        query=request.prompt, 
        top_k=3, 
        score_threshold=0.2 
    )
    case1 = case2 = case3 = None

    if len(results) >= 1:
        case1 = results[0]
    if len(results) >= 2:
        case2 = results[1]
    if len(results) >= 3:
        case3 = results[2]
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""SYSTEM:
You are an elite legal strategist and assistant for an Indian Court lawyer. 
Your job is to analyze the provided Client Facts and the Retrieved Legal Precedents to help the lawyer prepare for a hearing. 

Do not invent laws or precedents. If the retrieved cases do not fully answer the question, state that clearly.

RETRIEVED PRECEDENTS:
{case1 if case1 else "No relevant precedent found."}
{case2 if case2 else "No relevant precedent found."}
{case3 if case3 else "No relevant precedent found."}

CLIENT FACTS:
{request.prompt}

YOUR TASK:
Based ONLY on the precedents and facts above, generate a preparation brief for the lawyer. 
You MUST return the output as a strictly valid JSON object. Do NOT wrap it in markdown code blocks (e.g., ```json).
The JSON object must have exactly the following structure:
{{
  "executiveSummary": "A 2-paragraph summary of the client's legal standing.",
  "applicableSections": ["law or section 1", "law or section 2"],
  "keyArguments": ["argument 1", "argument 2", "argument 3"],
  "judgesQuestions": [
    {{ "question": "Question 1", "answer": "Answer 1" }},
    {{ "question": "Question 2", "answer": "Answer 2" }}
  ],
  "precedents": [
    {{ "citation": "citation 1", "summary": "brief summary of precedent 1" }}
  ]
}}"""
    )
    
    # Strip markdown block if model still outputs it
    text = response.text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    try:
        return json.loads(text)
    except Exception as e:
        return {"error": "Failed to parse API response as JSON", "raw": response.text}
#for future updatess in the website as i am planning to add document analysis as a seprate feature
@app.post("/process-doc")
async def handle_upload(user_pdf: UploadFile = File(...)):
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        content = await user_pdf.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        # Pass the file path to pdf_reader
        pdf_data = pdf_loader.pdf_reader(temp_file_path)
        return {"message": f"Received {user_pdf.filename}", "pdf_data": pdf_data}
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)





