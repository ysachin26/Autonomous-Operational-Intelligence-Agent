import { useState } from 'react';
import { Bot, PlayCircle } from 'lucide-react';
import { analyzeLead } from '../agentic-service'; 

const AgentIntegration = ({ companyData }) => {
  const [agentResults, setAgentResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runAgents = async () => {
    setLoading(true);
    setError(null);
    try {
      const results = await analyzeLead(companyData);
      setAgentResults(results);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="agent-integration card">
      <h3><Bot size={20} /> AI Agent Console</h3>
      <p>Run individual AI agents to get specific insights.</p>
      
      <button onClick={runAgents} disabled={loading} className="run-agent-btn">
        <PlayCircle size={18} />
        {loading ? 'Running Agents...' : 'Run All Agents'}
      </button>

      {error && <div className="error-message">Error: {error}</div>}

      {agentResults && (
        <div className="agent-results">
          <h4>Agent Results:</h4>
          <pre>{JSON.stringify(agentResults, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default AgentIntegration;