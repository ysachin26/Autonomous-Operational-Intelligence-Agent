import { useState } from 'react';
import './App.css';




function App() {
  const [step, setStep] = useState('form');
  const [formData, setFormData] = useState({
    personName: '',
    personTitle: '',
    personEmail: '',
    companyName: '',
    companySize: '',
    companyIndustry: '',
    notesRaw: '',
  });
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeLead = async (data) => {
    const AGENTIC_API_KEY = import.meta.env.VITE_AGENTIC_API_KEY;
    // Using a mock endpoint for demonstration
    const API_ENDPOINT = 'https://api.agentic.ai/v1/analyze_lead'; 

    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${AGENTIC_API_KEY}`
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`API call failed with status ${response.status}`);
    }

    return response.json();
  };

  const getMockAnalysis = (data) => ({
    score: Math.floor(Math.random() * 40) + 60,
    fitLabel: Math.random() > 0.5 ? 'EXCELLENT' : 'GOOD',
    bant: {
      budget: 'WEAK',
      authority: 'PASS',
      need: 'PASS',
      timeline: 'UNKNOWN',
      status: 'QUALIFIED'
    },
    outreach: `Subject: Reduce operational costs by 30% - ${data.companyName}`,
    priority: 'P1',
    segment: 'SaaS/Enterprise'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setStep('analyzing');

    try {
      const result = await analyzeLead(formData);
      setAnalysis(result);
    } catch (err) {
      // Fallback to mock data when API is unavailable
      setError('Live analysis failed. Using a mock analysis instead.');
      const mockResult = getMockAnalysis(formData);
      setAnalysis(mockResult);
    } finally {
      setStep('results');
      setLoading(false);
    }
  };

  if (step === 'analyzing') {
    return (
      <div className="container analyzing">
        <div className="spinner"></div>
        <h2>Analyzing Lead with ASLOA AI Agent...</h2>
        <p>Running scoring, qualification & routing models</p>
      </div>
    );
  }

  if (step === 'results' && analysis) {
    return (
      <div className="container">
        <div className="header">
          <h1>✓ Lead Analysis Complete</h1>
          <button onClick={() => {
            setStep('form');
            setFormData({
              personName: '',
              personTitle: '',
              personEmail: '',
              companyName: '',
              companySize: '',
              companyIndustry: '',
              notesRaw: '',
            });
          }} className="btn-secondary">New Lead</button>
        </div>
        {error && <div className="card error-card">{error}</div>}
        <div className="card score-card">
          <div className="score-large">{analysis.score}/100</div>
          <p className="fit-label">{analysis.fitLabel} FIT</p>
          <p>{formData.personName} @ {formData.companyName}</p>
        </div>
        <div className="card">
          <h3>BANT Qualification</h3>
          <div className="bant-grid">
            <div><strong>Budget</strong>: {analysis.bant.budget}</div>
            <div><strong>Authority</strong>: {analysis.bant.authority}</div>
            <div><strong>Need</strong>: {analysis.bant.need}</div>
            <div><strong>Timeline</strong>: {analysis.bant.timeline}</div>
          </div>
          <p><strong>Status: {analysis.bant.status}</strong></p>
        </div>
        <div className="card">
          <h3>Suggested Outreach</h3>
          <p>{analysis.outreach}</p>
        </div>
        <div className="card">
          <h3>Routing</h3>
          <p><strong>Priority:</strong> {analysis.priority}</p>
          <p><strong>Segment:</strong> {analysis.segment}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="header">
        <h1>🚀 ASLOA</h1>
        <p>AI Sales Lead Orchestration Agent</p>
      </div>
              {/* INPUT SECTION */}
        <div className="input-section">
          <div className="section-header">
            <h2>📥 Agent Input Format</h2>
            <p>The agent accepts the following input information</p>
          </div>
          <div className="input-specs">
            <div className="spec-item">
              <div className="spec-icon">👤</div>
              <div className="spec-details">
                <h3>Lead Information</h3>
                <ul>
                  <li><strong>First Name:</strong> Prospect's first name</li>
                  <li><strong>Job Title:</strong> Current job position</li>
                  <li><strong>Email:</strong> Contact email address</li>
                </ul>
              </div>
            </div>
            <div className="spec-item">
              <div className="spec-icon">🏢</div>
              <div className="spec-details">
                <h3>Company Information</h3>
                <ul>
                  <li><strong>Company Name:</strong> Organization name</li>
                  <li><strong>Company Size:</strong> 1-50, 51-200, 201-1000, 1001+</li>
                  <li><strong>Industry:</strong> SaaS, FinTech, Enterprise, Healthcare</li>
                </ul>
              </div>
            </div>
            <div className="spec-item">
              <div className="spec-icon">📝</div>
              <div className="spec-details">
                <h3>Additional Context</h3>
                <ul>
                  <li><strong>Notes:</strong> Any relevant context or notes about the prospect</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      <form onSubmit={handleSubmit} className="lead-form">
        <h3>Lead Information</h3>
        <input type="text" name="personName" placeholder="First Name" value={formData.personName} onChange={handleChange} required />
        <input type="text" name="personTitle" placeholder="Job Title" value={formData.personTitle} onChange={handleChange} required />
        <input type="email" name="personEmail" placeholder="Email" value={formData.personEmail} onChange={handleChange} required />
        
        <h3>Company Information</h3>
        <input type="text" name="companyName" placeholder="Company Name" value={formData.companyName} onChange={handleChange} required />
        <select name="companySize" value={formData.companySize} onChange={handleChange} required>
          <option value="">Company Size</option>
          <option value="1-50">1-50</option>
          <option value="51-200">51-200</option>
          <option value="201-1000">201-1000</option>
          <option value="1001+">1001+</option>
        </select>
        <select name="companyIndustry" value={formData.companyIndustry} onChange={handleChange} required>
          <option value="">Industry</option>
          <option value="SaaS">SaaS</option>
          <option value="FinTech">FinTech</option>
          <option value="Enterprise">Enterprise</option>
          <option value="Healthcare">Healthcare</option>
        </select>
        
        <h3>Additional Notes</h3>
        <textarea name="notesRaw" placeholder="Any additional context..." value={formData.notesRaw} onChange={handleChange} rows="3"></textarea>
        
        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Lead with AI'}
          </button>
          <button type="button" className="btn-secondary" onClick={() => window.location.reload()}>
            Clear
          </button>
        </div>
      </form>
              {/* OUTPUT SECTION */}
              <div className="output-section" style={{ display: step === 'results' && analysis ? 'block' : 'none' }}>
          <div className="section-header">
            <h2>📤 Agent Output Results</h2>
            <p>Comprehensive analysis and recommendations from the AI agent</p>
          </div>
          {error && <div className="output-error">Error: {error}</div>}
          {analysis && (
            <div className="output-content">
              <div className="output-tabs">
                <div className="tab-content">
                  <div className="analysis-card">
                    <h3 className="card-title">🎡 Key Insights</h3>
                    <div className="card-body">
                      <div className="metric-item">
                        <span className="metric-label">Budget Range:</span>
                        <span className="metric-value">{analysis.bant?.budget || 'N/A'}</span>
                      </div>
                      <div className="metric-item">
                        <span className="metric-label">Authority:</span>
                        <span className="metric-value">{analysis.bant?.authority || 'N/A'}</span>
                      </div>
                      <div className="metric-item">
                        <span className="metric-label">Need:</span>
                        <span className="metric-value">{analysis.bant?.need || 'N/A'}</span>
                      </div>
                      <div className="metric-item">
                        <span className="metric-label">Timeline:</span>
                        <span className="metric-value">{analysis.bant?.timeline || 'N/A'}</span>
                      </div>
                    </div>
                  </div>
                  <div className="analysis-card">
                    <h3 className="card-title">🎯 Fit Score & Priority</h3>
                    <div className="card-body">
                      <div className="score-container">
                        <div className="score-bar">
                          <div className="score-fill" style={{ width: `${analysis.score || 0}%` }}></div>
                        </div>
                        <div className="score-text">{analysis.score || 0}% Fit Score</div>
                      </div>
                      <div className="metric-item priority">
                        <span className="metric-label">Priority:</span>
                        <span className={`metric-value priority-${analysis.priority?.toLowerCase() || 'medium'}`}>
                          {analysis.priority || 'Medium'}
                        </span>
                      </div>
                      <div className="metric-item">
                        <span className="metric-label">Segment:</span>
                        <span className="metric-value">{analysis.segment || 'N/A'}</span>
                      </div>
                    </div>
                  </div>
                  <div className="analysis-card">
                    <h3 className="card-title">🚀 Suggested Outreach</h3>
                    <div className="card-body">
                      <p className="outreach-text">{analysis.outreach || 'No specific outreach strategy available'}</p>
                    </div>
                  </div>
                  <div className="analysis-card">
                    <h3 className="card-title">📄 Routing Recommendations</h3>
                    <div className="card-body">
                      <div className="routing-box">
                        <div className="routing-item">
                          <strong>Route to:</strong> {analysis.priority || 'Sales Team'}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
    </div>
  );
}

export default App;
