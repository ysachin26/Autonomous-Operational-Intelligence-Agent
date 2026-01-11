import { BarChart, CheckSquare, Star, Mail, TrendingUp, Users } from 'lucide-react';

const AIAnalysisPanel = ({ results }) => {
  if (!results) return null;

  return (
    <div className="ai-analysis-panel card">
      <h3><BarChart size={20} /> AI Analysis</h3>
      <div className="analysis-grid">
        <div className="analysis-item">
          <h4><Star size={18} /> Lead Score & Fit</h4>
          <p className="score">{results.score} / 100</p>
          <p className="fit-label">{results.fitLabel}</p>
        </div>
        <div className="analysis-item">
          <h4><CheckSquare size={18} /> BANT Analysis</h4>
          <ul>
            {Object.entries(results.bant).map(([key, value]) => (
              <li key={key}><strong>{key}:</strong> {value}</li>
            ))}
          </ul>
        </div>
        <div className="analysis-item">
          <h4><Mail size={18} /> Suggested Outreach</h4>
          <p>{results.outreach}</p>
        </div>
        <div className="analysis-item">
          <h4><TrendingUp size={18} /> Priority</h4>
          <p>{results.priority}</p>
        </div>
        <div className="analysis-item">
          <h4><Users size={18} /> Segment</h4>
          <p>{results.segment}</p>
        </div>
      </div>
    </div>
  );
};

export default AIAnalysisPanel;