const AGENTIC_API_KEY = import.meta.env.VITE_AGENTIC_API_KEY;
const API_BASE_URL = 'https://api.agentic.ai/v1'; // Replace with the actual API base URL

const callAgenticAPI = async (endpoint, data) => {
  const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${AGENTIC_API_KEY}`
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    throw new Error(`API call to ${endpoint} failed with status ${response.status}`);
  }

  return response.json();
};

export const analyzeLead = async (formData) => {
  // Replace with the actual endpoints and expected data structures
  const [scoreResponse, bantResponse, outreachResponse, routingResponse] = await Promise.all([
    callAgenticAPI('lead-scoring', { lead: formData }),
    callAgenticAPI('bant-qualification', { lead: formData }),
    callAgenticAPI('outreach-generation', { lead: formData }),
    callAgenticAPI('lead-routing', { lead: formData })
  ]);

  return {
    score: scoreResponse.score, // Adjust based on the actual API response
    fitLabel: scoreResponse.fitLabel,
    bant: bantResponse,
    outreach: outreachResponse.subject,
    priority: routingResponse.priority,
    segment: routingResponse.segment
  };
};