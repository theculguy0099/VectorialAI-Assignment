from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
from agents import agent_system, MultiAgentState
import json
from datetime import datetime
import logging
import traceback

app = FastAPI(title="Multi-Agent Conversational AI", version="2.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    collaboration_mode: Optional[str] = "enhanced"  # enhanced, basic, interactive

class ChatResponse(BaseModel):
    response: str
    agent_responses: Dict[str, str]
    citations: List[Dict[str, Any]]
    conversation_id: str
    collaboration_summary: List[Dict[str, Any]]
    agent_questions: Dict[str, Dict[str, str]]
    collaboration_flow: List[Dict[str, Any]]
    shared_memory: Optional[Dict[str, Any]] = None
    moderator: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class AgentInfo(BaseModel):
    name: str
    persona: str
    description: str
    collaboration_style: Dict[str, Any]
    strengths: List[str]

class CollaborationScenario(BaseModel):
    name: str
    description: str
    query: str
    expected_collaboration: str

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    return HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")

@app.get("/")
async def root():
    return {
        "message": "Multi-Agent Conversational AI System v2.0",
        "features": [
            "Advanced agent collaboration",
            "Agent-to-agent questioning",
            "Collaboration style tracking",
            "Enhanced citation system",
            "Real-time collaboration flow"
        ]
    }

@app.get("/agents", response_model=List[AgentInfo])
async def get_agents():
    agents = [
        AgentInfo(
            name="Inquisitive Analyst",
            persona="analyst",
            description="Drives conversations by asking direct questions, making observations, and planning. Engaging and analytical.",
            collaboration_style={
                "style": "analytical",
                "approach": "seeks understanding through questions",
                "conflict_handling": "analyzes and proposes solutions"
            },
            strengths=["pattern recognition", "critical thinking", "questioning"]
        ),
        AgentInfo(
            name="Concise Responder", 
            persona="responder",
            description="Characterized by short, reactive, and to-the-point statements. Often responds with brief questions or affirmations.",
            collaboration_style={
                "style": "reactive",
                "approach": "provides immediate feedback and clarification",
                "conflict_handling": "seeks quick resolution"
            },
            strengths=["quick responses", "direct communication", "efficiency"]
        ),
        AgentInfo(
            name="Narrative Storyteller",
            persona="storyteller", 
            description="More descriptive and expressive, sometimes telling stories or giving opinions with more detail.",
            collaboration_style={
                "style": "narrative",
                "approach": "weaves different perspectives into coherent narratives",
                "conflict_handling": "seeks common ground through storytelling"
            },
            strengths=["storytelling", "context building", "emotional intelligence"]
        )
    ]
    return agents

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if not request.message or not request.message.strip():
            logger.warning("Received empty user message.")
            raise HTTPException(status_code=400, detail="Message cannot be empty.")
        state = {
            "user_query": request.message,
            "messages": [],
            "shared_memory": {},
        }
        try:
            result = agent_system.invoke(state)
        except Exception as agent_exc:
            logger.error(f"Agent system error: {agent_exc}\n{traceback.format_exc()}")
            return ChatResponse(
                response="",
                agent_responses={},
                citations=[],
                conversation_id=request.conversation_id or "default",
                collaboration_summary=[],
                agent_questions={},
                collaboration_flow=[],
                shared_memory={},
                moderator=None,
                error="Agent system failed to process the request. Please try again later."
            )
        agent_responses = {}
        citations = []
        agent_questions = {}
        collaboration_flow = []
        shared_memory = result.get('combine', {}).get('shared_memory', {})
        moderator = result.get('moderator', None)
        # Guarantee each agent has a response, even if missing from result
        for agent_name in ['analyst', 'responder', 'storyteller']:
            agent_result = result.get(agent_name, {})
            agent_responses[agent_name] = agent_result.get('response', '[MOCKED LLM RESPONSE]')
            agent_questions[agent_name] = agent_result.get('questions_for_others', {})
            if 'citations' in agent_result:
                citations.extend(agent_result['citations'])
            collaboration_flow.append({
                'agent': agent_name,
                'response': agent_result.get('response', '[MOCKED LLM RESPONSE]'),
                'style': agent_result.get('collaboration_style', {}).get('style', 'general'),
                'timestamp': datetime.now().isoformat()
            })
        final_response = result.get('combine', {}).get('final_response', '[MOCKED LLM RESPONSE]')
        collaboration_summary = result.get('combine', {}).get('collaboration_summary', [])
        return ChatResponse(
            response=final_response,
            agent_responses=agent_responses,
            citations=citations,
            conversation_id=request.conversation_id or "default",
            collaboration_summary=collaboration_summary,
            agent_questions=agent_questions,
            collaboration_flow=collaboration_flow,
            shared_memory=shared_memory,
            moderator=moderator
        )
        
    except HTTPException as http_exc:
        logger.warning(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unhandled error in /chat: {e}\n{traceback.format_exc()}")
        return ChatResponse(
            response="",
            agent_responses={},
            citations=[],
            conversation_id=request.conversation_id or "default",
            collaboration_summary=[],
            agent_questions={},
            collaboration_flow=[],
            error="An unexpected error occurred. Please try again later."
        )

@app.get("/collaboration-scenarios", response_model=List[CollaborationScenario])
async def get_collaboration_scenarios():
    scenarios = [
        CollaborationScenario(
            name="Dialogue Analysis",
            description="Analyze what makes movie dialogues effective",
            query="What makes a good movie dialogue?",
            expected_collaboration="Analyst will ask probing questions, Responder will provide quick insights, Storyteller will share detailed examples"
        ),
        CollaborationScenario(
            name="Emotional Expression",
            description="Understand how characters express emotions in movies",
            query="How do characters express emotions in movies?",
            expected_collaboration="Analyst will analyze patterns, Responder will highlight key moments, Storyteller will provide rich context"
        ),
        CollaborationScenario(
            name="Conversation Patterns",
            description="Identify recurring dialogue structures",
            query="What are some common conversation patterns in films?",
            expected_collaboration="Analyst will map structures, Responder will identify turning points, Storyteller will explain narrative arcs"
        ),
        CollaborationScenario(
            name="Character Development",
            description="Explore how characters evolve through dialogue",
            query="How do movie characters develop through their conversations?",
            expected_collaboration="Analyst will track development patterns, Responder will note key changes, Storyteller will weave character stories"
        )
    ]
    return scenarios

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents": ["analyst", "responder", "storyteller"],
        "features": [
            "advanced_collaboration",
            "agent_questioning",
            "collaboration_tracking",
            "citation_system"
        ],
        "version": "2.0.0"
    }

@app.get("/collaboration-stats")
async def get_collaboration_stats():
    return {
        "total_conversations": 0,  # Would be tracked in a real implementation
        "collaboration_patterns": {
            "analytical_lead": "Analyst initiates with questions",
            "reactive_support": "Responder provides quick feedback",
            "narrative_synthesis": "Storyteller weaves perspectives together"
        },
        "agent_interactions": {
            "analyst_questions": "High frequency of questions to other agents",
            "responder_acknowledgments": "Quick acknowledgments and clarifications",
            "storyteller_connections": "Rich narrative connections between perspectives"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 