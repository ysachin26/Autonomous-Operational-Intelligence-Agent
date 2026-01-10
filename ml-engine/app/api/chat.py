"""
AOIA ML Engine - Chat & Reasoning API
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.agents.reasoning_agent import ReasoningAgent

router = APIRouter()
agent = ReasoningAgent()


class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None
    suggested_actions: Optional[List[str]] = None


class ExplainRequest(BaseModel):
    entity_type: str  # "anomaly" or "incident"
    entity: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None


class ExplainResponse(BaseModel):
    explanation: str
    key_findings: List[str]
    root_cause: Optional[str]
    confidence: float


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the AOIA reasoning agent.
    Handles natural language queries about operations.
    """
    result = agent.chat(
        message=request.message,
        context=request.context,
        session_id=request.session_id,
    )
    
    return ChatResponse(**result)


@router.post("/explain", response_model=ExplainResponse)
async def explain(request: ExplainRequest):
    """
    Get an AI-generated explanation for an anomaly or incident.
    """
    result = agent.explain(
        entity_type=request.entity_type,
        entity=request.entity,
        context=request.context,
    )
    
    return ExplainResponse(**result)


@router.post("/summarize")
async def summarize(
    data: Dict[str, Any],
    summary_type: str = "daily",
):
    """
    Generate a natural language summary of operational data.
    """
    summary = agent.summarize(data, summary_type)
    
    return {
        "summary": summary,
        "type": summary_type,
        "generated_at": agent.get_timestamp(),
    }


@router.post("/query")
async def query(
    question: str,
    data_context: Optional[Dict[str, Any]] = None,
):
    """
    Answer a specific question about operations using AI.
    """
    answer = agent.answer_question(question, data_context)
    
    return {
        "question": question,
        "answer": answer["answer"],
        "confidence": answer["confidence"],
        "data_sources": answer.get("data_sources", []),
    }
