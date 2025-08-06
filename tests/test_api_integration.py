import unittest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from api import app

client = TestClient(app)

class TestAPIIntegration(unittest.TestCase):
    def test_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Multi-Agent Conversational AI System", response.json()["message"])

    def test_agents(self):
        response = client.get("/agents")
        self.assertEqual(response.status_code, 200)
        agents = response.json()
        self.assertTrue(isinstance(agents, list))
        self.assertGreaterEqual(len(agents), 3)
        self.assertIn("persona", agents[0])

    def test_collaboration_scenarios(self):
        response = client.get("/collaboration-scenarios")
        self.assertEqual(response.status_code, 200)
        scenarios = response.json()
        self.assertTrue(isinstance(scenarios, list))
        self.assertGreaterEqual(len(scenarios), 1)
        self.assertIn("query", scenarios[0])

    def test_health(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        health = response.json()
        self.assertEqual(health["status"], "healthy")
        self.assertIn("analyst", health["agents"])

    def test_collaboration_stats(self):
        response = client.get("/collaboration-stats")
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertIn("collaboration_patterns", stats)

    def test_chat_success(self):
        response = client.post("/chat", json={"message": "What makes a good movie dialogue?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("agent_responses", data)
        self.assertIn("citations", data)
        self.assertIn("collaboration_summary", data)
        self.assertIn("agent_questions", data)
        self.assertIn("collaboration_flow", data)
        self.assertIsNone(data.get("error"))

    def test_chat_empty_message(self):
        response = client.post("/chat", json={"message": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_chat_missing_message(self):
        response = client.post("/chat", json={})
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

    def test_chat_agent_failure(self):
        # Simulate agent failure by monkeypatching agent_system.invoke
        from api import agent_system
        orig_invoke = agent_system.invoke
        agent_system.invoke = lambda state: (_ for _ in ()).throw(Exception("Simulated agent failure"))
        response = client.post("/chat", json={"message": "Test agent failure"})
        agent_system.invoke = orig_invoke
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("error", data)
        self.assertIn("Agent system failed", data["error"])

if __name__ == "__main__":
    unittest.main()