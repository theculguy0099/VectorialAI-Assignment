import os
import json
from typing import Dict, List, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import pandas as pd
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()

MOCK_LLM = os.getenv("MOCK_LLM", "false").lower() == "true"

class MockLLM:
    def invoke(self, messages):
        # Return a simple mock response based on the last user message
        user_msg = ""
        for m in reversed(messages):
            if hasattr(m, "content"):
                user_msg = m.content
                break
        class MockResponse:
            content = f"[MOCKED LLM RESPONSE] {user_msg[:60]}"
        return MockResponse()

class MultiAgentState:
    """Enhanced state management for multi-agent conversations."""
    def __init__(self):
        self.messages: List[Dict] = []
        self.agent_responses: Dict[str, List[str]] = {}
        self.citations: Dict[str, List[Dict]] = {}
        self.collaboration_history: List[Dict] = []
        self.current_agent: Optional[str] = None
        self.user_query: Optional[str] = None
        self.conversation_id: str = str(uuid.uuid4())
        self.timestamp: datetime = datetime.now()
        self.agent_questions: Dict[str, List[str]] = {}  # Questions agents ask each other
        self.collaboration_flow: List[Dict] = []  # Track collaboration steps
        self.consensus_reached: bool = False
        self.conflict_resolution: Dict[str, Any] = {}

