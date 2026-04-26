# Project Analysis & Setup Guide

## Project Overview
This is a **Legal AI Assistant** with:
- **Backend**: FastAPI-based RAG (Retrieval-Augmented Generation) system for Indian legal precedents
- **Frontend**: React + TypeScript + Vite SPA for lawyer interface
- **Database**: ChromaDB for vector storage of Supreme Court judgments

---

## ✅ CLEANED REQUIREMENTS (Use These)

### **Backend - requirements.txt** (Essentials Only)
```
# Web Framework
fastapi==0.135.2
uvicorn==0.42.0
python-multipart==0.0.22

# LLM & AI
google-genai==2.1.0
langchain==1.2.13
langchain-core==1.2.23
langchain-community==0.4.1

# Vector DB & Embeddings
chromadb==1.5.5
sentence-transformers==5.3.0
numpy==2.4.3

# Document Processing
pypdf==6.9.2
PyMuPDF==1.27.2.2
unstructured==0.22.6
beautifulsoup4==4.14.3

# Data Processing & Utils
python-dotenv==1.2.2
pydantic==2.12.5
requests==2.33.0

# Machine Learning Support
scikit-learn==1.8.0
scipy==1.17.1
torch==2.11.0
transformers==5.4.0
```

### **Frontend - package.json** (Already Good)
```json
{
  "dependencies": {
    "react": "^19.2.4",
    "react-dom": "^19.2.4",
    "lucide-react": "^1.7.0"
  },
  "devDependencies": {
    "typescript": "~5.9.3",
    "vite": "^8.0.1",
    "@vitejs/plugin-react": "^6.0.1",
    "eslint": "^9.39.4",
    "@types/react": "^19.2.14",
    "@types/react-dom": "^19.2.3"
  }
}
```

---

## 🔴 CRITICAL ISSUES TO FIX

### 1. **Security: .env File Committed**
- **Problem**: `.env` contains `GEMINI_API_KEY` and is version controlled
- **Fix**: Add to `.gitignore` immediately
- **Risk**: Anyone cloning repo will see your API key

### 2. **Missing Root .gitignore**
- **Problem**: Only frontend has `.gitignore`, root has none
- **Fix**: Create `.gitignore` in project root (see below)

### 3. **Broken requirement2.txt**
- **Problem**: Has `genai` (uninstalled) instead of `google-genai`
- **Problem**: Has `fastapi uvicorn` on same line (should be separate)
- **Problem**: Missing spacy, scipy, torch needed for NLP

### 4. **Duplicate Entries in requirements.txt**
- **Problem**: All packages repeated twice
- **Fix**: Clean it up, keep only one copy

### 5. **Wrong API Model Name**
- **File**: `main.py` line 62 and 100
- **Problem**: Uses `gemini-3-flash-preview` (preview model, may be deprecated)
- **Fix**: Change to `gemini-2.0-flash` or `gemini-1.5-flash`

### 6. **Virtual Environment in Git**
- **Problem**: `lgenv/` folder (200MB+) should not be committed
- **Fix**: Add to `.gitignore`

### 7. **Missing Documentation**
- **Problem**: No root README.md or setup instructions
- **Problem**: No API documentation
- **Fix**: Create proper README

---

## 📝 FILES TO CREATE/UPDATE

### 1. Create Root `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
lgenv/
*.egg-info/
dist/
build/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
saved_files/
data/sc_judgments_db/chroma.sqlite3
*.db
*.sqlite3

# Frontend
frontend/node_modules/
frontend/dist/
frontend/.env.local

# OS
.DS_Store
Thumbs.db
```

### 2. Fix `requirement2.txt` → Delete and Use `requirements.txt` Instead
- You don't need two files. Keep one clean `requirements.txt`

### 3. Create Root `README.md`
```markdown
# Legal AI Assistant for Indian Court Lawyers

AI-powered assistant that retrieves Supreme Court precedents and generates legal briefs using RAG (Retrieval-Augmented Generation).

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API Key

### Backend Setup

1. **Clone and navigate**
   ```bash
   git clone <repo>
   cd legal-ai-solution
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or: source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

5. **Run API server**
   ```bash
   uvicorn main:app --reload
   ```
   Server runs on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run dev server**
   ```bash
   npm run dev
   ```
   Frontend runs on `http://localhost:5173`

## 📚 API Endpoints

- `POST /ask` - Get legal brief for a query
- `POST /api/generate-brief` - Generate structured legal brief (JSON)

## 🏗️ Project Structure

```
legal-ai-solution/
├── main.py              # FastAPI app
├── intake.py            # Document processing & embeddings
├── retrieval.py         # RAG retrieval logic
├── requirements.txt     # Python dependencies
├── .env                 # API keys (NOT in git)
├── frontend/            # React + TypeScript frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
└── data/
    └── sc_judgments_db/ # ChromaDB vector store
```

## 🔧 Environment Variables

Create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

## 📋 Tech Stack

**Backend:**
- FastAPI + Uvicorn
- ChromaDB (vector DB)
- Sentence Transformers (embeddings)
- Google Genai (LLM)
- LangChain (document processing)

**Frontend:**
- React 19 + TypeScript
- Vite
- Lucide React

## ⚠️ Important Notes

- Don't commit `.env` file (contains API keys)
- Vector DB uses local SQLite, no separate DB setup needed
- Frontend makes requests to `http://localhost:8000`
```

### 4. Create `.env.example`
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Update `main.py` - Fix API Model
Change:
- `gemini-3-flash-preview` → `gemini-2.0-flash`

---

## 📊 Dependency Analysis

| Package | Purpose | Required |
|---------|---------|----------|
| fastapi | Web framework | ✅ ESSENTIAL |
| uvicorn | ASGI server | ✅ ESSENTIAL |
| google-genai | LLM calls | ✅ ESSENTIAL |
| chromadb | Vector DB | ✅ ESSENTIAL |
| sentence-transformers | Embeddings | ✅ ESSENTIAL |
| langchain* | Document processing | ✅ ESSENTIAL |
| pypdf, PyMuPDF | PDF reading | ✅ ESSENTIAL |
| unstructured | Document parsing | ✅ ESSENTIAL |
| numpy, scipy, torch | ML math ops | ✅ ESSENTIAL |
| python-dotenv | ENV management | ✅ ESSENTIAL |
| requests | HTTP client | ✅ ESSENTIAL |
| beautifulsoup4 | HTML parsing | ⚠️ Nice-to-have |
| scikit-learn | ML utilities | ⚠️ Optional |
| spacy, transformers | NLP extras | ⚠️ Optional |

**Remove bloat**: The original `requirements.txt` has 200+ packages. Most are sub-dependencies. The list above has only direct dependencies needed.

---

## 🎯 Before Uploading to GitHub

- [ ] Delete or clean `requirements.txt` (remove duplicates)
- [ ] Fix `.env` - add to `.gitignore`, create `.env.example` instead
- [ ] Create root `.gitignore`
- [ ] Update `main.py`: Change `gemini-3-flash-preview` to `gemini-2.0-flash`
- [ ] Create root `README.md` with setup instructions
- [ ] Add `CORS_ORIGINS` config if deploying (currently allows all: `["*"]`)
- [ ] Test: `pip install -r requirements.txt`, then run locally
- [ ] Verify: Both backend and frontend start successfully

---

## 🚀 Deployment Checklist

**For Others Cloning:**
1. Instructions match our README ✅
2. Only actual code in git (no venv, node_modules, .env) ✅
3. Clear API documentation ✅
4. Requirements file is clean & minimal ✅
5. API model name works (not deprecated) ✅
6. No hardcoded API keys ✅
