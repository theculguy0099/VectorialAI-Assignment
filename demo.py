#!/usr/bin/env python3
"""
Demo script for the Multi-Agent Conversational AI system.
This script demonstrates the collaborative capabilities of the agents.
"""

import os
import sys
import time
from pathlib import Path

# Add backend to path
sys.path.append('backend')

from agents import create_agent_system, MultiAgentState

def print_separator(title=""):
    """Print a formatted separator."""
    if title:
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")

def demo_agent_collaboration():
    """Demonstrate agent collaboration with example queries."""
    
    print_separator("🤖 Multi-Agent Conversational AI Demo")
    print("This demo showcases how three AI agents collaborate to answer questions.")
    print("Each agent has a unique persona and knowledge domain.")
    
    # Create the agent system
    try:
        agent_system = create_agent_system()
        print("✅ Agent system initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent system: {e}")
        return
    
    # Example queries to demonstrate different collaboration scenarios
    demo_queries = [
        {
            "query": "What makes a good movie dialogue?",
            "description": "Analyzing dialogue quality and effectiveness"
        },
        {
            "query": "How do characters express emotions in movies?",
            "description": "Understanding emotional expression patterns"
        },
        {
            "query": "What are some common conversation patterns in films?",
            "description": "Identifying recurring dialogue structures"
        },
        {
            "query": "Tell me about different conversation styles in movies",
            "description": "Exploring various conversational approaches"
        }
    ]
    
    for i, demo in enumerate(demo_queries, 1):
        print_separator(f"Demo {i}: {demo['description']}")
        print(f"Query: {demo['query']}")
        print("\n🤖 Agents are collaborating...")
        
        # Create state for this query
        state = MultiAgentState()
        state.user_query = demo['query']
        state.messages = []
        
        try:
            # Run the agent system
            result = agent_system.invoke(state)
            
            # Display results
            print("\n📝 Combined Response:")
            print("-" * 40)
            
            # Show individual agent responses
            for agent_name in ['analyst', 'responder', 'storyteller']:
                if agent_name in result:
                    agent_result = result[agent_name]
                    print(f"\n🔍 {agent_name.title()}:")
                    print(f"   {agent_result.get('response', 'No response')}")
                    
                    # Show citations if available
                    if 'citations' in agent_result and agent_result['citations']:
                        print(f"   📚 Citations: {len(agent_result['citations'])} sources")
            
            # Show combined response
            if 'combine' in result:
                combined = result['combine']
                print(f"\n🎯 Final Collaborative Response:")
                print(f"   {combined.get('final_response', 'No combined response')}")
            
            print("\n" + "="*60)
            
        except Exception as e:
            print(f"❌ Error during collaboration: {e}")
        
        # Pause between demos
        if i < len(demo_queries):
            print("\n⏳ Waiting 3 seconds before next demo...")
            time.sleep(3)

def demo_agent_personas():
    """Demonstrate the distinct personas of each agent."""
    
    print_separator("🎭 Agent Persona Demonstration")
    print("Each agent has a unique personality and knowledge domain:")
    
    personas = [
        {
            "name": "🔍 Inquisitive Analyst",
            "persona": "analyst",
            "characteristics": [
                "Asks direct questions and makes observations",
                "Plans and organizes thoughts systematically",
                "Engaging and analytical approach",
                "Focuses on patterns and analysis"
            ],
            "knowledge": "Analytical and questioning dialogue patterns from movies"
        },
        {
            "name": "⚡ Concise Responder", 
            "persona": "responder",
            "characteristics": [
                "Short, reactive, and to-the-point statements",
                "Brief questions and affirmations",
                "Quick responses and clarifications",
                "Focused and direct communication"
            ],
            "knowledge": "Concise and reactive dialogue patterns from movies"
        },
        {
            "name": "📖 Narrative Storyteller",
            "persona": "storyteller", 
            "characteristics": [
                "Descriptive and expressive communication",
                "Shares detailed stories and opinions",
                "Provides rich context and background",
                "Verbose and engaging narrative style"
            ],
            "knowledge": "Narrative and expressive dialogue patterns from movies"
        }
    ]
    
    for persona in personas:
        print(f"\n{persona['name']}")
        print(f"Knowledge Domain: {persona['knowledge']}")
        print("Characteristics:")
        for char in persona['characteristics']:
            print(f"  • {char}")
        print("-" * 40)

def demo_citation_system():
    """Demonstrate the citation and transparency system."""
    
    print_separator("📚 Citation System Demonstration")
    print("Every agent response includes citations to movie dialogues:")
    
    citation_example = {
        "source": "movie_dialogues",
        "persona": "Inquisitive Analyst", 
        "context": "Character: John McClane - \"Yippee-ki-yay, motherf***er!\" (Movie: Die Hard)",
        "agent": "Inquisitive Analyst"
    }
    
    print("\nExample Citation Format:")
    print(f"  Source: {citation_example['source']}")
    print(f"  Persona: {citation_example['persona']}")
    print(f"  Context: {citation_example['context']}")
    print(f"  Agent: {citation_example['agent']}")
    
    print("\nCitation Features:")
    print("  ✅ Source Tracking: All information traceable to movie dialogues")
    print("  ✅ Agent Attribution: Clear distinction between agent knowledge")
    print("  ✅ Transparency: Users can verify information sources")
    print("  ✅ Inter-Agent Attribution: Proper credit for collaborative insights")

def main():
    """Run the complete demo."""
    
    print("🎬 Welcome to the Multi-Agent Conversational AI Demo!")
    print("This system demonstrates autonomous agent collaboration using LangGraph.")
    
    # Check if data files exist
    required_files = [
        'data/persona_0_data.csv',
        'data/persona_1_data.csv', 
        'data/persona_2_data.csv'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"\n❌ Missing required data files: {missing_files}")
        print("Please run the data processing first:")
        print("  python backend/data_loader.py")
        print("  python backend/persona_discovery.py")
        return
    
    # Run demos
    demo_agent_personas()
    demo_citation_system()
    demo_agent_collaboration()
    
    print_separator("🎉 Demo Complete!")
    print("To interact with the system:")
    print("  1. Start the server: python backend/api.py")
    print("  2. Open the frontend: http://localhost:8000")
    print("  3. Ask questions and watch the agents collaborate!")

if __name__ == "__main__":
    main() 