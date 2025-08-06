#!/usr/bin/env python3
"""
Phase 2 Demo: Advanced Collaboration Features
This script demonstrates the enhanced multi-agent system with advanced collaboration capabilities.
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
        print(f"\n{'='*70}")
        print(f" {title}")
        print(f"{'='*70}")
    else:
        print(f"\n{'='*70}")

def demo_enhanced_collaboration():
    """Demonstrate enhanced collaboration with agent questioning and styles."""
    
    print_separator("🤖 Phase 2: Advanced Collaboration Demo")
    print("This demo showcases enhanced agent collaboration with:")
    print("• Agent-to-agent questioning")
    print("• Distinct collaboration styles")
    print("• Enhanced state management")
    print("• Collaboration flow tracking")
    
    # Create the agent system
    try:
        agent_system = create_agent_system()
        print("✅ Enhanced agent system initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent system: {e}")
        return
    
    # Enhanced demo queries with collaboration scenarios
    demo_queries = [
        {
            "query": "How do movie characters develop through their conversations?",
            "description": "Character development analysis with agent questioning",
            "expected_collaboration": "Analyst will ask probing questions about patterns, Responder will provide quick insights on key moments, Storyteller will share detailed character arcs"
        },
        {
            "query": "What makes dialogue feel natural and authentic in films?",
            "description": "Authenticity analysis with collaboration insights",
            "expected_collaboration": "Analyst will analyze authenticity patterns, Responder will highlight natural moments, Storyteller will provide rich context about realistic dialogue"
        },
        {
            "query": "How do different genres approach dialogue differently?",
            "description": "Genre analysis with multi-perspective collaboration",
            "expected_collaboration": "Analyst will map genre patterns, Responder will identify genre-specific techniques, Storyteller will weave genre narratives together"
        }
    ]
    
    for i, demo in enumerate(demo_queries, 1):
        print_separator(f"Demo {i}: {demo['description']}")
        print(f"Query: {demo['query']}")
        print(f"Expected Collaboration: {demo['expected_collaboration']}")
        print("\n🤖 Agents are collaborating with advanced features...")
        
        # Use a dict for state
        state = {
            "user_query": demo['query'],
            "messages": [],
            "collaboration_history": [
                {'agent': 'analyst', 'response': 'Previous analytical insight'},
                {'agent': 'responder', 'response': 'Previous quick response'},
                {'agent': 'storyteller', 'response': 'Previous narrative example'}
            ]
        }
        
        try:
            # Run the enhanced agent system
            result = agent_system.invoke(state)
            
            # Display enhanced results
            print("\n📝 Enhanced Collaborative Response:")
            print("-" * 50)
            
            # Show individual agent responses with collaboration styles
            for agent_name in ['analyst', 'responder', 'storyteller']:
                if agent_name in result:
                    agent_result = result[agent_name]
                    style = agent_result.get('collaboration_style', {}).get('style', 'general')
                    print(f"\n🔍 {agent_name.title()} ({style.upper()}):")
                    print(f"   Response: {agent_result.get('response', 'No response')}")
                    
                    # Show questions for other agents
                    if 'questions_for_others' in agent_result:
                        questions = agent_result['questions_for_others']
                        if questions:
                            print(f"   Questions for others:")
                            for target_agent, question in questions.items():
                                print(f"     → {target_agent.title()}: \"{question}\"")
                    
                    # Show citations
                    if 'citations' in agent_result and agent_result['citations']:
                        print(f"   📚 Citations: {len(agent_result['citations'])} sources")
            
            # Show enhanced combined response
            if 'combine' in result:
                combined = result['combine']
                print(f"\n🎯 Final Collaborative Response:")
                print(f"   {combined.get('final_response', 'No combined response')}")
                
                # Show shared memory
                memory = combined.get('shared_memory', {})
                if memory:
                    print(f"\n🧠 Shared Memory:")
                    for k, v in memory.items():
                        print(f"   - {k}: {v['content']} (by {v['agent']})")
                # Show collaboration summary
                if 'collaboration_summary' in combined:
                    print(f"\n📊 Collaboration Summary:")
                    for summary in combined['collaboration_summary']:
                        print(f"   • {summary['agent'].title()} ({summary['style']}): {summary['contribution'][:60]}...")
            
            # Show moderator output
            if 'moderator' in result:
                moderator = result['moderator']
                print(f"\n🧑‍⚖️ Moderator Summary:")
                print(f"   {moderator.get('summary', 'No summary')}")
                print(f"   Agents Reviewed: {', '.join(moderator.get('agents_reviewed', []))}")
            print("\n" + "="*70)
            
        except Exception as e:
            print(f"❌ Error during enhanced collaboration: {e}")
        
        # Pause between demos
        if i < len(demo_queries):
            print("\n⏳ Waiting 3 seconds before next demo...")
            time.sleep(3)

def demo_collaboration_styles():
    """Demonstrate the distinct collaboration styles of each agent."""
    
    print_separator("🎭 Enhanced Collaboration Styles Demo")
    print("Each agent has a unique collaboration style and approach:")
    
    collaboration_styles = [
        {
            "name": "🔍 Inquisitive Analyst",
            "style": "analytical",
            "approach": "seeks understanding through questions",
            "strengths": ["pattern recognition", "critical thinking", "questioning"],
            "conflict_handling": "analyzes and proposes solutions",
            "example_behavior": "Asks probing questions to understand other agents' perspectives"
        },
        {
            "name": "⚡ Concise Responder",
            "style": "reactive", 
            "approach": "provides immediate feedback and clarification",
            "strengths": ["quick responses", "direct communication", "efficiency"],
            "conflict_handling": "seeks quick resolution",
            "example_behavior": "Provides quick, focused responses that move conversation forward"
        },
        {
            "name": "📖 Narrative Storyteller",
            "style": "narrative",
            "approach": "weaves different perspectives into coherent narratives",
            "strengths": ["storytelling", "context building", "emotional intelligence"],
            "conflict_handling": "seeks common ground through storytelling",
            "example_behavior": "Connects different perspectives into rich, coherent stories"
        }
    ]
    
    for style in collaboration_styles:
        print(f"\n{style['name']}")
        print(f"  Style: {style['style'].title()}")
        print(f"  Approach: {style['approach']}")
        print(f"  Strengths: {', '.join(style['strengths'])}")
        print(f"  Conflict Handling: {style['conflict_handling']}")
        print(f"  Example Behavior: {style['example_behavior']}")
        print("-" * 50)

def demo_agent_questioning():
    """Demonstrate agent-to-agent questioning capabilities."""
    
    print_separator("🤔 Agent-to-Agent Questioning Demo")
    print("Agents can now ask questions to each other to enhance collaboration:")
    
    questioning_patterns = [
        {
            "from_agent": "Analyst",
            "to_agent": "Storyteller", 
            "question_type": "analytical",
            "example": "What specific examples can you provide to support your narrative perspective?"
        },
        {
            "from_agent": "Responder",
            "to_agent": "Analyst",
            "question_type": "reactive", 
            "example": "Can you clarify the key patterns you've identified?"
        },
        {
            "from_agent": "Storyteller",
            "to_agent": "Responder",
            "question_type": "narrative",
            "example": "How do these quick responses fit into the broader character development?"
        }
    ]
    
    for pattern in questioning_patterns:
        print(f"\n{pattern['from_agent']} → {pattern['to_agent']}")
        print(f"  Question Type: {pattern['question_type'].title()}")
        print(f"  Example: \"{pattern['example']}\"")
        print(f"  Purpose: {pattern['from_agent']} seeks to understand {pattern['to_agent']}'s perspective")
        print("-" * 40)

def demo_enhanced_state_management():
    """Demonstrate enhanced state management features."""
    
    print_separator("📊 Enhanced State Management Demo")
    print("The system now tracks comprehensive collaboration state:")
    
    state_features = [
        {
            "feature": "Conversation ID",
            "description": "Unique identifier for each conversation",
            "purpose": "Track conversation history and context"
        },
        {
            "feature": "Agent Questions",
            "description": "Questions agents ask each other",
            "purpose": "Enable agent-to-agent communication"
        },
        {
            "feature": "Collaboration Flow",
            "description": "Step-by-step collaboration tracking",
            "purpose": "Monitor how agents work together"
        },
        {
            "feature": "Collaboration History",
            "description": "Previous agent interactions",
            "purpose": "Provide context for future responses"
        },
        {
            "feature": "Consensus Tracking",
            "description": "Track when agents reach agreement",
            "purpose": "Monitor collaboration effectiveness"
        },
        {
            "feature": "Conflict Resolution",
            "description": "Handle disagreements between agents",
            "purpose": "Maintain productive collaboration"
        }
    ]
    
    for feature in state_features:
        print(f"\n• {feature['feature']}")
        print(f"  Description: {feature['description']}")
        print(f"  Purpose: {feature['purpose']}")

def demo_collaboration_scenarios():
    """Demonstrate different collaboration scenarios."""
    
    print_separator("🎯 Advanced Collaboration Scenarios Demo")
    print("The system supports various collaboration patterns:")
    
    scenarios = [
        {
            "name": "Analytical Lead",
            "description": "Analyst initiates with questions, others build on insights",
            "pattern": "Question → Insight → Synthesis",
            "example": "Analyzing dialogue patterns across genres"
        },
        {
            "name": "Reactive Support", 
            "description": "Responder provides quick feedback, others elaborate",
            "pattern": "Quick Response → Clarification → Expansion",
            "example": "Identifying key moments in conversations"
        },
        {
            "name": "Narrative Synthesis",
            "description": "Storyteller weaves different perspectives together",
            "pattern": "Multiple Perspectives → Narrative Connection → Coherent Story",
            "example": "Building character development narratives"
        },
        {
            "name": "Iterative Refinement",
            "description": "Agents iteratively improve their understanding",
            "pattern": "Initial Response → Question → Refined Response",
            "example": "Deep analysis of complex dialogue patterns"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 {scenario['name']}")
        print(f"  Description: {scenario['description']}")
        print(f"  Pattern: {scenario['pattern']}")
        print(f"  Example: {scenario['example']}")
        print("-" * 40)

def main():
    """Run the complete Phase 2 demo."""
    
    print("🎬 Phase 2: Advanced Collaboration Features Demo")
    print("This demo showcases the enhanced multi-agent system with advanced collaboration capabilities.")
    
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
    
    # Run enhanced demos
    demo_collaboration_styles()
    demo_agent_questioning()
    demo_enhanced_state_management()
    demo_collaboration_scenarios()
    demo_enhanced_collaboration()
    
    print_separator("🎉 Phase 2 Demo Complete!")
    print("Advanced collaboration features demonstrated:")
    print("✅ Agent-to-agent questioning")
    print("✅ Distinct collaboration styles")
    print("✅ Enhanced state management")
    print("✅ Collaboration flow tracking")
    print("✅ Advanced response synthesis")
    print("\nTo interact with the enhanced system:")
    print("  1. Start the server: python backend/api.py")
    print("  2. Open the frontend: http://localhost:8000")
    print("  3. Experience advanced agent collaboration!")

if __name__ == "__main__":
    main() 