import pytest
from backend.utils.citation_utils import extract_relevant_citations

def test_citation_extraction():
    # Use a small sample CSV for testing
    citations = extract_relevant_citations("love", "data/persona_0.csv", max_examples=2)
    assert isinstance(citations, list)
    assert all('line' in c for c in citations)

def test_agent_response_structure():
    from backend.agents import PersonaAgent
    agent = PersonaAgent(0, "Cluster0", "data/persona_0.csv", "cluster0")
    state = {"user_query": "What makes a good friend?"}
    result = agent.generate_response(state)
    assert "cluster0" in result
    assert "response" in result["cluster0"]
    assert "citations" in result["cluster0"]

def test_inter_agent_communication():
    # Simulate a state with collaboration_history and test
    from backend.agents import PersonaAgent
    agent = PersonaAgent(1, "Cluster1", "data/persona_1.csv", "cluster1")
    state = {"user_query": "How do you resolve conflict?", "collaboration_history": [{"agent": "cluster0", "response": "By talking it out."}]}
    result = agent.generate_response(state)
    assert "cluster1" in result
    assert "response" in result["cluster1"]
    assert "citations" in result["cluster1"]
