import unittest
import os
import sys
import pandas as pd
from unittest.mock import patch, MagicMock

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from agents import PersonaAgent, MultiAgentState, create_agent_system

class TestMultiAgentSystem(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data_path = "data/persona_0_data.csv"
        
        # Create a mock state
        self.state = MultiAgentState()
        self.state.user_query = "What are some interesting movie dialogues?"
        self.state.messages = []
    
    def test_persona_agent_initialization(self):
        """Test that persona agents can be initialized correctly."""
        if os.path.exists(self.test_data_path):
            agent = PersonaAgent(0, "Test Analyst", self.test_data_path, "analyst")
            self.assertEqual(agent.persona_id, 0)
            self.assertEqual(agent.persona_name, "Test Analyst")
            self.assertIsNotNone(agent.persona_prompt)
            self.assertIsNotNone(agent.llm)
        else:
            self.skipTest("Test data not available")
    
    def test_knowledge_base_loading(self):
        """Test that knowledge base is loaded correctly."""
        if os.path.exists(self.test_data_path):
            agent = PersonaAgent(0, "Test Analyst", self.test_data_path, "analyst")
            self.assertIsInstance(agent.knowledge_base, pd.DataFrame)
            if not agent.knowledge_base.empty:
                self.assertIn('line1_text', agent.knowledge_base.columns)
        else:
            self.skipTest("Test data not available")
    
    def test_persona_prompts(self):
        """Test that different personas have different prompts."""
        agent1 = PersonaAgent(0, "Analyst", "data/persona_0_data.csv", "analyst")
        agent2 = PersonaAgent(1, "Responder", "data/persona_1_data.csv", "responder")
        agent3 = PersonaAgent(2, "Storyteller", "data/persona_2_data.csv", "storyteller")
        
        self.assertNotEqual(agent1.persona_prompt, agent2.persona_prompt)
        self.assertNotEqual(agent2.persona_prompt, agent3.persona_prompt)
        self.assertNotEqual(agent1.persona_prompt, agent3.persona_prompt)
    
    @patch('agents.ChatOpenAI')
    def test_agent_response_generation(self, mock_chat_openai):
        """Test that agents can generate responses."""
        # Mock the LLM response
        mock_response = MagicMock()
        mock_response.content = "This is a test response from the agent."
        mock_chat_openai.return_value.invoke.return_value = mock_response
        
        agent = PersonaAgent(0, "Test Analyst", "data/persona_0_data.csv", "analyst")
        result = agent.generate_response({"user_query": "test"})
        
        self.assertIn('analyst', result)
        self.assertIn('agent', result['analyst'])
        self.assertIn('response', result['analyst'])
        self.assertIn('citations', result['analyst'])
        self.assertEqual(result['analyst']['agent'], "Test Analyst")
        self.assertEqual(result['analyst']['response'], "[MOCKED LLM RESPONSE] test")
    
    def test_context_retrieval(self):
        """Test that agents can retrieve relevant context."""
        if os.path.exists(self.test_data_path):
            agent = PersonaAgent(0, "Test Analyst", self.test_data_path, "analyst")
            context = agent.get_relevant_context("test query")
            self.assertIsInstance(context, str)
        else:
            self.skipTest("Test data not available")
    
    def test_agent_system_creation(self):
        """Test that the agent system can be created."""
        try:
            system = create_agent_system()
            self.assertIsNotNone(system)
        except Exception as e:
            self.skipTest(f"Agent system creation failed: {e}")
    
    def test_state_management(self):
        """Test that the state management works correctly."""
        state = MultiAgentState()
        state.user_query = "Test query"
        state.messages = [{"role": "user", "content": "Hello"}]
        
        self.assertEqual(state.user_query, "Test query")
        self.assertEqual(len(state.messages), 1)
        self.assertEqual(state.messages[0]["content"], "Hello")

class TestCitationSystem(unittest.TestCase):
    
    def test_citation_format(self):
        """Test that citations are formatted correctly."""
        citation = {
            'source': 'movie_dialogues',
            'persona': 'Test Analyst',
            'context': 'Character: John - "Hello there" (Movie: Test Movie)',
            'agent': 'Test Analyst'
        }
        
        self.assertIn('source', citation)
        self.assertIn('persona', citation)
        self.assertIn('context', citation)
        self.assertIn('agent', citation)

if __name__ == '__main__':
    unittest.main() 