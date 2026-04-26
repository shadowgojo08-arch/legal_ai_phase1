# Legal AI Assistant for Indian Court Lawyers(most important part to read)
## This is also my MLH sample code submission
An AI-powered assistant that retrieves Supreme Court precedents and generates comprehensive legal briefs using RAG (Retrieval-Augmented Generation) with Google Gemini API.
That just was the intro in this project i tried  to build the go to platform for lawyers 
i tested and trained this with a 8k case opensource data base locally ()
you could load any database of your choice on your system and convert it into vector store using the intake then could use the main.py to run the app with the below process
its still on working stages i am working to add a database dashboard on the site where previous CASES with list of key argument,dates and other details with sources are cited 
### currently it solves the most basic but critical problem for lawyers which is to find similar cases and ruling and it searches the the vector database apply similarity searches then find the most relvent cases then the agetic part wakes up summarise key points from those cases and then user get the answer with relevent cases and sources on the frontend dashboard  
### i am improving continously and working on improving the docs and  implementing new features as mentioned above this is just the phase_1/proto_1 of the project or should say solution

## 🎯 Features

- **Precedent Retrieval**: Search Indian Supreme Court judgments using semantic similarity
- **Legal Brief Generation**: Create structured legal briefs with arguments, judge questions, and precedent analysis
- **Vector Search**: Fast similarity search using ChromaDB
- **REST API**: FastAPI backend with full CORS support
- **Modern Frontend**: React + TypeScript interface for lawyers(made with the help of ai)

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher  
- Google Gemini API Key (get free at [ai.google.dev](https://ai.google.dev))

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd legal-ai-solution
   ```

2. **Create Python virtual environment**
   ```bash
   # Windows
   python -m venv lgenv
   lgenv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv lgenv
   source lgenv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env and add your Google Gemini API key
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

5. **Start the API server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   - API will be available at `http://localhost:8000`
   - API docs at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   - Frontend will be available at `http://localhost:5173`

## 📚 API Endpoints

### POST `/ask`
Generate a legal brief for a lawyer's query.

**Request:**
```json
{
  "prompt": "Client was injured in a hit-and-run case. What are the liability implications under Indian law?"
}
```

**Response:**
```json
{
  "answer": "EXECUTIVE SUMMARY:\nBased on the retrieved precedents..."
}
```

### POST `/api/generate-brief`
Generate a structured legal brief in JSON format.

**Request:**
```json
{
  "prompt": "Client's legal fact pattern..."
}
```

**Response:**
```json
{
  "executiveSummary": "...",
  "applicableSections": ["Section 304A IPC", "..."],
  "keyArguments": ["...", "..."],
  "judgesQuestions": [
    {
      "question": "Question 1?",
      "answer": "Answer..."
    }
  ],
  "precedents": [
    {
      "citation": "Case Name, Year",
      "summary": "Brief summary"
    }
  ]
}
```

## 🏗️ Project Structure

```
legal-ai-solution/
├── main.py                          # FastAPI application
├── intake.py                        # Document processing & embeddings
├── retrieval.py                     # RAG retrieval logic
├── requirements.txt                 # Python dependencies
├── .env.example                     # Example environment file
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── SETUP_ANALYSIS.md               # Detailed setup analysis
│
├── frontend/                        # React + TypeScript SPA
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── assets/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── .gitignore
│
├── data/
│   └── sc_judgments_db/            # ChromaDB vector store (local SQLite)
│       └── chroma.sqlite3
│
└── saved_files/                    # Processed documents storage
```

## 🔧 Environment Variables

Create a `.env` file in the root (copy from `.env.example`):

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```


## 📋 Tech Stack

### Backend
- **Framework**: FastAPI (async web framework)
- **Server**: Uvicorn (ASGI server)
- **LLM**: Google Gemini API (google-genai)
- **Vector DB**: ChromaDB (local, SQLite-backed)
- **Embeddings**: Sentence Transformers
- **Document Processing**: LangChain, PyMuPDF, Unstructured
- **NLP**: Transformers, Spacy
- **ML**: NumPy, SciPy, Scikit-learn, PyTorch
### FRONTEND IS made with the help of ai and anti gravity
### Frontend
- **Framework**: React 19
- **Language**: TypeScript
- **Build Tool**: Vite
- **UI Components**: Lucide React (icons)
- **Linting**: ESLint

## 🎓 How It Works

1. **Document Processing**: Legal documents are loaded using PyMuPDF/Unstructured
2. **Chunking**: Documents are split into semantic chunks
3. **Embeddings**: Chunks are converted to embeddings using Sentence Transformers
4. **Vector Storage**: Embeddings stored in ChromaDB for fast retrieval
5. **Query Processing**: User query is embedded with same model
6. **Semantic Search**: Top-K similar documents retrieved via cosine similarity
7. **LLM Generation**: Google Gemini generates structured brief using retrieved context

## 🧪 Testing

### Test Backend API
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is the liability in a negligence case?"}'
```

### Interactive API Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📦 Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.135.2 | Web framework |
| google-genai | 2.1.0 | AI model API |
| chromadb | 1.5.5 | Vector database |
| sentence-transformers | 5.3.0 | Text embeddings |
| langchain | 1.2.13 | Document processing |
| torch | 2.11.0 | ML computation |
| react | 19.2.4 | Frontend framework |
| vite | 8.0.1 | Build tool |

See `requirements.txt` for complete list.

## ⚙️ Configuration

### API Model Configuration
The system uses `gemini-2.0-flash` as the LLM model. To change:
- Edit `main.py` line 62 and 100
- Change `model="gemini-2.0-flash"` to desired model

### CORS Configuration
Currently allows all origins for development (`allow_origins=["*"]`). For production:
- Edit `main.py` line 25
- Set specific allowed origins: `allow_origins=["https://yourdomain.com"]`

### Vector DB Configuration
- Default collection: `indian_court_cases`
- Default path: `../data/sc_judgments_db`
- Backend: SQLite (no additional setup needed)

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Ensure virtual environment is activated
lgenv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### API key issues
- Verify `.env` file exists and contains valid `GEMINI_API_KEY`
- Get free API key at https://aistudio.google.com/apikey

### Frontend can't reach backend
- Ensure backend is running on `http://localhost:8000`
- Check CORS configuration in `main.py`
- Verify no firewall blocking port 8000

### Vector DB issues
- Ensure `data/sc_judgments_db/` directory exists
- ChromaDB uses local SQLite, no external DB needed
- Delete `chroma.sqlite3` to reset if needed

## 📝 Development

### Install development dependencies (optional)
```bash
# For code formatting (optional)
pip install black flake8

# Frontend linting
cd frontend && npm run lint
```

### Code Structure

**main.py** - API endpoints
- `/ask` - Get legal brief
- `/api/generate-brief` - Get structured brief

**intake.py** - Data ingestion
- `pdf_loader` - Load PDFs
- `VectorStore` - Manage ChromaDB
- `embedding_model` - Create embeddings

**retrieval.py** - Search & retrieval
- `RAGRetriever` - Retrieve similar documents

## 🚀 Deployment

### Local Testing
```bash
# Terminal 1 - Backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### Production Build
```bash
# Frontend
cd frontend
npm run build

# Backend - use production ASGI server
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 📄 License

MIT License - Feel free to use for educational and commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request


## ⚠️ Important Notes

- **API Key Security**: Never commit `.env` file. Add to `.gitignore`.
- **Vector DB**: Uses local SQLite. No external database needed.
- **CORS**: Currently allows all origins. Configure for production.
- **Model Availability**: Ensure `gemini-2.0-flash` is available in your region.
- **Large Documents**: Processing very large PDFs may take time and memory.(mine took more than 3 hrs to get converted and stored)

---

**Last Updated**: April 2026  
**Python Version**: 3.10+  
**Node Version**: 18+
