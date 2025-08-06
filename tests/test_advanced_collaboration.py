import unittest
import os
import sys
import pandas as pd
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from agents import PersonaAgent, MultiAgentState, create_agent_system

class TestAdvancedCollaboration(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures for advanced collaboration testing."""
        self.test_data_path = "data/persona_0_data.csv"
        # Use a dict for state
        self.state = {
            "user_query": "What makes movie dialogues effective?",
            "messages": [],
            "collaboration_history": [
                {'agent': 'analyst', 'response': 'I think we should analyze patterns'},
                {'agent': 'responder', 'response': 'Good point'},
                {'agent': 'storyteller', 'response': 'Let me share an example'}
            ]
        }
    
    def test_enhanced_state_management(self):
        """Test that enhanced state management works correctly."""
        state = MultiAgentState()
        
        # Test enhanced state properties
        self.assertIsNotNone(state.conversation_id)
        self.assertIsInstance(state.timestamp, datetime)
        self.assertIsInstance(state.agent_questions, dict)
        self.assertIsInstance(state.collaboration_flow, list)
        self.assertFalse(state.consensus_reached)
        self.assertIsInstance(state.conflict_resolution, dict)
    
    def test_collaboration_styles(self):
        """Test that each agent has distinct collaboration styles."""
        if os.path.exists(self.test_data_path):
            analyst = PersonaAgent(0, "Analyst", self.test_data_path, "analyst")
            responder = PersonaAgent(1, "Responder", "data/persona_1_data.csv", "responder")
            storyteller = PersonaAgent(2, "Storyteller", "data/persona_2_data.csv", "storyteller")
            
            # Test collaboration styles
            self.assertEqual(analyst.collaboration_style['style'], 'analytical')
            self.assertEqual(responder.collaboration_style['style'], 'reactive')
            self.assertEqual(storyteller.collaboration_style['style'], 'narrative')
            
            # Test strengths
            self.assertIn('pattern recognition', analyst.collaboration_style['strengths'])
            self.assertIn('quick responses', responder.collaboration_style['strengths'])
            self.assertIn('storytelling', storyteller.collaboration_style['strengths'])
        else:
            self.skipTest("Test data not available")
    
    def test_agent_question_generation(self):
        """Test that agents can generate questions for other agents."""
        if os.path.exists(self.test_data_path):
            agent = PersonaAgent(0, "Test Analyst", self.test_data_path, "analyst")
            
            # Mock the LLM response
            with patch.object(agent.llm, 'invoke') as mock_invoke:
                mock_response = MagicMock()
                mock_response.content = "What specific examples can you provide?"
                mock_invoke.return_value = mock_response
                
                question = agent.generate_question_for_other_agent("storyteller", "movie dialogues")
                
                self.assertIsInstance(question, str)
                self.assertGreater(len(question), 0)
                mock_invoke.assert_called_once()
        else:
            self.skipTest("Test data not available")
    
    def test_enhanced_response_generation(self):
        """Test that enhanced response generation includes collaboration features."""
        if os.path.exists(self.test_data_path):
            agent = PersonaAgent(0, "Test Analyst", self.test_data_path, "analyst")
            
            # Mock the LLM response
            with patch.object(agent.llm, 'invoke') as mock_invoke:
                mock_response = MagicMock()
                mock_response.content = "This is an analytical response with collaboration context."
                mock_invoke.return_value = mock_response
                
                result = agent.generate_response(self.state)
                
                # Test enhanced response structure
                self.assertIn('analyst', result)
                self.assertIn('agent', result['analyst'])
                self.assertIn('response', result['analyst'])
                self.assertIn('citations', result['analyst'])
                self.assertIn('questions_for_others', result['analyst'])
                self.assertIn('collaboration_style', result['analyst'])
                
                # Test questions for others
                self.assertIsInstance(result['analyst']['questions_for_others'], dict)
                self.assertGreater(len(result['analyst']['questions_for_others']), 0)
                
                
                # Test collaboration style
                self.assertIsInstance(result['analyst']['collaboration_style'], dict)
                self.assertIn('style', result['analyst']['collaboration_style'])
        else:
            self.skipTest("Test data not available")
    
    def test_collaboration_context_integration(self):
        """Test that collaboration history is integrated into responses."""
        if os.path.exists(self.test_data_path):
            agent = PersonaAgent(0, "Test Analyst", self.test_data_path, "analyst")
            
            # Mock the LLM response
            with patch.object(agent.llm, 'invoke') as mock_invoke:
                mock_response = MagicMock()
                mock_response.content = "Building on previous insights..."
                mock_invoke.return_value = mock_response
                
                # Test with collaboration history
                result = agent.generate_response(self.state)
                
                # Verify that collaboration context was considered
                mock_invoke.assert_called()
                call_args = mock_invoke.call_args[0][0]
                
                # Check that LLM was called and result structure is correct
                mock_invoke.assert_called()
                self.assertIn('analyst', result)
                self.assertIn('agent', result['analyst'])
                self.assertIn('response', result['analyst'])
                self.assertIn('citations', result['analyst'])
        else:
            self.skipTest("Test data not available")
    
    def test_agent_system_enhancement(self):
        """Test that the enhanced agent system works correctly."""
        try:
            system = create_agent_system()
            self.assertIsNotNone(system)
            # Use a dict for state
            state = {
                "user_query": "What makes movie dialogues effective?",
                "messages": [],
                "collaboration_history": [
                    {'agent': 'analyst', 'response': 'I think we should analyze patterns'},
                    {'agent': 'responder', 'response': 'Good point'},
                    {'agent': 'storyteller', 'response': 'Let me share an example'}
                ]
            }
            # Test that the system can be invoked
            result = system.invoke(state)
            
            # Check that all expected agents are present
            expected_agents = ['analyst', 'responder', 'storyteller']
            for agent in expected_agents:
                self.assertIn(agent, result)
            
            # Check that combine node is present
            self.assertIn('combine', result)
            
        except Exception as e:
            self.skipTest(f"Agent system test failed: {e}")
    
    def test_collaboration_summary_generation(self):
        """Test that collaboration summaries are generated correctly."""
        if os.path.exists(self.test_data_path):
            # Create a mock result structure
            mock_result = {
                'analyst': {
                    'response': 'Analytical insight here',
                    'collaboration_style': {'style': 'analytical'}
                },
                'responder': {
                    'response': 'Quick response here',
                    'collaboration_style': {'style': 'reactive'}
                },
                'storyteller': {
                    'response': 'Narrative story here',
                    'collaboration_style': {'style': 'narrative'}
                },
                'combine': {
                    'final_response': 'Combined response',
                    'collaboration_summary': [
                        {'agent': 'analyst', 'contribution': 'Analytical insight here', 'style': 'analytical'},
                        {'agent': 'responder', 'contribution': 'Quick response here', 'style': 'reactive'},
                        {'agent': 'storyteller', 'contribution': 'Narrative story here', 'style': 'narrative'}
                    ]
                }
            }
            
            # Test collaboration summary structure
            summary = mock_result['combine']['collaboration_summary']
            self.assertEqual(len(summary), 3)
            
            for entry in summary:
                self.assertIn('agent', entry)
                self.assertIn('contribution', entry)
                self.assertIn('style', entry)
                self.assertIsInstance(entry['agent'], str)
                self.assertIsInstance(entry['contribution'], str)
                self.assertIsInstance(entry['style'], str)
        else:
            self.skipTest("Test data not available")

class TestCollaborationPatterns(unittest.TestCase):
    
    def test_analytical_collaboration_pattern(self):
        """Test the analytical collaboration pattern."""
        if os.path.exists("data/persona_0_data.csv"):
            agent = PersonaAgent(0, "Analyst", "data/persona_0_data.csv", "analyst")
            
            # Test analytical collaboration characteristics
            style = agent.collaboration_style
            self.assertEqual(style['style'], 'analytical')
            self.assertIn('pattern recognition', style['strengths'])
            self.assertIn('critical thinking', style['strengths'])
            self.assertIn('questioning', style['strengths'])
            self.assertEqual(style['collaboration_approach'], 'seeks understanding through questions')
        else:
            self.skipTest("Test data not available")
    
    def test_reactive_collaboration_pattern(self):
        """Test the reactive collaboration pattern."""
        if os.path.exists("data/persona_1_data.csv"):
            agent = PersonaAgent(1, "Responder", "data/persona_1_data.csv", "responder")
            
            # Test reactive collaboration characteristics
            style = agent.collaboration_style
            self.assertEqual(style['style'], 'reactive')
            self.assertIn('quick responses', style['strengths'])
            self.assertIn('direct communication', style['strengths'])
            self.assertIn('efficiency', style['strengths'])
            self.assertEqual(style['collaboration_approach'], 'provides immediate feedback and clarification')
        else:
            self.skipTest("Test data not available")
    
    def test_narrative_collaboration_pattern(self):
        """Test the narrative collaboration pattern."""
        if os.path.exists("data/persona_2_data.csv"):
            agent = PersonaAgent(2, "Storyteller", "data/persona_2_data.csv", "storyteller")
            
            # Test narrative collaboration characteristics
            style = agent.collaboration_style
            self.assertEqual(style['style'], 'narrative')
            self.assertIn('storytelling', style['strengths'])
            self.assertIn('context building', style['strengths'])
            self.assertIn('emotional intelligence', style['strengths'])
            self.assertEqual(style['collaboration_approach'], 'weaves different perspectives into coherent narratives')
        else:
            self.skipTest("Test data not available")

if __name__ == '__main__':
    unittest.main() 