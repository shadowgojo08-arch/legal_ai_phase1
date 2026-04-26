import { useState } from 'react'
import {
  Scale,
  Sparkles,
  RefreshCw,
  AlertTriangle,
  Scale3D,
  BookOpen,
  MessageSquare,
  HelpCircle,
  Gavel,
  Briefcase
} from 'lucide-react'

// Types for the JSON response mapping the backend schema
interface PrecedentRow {
  citation: string;
  summary: string;
}

interface JudgeQuestionRow {
  question: string;
  answer: string;
}

interface LegalBriefResponse {
  executiveSummary: string;
  applicableSections: string[];
  keyArguments: string[];
  judgesQuestions: JudgeQuestionRow[];
  precedents: PrecedentRow[];
}

function App() {
  const [prompt, setPrompt] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [brief, setBrief] = useState<LegalBriefResponse | null>(null)

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setIsLoading(true);
    setError(null);
    setBrief(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/generate-brief', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate brief. Please try again.');
      }
      
      const data: LegalBriefResponse = await response.json();
      setBrief(data);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <>
      {/* Header */}
      <header className="app-header">
        <div className="logo-container">
          <Scale className="logo-icon" size={28} />
          <h1 className="logo-text">LexAssist <span>Pro</span></h1>
        </div>
      </header>

      {/* Main Content Layout */}
      <main className="main-container">
        
        {/* Input Area Section */}
        <section className="input-section">
          <label className="input-label" htmlFor="client-facts">
            Enter Client Facts & Case Summary
          </label>
          <div className="textarea-wrapper">
            <textarea
              id="client-facts"
              className="prompt-textarea"
              placeholder="Provide a detailed summary of the client's situation, relevant timeline, parties involved, and the specific legal query..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              disabled={isLoading}
            />
            <div className="word-count">
              {prompt.trim().split(/\s+/).filter(Boolean).length} words
            </div>
          </div>
          
          {error && (
            <div className="error-message">
              <AlertTriangle size={20} />
              <span>{error}</span>
            </div>
          )}

          <div className="action-row">
            <button 
              className="btn-primary" 
              onClick={handleGenerate}
              disabled={isLoading || !prompt.trim()}
            >
              {isLoading ? (
                <RefreshCw className="custom-loader" size={20} />
              ) : (
                <Sparkles size={20} />
              )}
              {isLoading ? 'Generating Brief...' : 'Generate Legal Brief'}
            </button>
          </div>
        </section>

        {/* Loading State */}
        {isLoading && (
          <section className="loading-container pulse">
            <div className="loader-icons">
              <Scale size={32} className="custom-loader" />
              <Search size={32} style={{ animationDelay: '0.2s' }} />
              <FileText size={32} style={{ animationDelay: '0.4s' }} />
            </div>
            <p className="loading-text">Analyzing precedents and drafting brief...</p>
          </section>
        )}

        {/* The Results Dashboard */}
        {brief && !isLoading && (
          <div className="results-dashboard">
            
            {/* 1. Executive Summary as a prominent Hero card */}
            <section className="hero-card">
              <h2 className="section-title">
                <Briefcase size={22} /> Executive Summary
              </h2>
              <div className="summary-text">
                {brief.executiveSummary}
              </div>
            </section>

            <div className="middle-grid">
              
              {/* 2. Applicable Sections / Articles as pill-shaped tags */}
              <section className="card applicable-sections">
                <h2 className="section-title">
                  <BookOpen size={22} /> Applicable Sections & Articles
                </h2>
                <div className="tags-container">
                  {brief.applicableSections && brief.applicableSections.map((section, idx) => (
                    <span key={idx} className="tag">
                      <Scale3D size={14} /> {section}
                    </span>
                  ))}
                </div>
              </section>

              {/* 3. Key Arguments in a styled list */}
              <section className="card card-key-arguments">
                <h2 className="section-title">
                  <Gavel size={22} /> Key Arguments
                </h2>
                <div className="arguments-list">
                  {brief.keyArguments && brief.keyArguments.map((arg, idx) => (
                    <div key={idx} className="argument-item">
                      <div className="argument-number">{idx + 1}</div>
                      <div className="argument-text">{arg}</div>
                    </div>
                  ))}
                </div>
              </section>
              
            </div>

            {/* 4. Judge's Questions in Q&A Card layout */}
            <section className="card qa-section">
              <h2 className="section-title">
                <HelpCircle size={22} /> Anticipated Judge's Questions
              </h2>
              <div className="questions-list">
                {brief.judgesQuestions && brief.judgesQuestions.map((qa, idx) => (
                  <div key={idx} className="qa-card">
                    <div className="qa-question">
                      <HelpCircle size={18} className="qa-question-icon" />
                      <span>{qa.question}</span>
                    </div>
                    <div className="qa-answer">
                      <MessageSquare size={18} className="qa-answer-icon" />
                      <span>{qa.answer}</span>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* 5. Precedent Summary & Citations (CRITICAL: 2-column Grid/Data Table) */}
            <section className="card table-container">
              <h2 className="section-title">
                <Scale size={22} /> Precedent Summary & Citations
              </h2>
              <table className="precedent-table">
                <thead>
                  <tr>
                    <th className="col-citation">Cititations</th>
                    <th className="col-summary">Precedent Application / Summary</th>
                  </tr>
                </thead>
                <tbody>
                  {brief.precedents && brief.precedents.map((prec, idx) => (
                    <tr key={idx}>
                      <td>
                        <div className="citation-text">{prec.citation}</div>
                      </td>
                      <td>
                        <div className="summary-text-td">{prec.summary}</div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>

          </div>
        )}
      </main>
    </>
  )
}

// Temporary manual imports to prevent missing icon issues just in case
const Search = ({ size, style }: any) => <svg style={style} width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>;
const FileText = ({ size, style }: any) => <svg style={style} width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>;

export default App