class PersonaAgent:
    """Enhanced persona-specific agents with advanced collaboration capabilities."""
    
    def __init__(self, persona_id: int, persona_name: str, data_path: str, node_name: str):
        self.persona_id = persona_id
        self.persona_name = persona_name
        self.data_path = data_path
        self.node_name = node_name  # Add node_name for routing and keying
        self.knowledge_base = self._load_knowledge_base()
        if MOCK_LLM:
            self.llm = MockLLM()
        else:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        self.persona_prompt = self._get_persona_prompt()
        self.collaboration_style = self._get_collaboration_style()
    
    def _load_knowledge_base(self) -> pd.DataFrame:
        """Load the persona-specific knowledge base."""
        if os.path.exists(self.data_path):
            return pd.read_csv(self.data_path)
        else:
            print(f"Warning: Knowledge base not found at {self.data_path}")
            return pd.DataFrame()
    
    def _get_persona_prompt(self) -> str:
        """Get the persona-specific system prompt."""
        prompts = {
            0: """You are the Inquisitive Analyst. You drive conversations by asking direct questions, making observations, and planning. You are engaging and analytical. You have access to dialogue data from movies where characters exhibit inquisitive, analytical behavior.

Your responses should:
- Ask clarifying questions when needed
- Make analytical observations
- Plan and organize thoughts
- Be engaging and curious
- Always cite specific movie dialogues that inform your responses
- When collaborating, ask other agents specific questions to understand their perspective
- Challenge assumptions and seek deeper understanding

When collaborating with other agents, ask them questions to understand their perspective and build upon their insights.""",
            
            1: """You are the Concise Responder. You are characterized by short, reactive, and to-the-point statements. You often respond with brief questions or affirmations. You have access to dialogue data from movies where characters exhibit concise, reactive behavior.

Your responses should:
- Be brief and to the point
- React quickly to others' statements
- Ask short, direct questions
- Provide concise affirmations or clarifications
- Always cite specific movie dialogues that inform your responses
- When collaborating, provide quick, focused responses that help move the conversation forward
- Acknowledge other agents' contributions briefly but effectively

When collaborating with other agents, provide quick, focused responses that help move the conversation forward.""",
            
            2: """You are the Narrative Storyteller. You tend to be more descriptive and expressive, sometimes telling stories or giving opinions with more detail. You have access to dialogue data from movies where characters exhibit narrative, expressive behavior.

Your responses should:
- Be descriptive and expressive
- Share stories and detailed opinions
- Provide rich context and background
- Be more verbose and engaging
- Always cite specific movie dialogues that inform your responses
- When collaborating, provide detailed insights and help build rich narratives
- Connect different perspectives into coherent stories

When collaborating with other agents, provide detailed insights and help build rich narratives around the discussion."""
        }
        return prompts.get(self.persona_id, "You are a helpful AI assistant.")
    
    def _get_collaboration_style(self) -> Dict[str, Any]:
        """Get the agent's collaboration style and preferences."""
        styles = {
            0: {
                "style": "analytical",
                "strengths": ["pattern recognition", "critical thinking", "questioning"],
                "collaboration_approach": "seeks understanding through questions",
                "preferred_partners": ["storyteller", "responder"],
                "conflict_handling": "analyzes and proposes solutions"
            },
            1: {
                "style": "reactive",
                "strengths": ["quick responses", "direct communication", "efficiency"],
                "collaboration_approach": "provides immediate feedback and clarification",
                "preferred_partners": ["analyst", "storyteller"],
                "conflict_handling": "seeks quick resolution"
            },
            2: {
                "style": "narrative",
                "strengths": ["storytelling", "context building", "emotional intelligence"],
                "collaboration_approach": "weaves different perspectives into coherent narratives",
                "preferred_partners": ["analyst", "responder"],
                "conflict_handling": "seeks common ground through storytelling"
            }
        }
        return styles.get(self.persona_id, {})
    
    def get_relevant_context(self, query: str, max_examples: int = 3) -> str:
        """Get relevant context from the agent's knowledge base."""
        if self.knowledge_base.empty:
            return "No specific knowledge available for this persona."
        
        # Enhanced keyword matching with semantic similarity
        query_lower = query.lower()
        relevant_examples = []
        
        for _, row in self.knowledge_base.iterrows():
            text = str(row.get('line1_text', '')).lower()
            if any(word in text for word in query_lower.split()):
                example = f"Character: {row.get('char1_name', 'Unknown')} - \"{row.get('line1_text', '')}\" (Movie: {row.get('movie_title', 'Unknown')})"
                relevant_examples.append(example)
                if len(relevant_examples) >= max_examples:
                    break
        
        if relevant_examples:
            return "\n".join(relevant_examples)
        else:
            # Return random examples if no direct matches
            sample = self.knowledge_base.sample(min(max_examples, len(self.knowledge_base)))
            examples = []
            for _, row in sample.iterrows():
                example = f"Character: {row.get('char1_name', 'Unknown')} - \"{row.get('line1_text', '')}\" (Movie: {row.get('movie_title', 'Unknown')})"
                examples.append(example)
            return "\n".join(examples)
    
    def generate_question_for_other_agent(self, other_agent_name: str, context: str) -> str:
        """Generate a question to ask another agent based on collaboration style."""
        question_prompts = {
            "analyst": f"As the Inquisitive Analyst, what specific question would you ask the {other_agent_name} to better understand their perspective on: {context}?",
            "responder": f"As the Concise Responder, what brief, direct question would you ask the {other_agent_name} about: {context}?",
            "storyteller": f"As the Narrative Storyteller, what question would you ask the {other_agent_name} to help build a richer story around: {context}?"
        }
        
        style = self.collaboration_style.get("style", "general")
        prompt = question_prompts.get(style, f"What question would you ask the {other_agent_name} about: {context}?")
        
        messages = [
            SystemMessage(content=self.persona_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def generate_response(self, state: dict) -> dict:
        """Generate a response based on the current state and agent's persona. Returns a dict for LangGraph."""
        # Get relevant context from knowledge base
        context = self.get_relevant_context(state.get("user_query", ""))
        # Build messages for the LLM
        messages = [
            SystemMessage(content=self.persona_prompt),
            SystemMessage(content=f"Relevant dialogue examples from your knowledge base:\n{context}"),
        ]
        # Add collaboration context if available
        if state.get("collaboration_history"):
            collaboration_context = "\n".join([f"{item['agent']}: {item['response']}" for item in state["collaboration_history"][-3:]])
            messages.append(SystemMessage(content=f"Recent collaboration context:\n{collaboration_context}"))
        # Add conversation history
        for msg in state.get("messages", [])[-5:]:  # Last 5 messages for context
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
        # Add current user query
        if state.get("user_query"):
            messages.append(HumanMessage(content=state["user_query"]))
        # Generate response
        response = self.llm.invoke(messages)
        # Generate questions for other agents
        other_agents = ['analyst', 'responder', 'storyteller']
        if self.node_name in other_agents:
            other_agents.remove(self.node_name)
        questions_for_others = {}
        for other_agent in other_agents:
            question = self.generate_question_for_other_agent(other_agent, state.get("user_query", ""))
            questions_for_others[other_agent] = question
        # Extract citations from context
        citations = []
        if context and context != "No specific knowledge available for this persona.":
            citations.append({
                'source': 'movie_dialogues',
                'persona': self.persona_name,
                'context': context,
                'agent': self.persona_name
            })
        # Collaborative memory logic
        shared_memory = state.get('shared_memory', {})
        memory_updates = {}
        # Example: Each agent writes a key to shared_memory with attribution
        memory_key = f"{self.node_name}_insight"
        memory_value = {
            'agent': self.persona_name,
            'content': response.content,
            'timestamp': str(pd.Timestamp.now())
        }
        memory_updates[memory_key] = memory_value
        # Return agent update and memory update
        return {
            self.node_name: {
                'agent': self.persona_name,
                'response': response.content,
                'citations': citations,
                'persona_id': self.persona_id,
                'questions_for_others': questions_for_others,
                'collaboration_style': self.collaboration_style
            },
            'shared_memory': {**shared_memory, **memory_updates}
        }

# Moderator agent
class ModeratorAgent:
    def __init__(self):
        self.name = "Moderator"
        self.prompt = (
            "You are the Moderator. Your job is to review all agent responses and the shared memory, "
            "summarize the main points, highlight consensus or disagreement, and resolve conflicts if any. "
            "Cite memory and agent contributions as needed."
        )
        self.llm = MockLLM() if MOCK_LLM else ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    def moderate(self, state: dict) -> dict:
        # Gather all agent responses
        agent_summaries = []
        for agent_key in ['analyst', 'responder', 'storyteller']:
            if agent_key in state:
                agent = state[agent_key]
                agent_summaries.append(f"{agent['agent']}: {agent['response']}")
        # Gather shared memory
        memory = state.get('shared_memory', {})
        memory_summary = "\n".join([f"{k}: {v['content']} (by {v['agent']})" for k, v in memory.items()])
        # Build LLM prompt
        messages = [
            SystemMessage(content=self.prompt),
            SystemMessage(content=f"Agent responses:\n{chr(10).join(agent_summaries)}"),
            SystemMessage(content=f"Shared memory:\n{memory_summary}")
        ]
        response = self.llm.invoke(messages)
        return {
            'moderator': {
                'summary': response.content,
                'memory_used': memory,
                'agents_reviewed': agent_summaries
            }
        }

StateType = Dict[
    str,
    Dict[str, Any]
]

def create_agent_system() -> StateGraph:
    """Create the enhanced multi-agent system using LangGraph."""
    
    # Initialize agents with node_name
    agents = {
        'analyst': PersonaAgent(0, "Inquisitive Analyst", "data/persona_0_data.csv", "analyst"),
        'responder': PersonaAgent(1, "Concise Responder", "data/persona_1_data.csv", "responder"),
        'storyteller': PersonaAgent(2, "Narrative Storyteller", "data/persona_2_data.csv", "storyteller")
    }
    
    # Create the state graph (no channels needed for sequential)
    moderator = ModeratorAgent()
    workflow = StateGraph(dict)
    
    # Add nodes for each agent
    for agent_name, agent in agents.items():
        workflow.add_node(agent_name, agent.generate_response)
    
    # Sequential routing logic
    def start_node(state: dict) -> dict:
        return {**state, "__next__": "analyst"}
    
    # Combine node unchanged
    def combine_responses(state: dict) -> dict:
        combined_response = "Collaborative Response:\n\n"
        all_citations = []
        collaboration_summary = []
        for agent_name in agents.keys():
            agent_key = agent_name
            if agent_key in state:
                agent_result = state[agent_key]
                combined_response += f"**{agent_name.title()}**: {agent_result.get('response', '')}\n\n"
                if 'citations' in agent_result:
                    all_citations.extend(agent_result['citations'])
                collaboration_summary.append({
                    'agent': agent_name,
                    'contribution': agent_result.get('response', ''),
                    'style': agent_result.get('collaboration_style', {}).get('style', 'general')
                })
        # Add shared memory summary
        memory = state.get('shared_memory', {})
        if memory:
            combined_response += "\n---\nShared Memory:\n"
            for k, v in memory.items():
                combined_response += f"- {k}: {v['content']} (by {v['agent']})\n"
        combined_response += "\n---\nCollaboration Insights:\n"
        for summary in collaboration_summary:
            combined_response += f"- {summary['agent'].title()} ({summary['style']}): Provided {summary['contribution'][:50]}...\n"
        combined_response += "\n---\nCitations:\n"
        for citation in all_citations:
            combined_response += f"- {citation['agent']}: {citation['context'][:100]}...\n"
        return {
            "combine": {
                'final_response': combined_response,
                'all_citations': all_citations,
                'collaboration_summary': collaboration_summary,
                'shared_memory': memory
            }
        }
    
    # Add the nodes
    workflow.add_node("route", start_node)
    workflow.add_node("combine", combine_responses)
    workflow.add_node("moderator", moderator.moderate)
    
    # Set up the graph edges for sequential execution
    workflow.set_entry_point("route")
    workflow.add_edge("route", "analyst")
    workflow.add_edge("analyst", "responder")
    workflow.add_edge("responder", "storyteller")
    workflow.add_edge("storyteller", "combine")
    workflow.add_edge("combine", "moderator")
    workflow.add_edge("moderator", END)
    
    return workflow.compile()

# Create the agent system instance
agent_system = create_agent_system() 