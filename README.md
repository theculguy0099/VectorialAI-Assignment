# Vectorial AI Take-Home Assignment: Full-Stack Multi-Agent Conversational AI

This repository contains the solution for the Vectorial AI take-home assignment - a multi-agent conversational AI system using LangGraph that demonstrates autonomous agent collaboration with distinct, data-driven personas.

## 🎯 Project Overview

This project implements a sophisticated multi-agent conversational AI system featuring three distinct AI agents with unique personas derived from the Cornell Movie-Dialogs Corpus. The agents can communicate and collaborate autonomously to solve problems, with a modern web interface for observation and interaction.

### Key Features

- **🤖 Multi-Agent Collaboration**: Three distinct AI agents with unique personas
- **📊 Data-Driven Personas**: Personas discovered through clustering analysis of movie dialogues
- **🔗 LangGraph Orchestration**: Sophisticated agent communication using LangGraph
- **📚 Citation System**: Comprehensive source tracking and attribution
- **💬 Interactive Interface**: Real-time chat interface for observing agent collaboration
- **🧪 Robust Testing**: Comprehensive test suite for agent functionality
- **🔄 Advanced Collaboration**: Agent-to-agent questioning and distinct collaboration styles
- **📊 Enhanced State Management**: Comprehensive tracking of collaboration flow and history
- **🧠 Collaborative Shared Memory**: Agents read/write to a shared memory with attribution, visible in the UI and cited in responses
- **🧑‍⚖️ Moderator Agent**: A moderator reviews all agent responses and memory, summarizes, and resolves conflicts
- **📈 Frontend Visualization**: Shared memory and moderator output are visualized in the chat interface

## 🚀 Creative Extensions

### Collaborative Shared Memory
- All agents can read from and write to a shared memory (a dict in the state).
- Each agent writes its own insight to memory, with attribution (agent name, content, timestamp).
- Shared memory is cited in agent and moderator responses, and is visualized in the frontend.

### Moderator Agent
- After all agents respond, a moderator agent reviews all responses and the shared memory.
- The moderator summarizes the main points, highlights consensus/disagreement, and resolves conflicts if any.
- Moderator output is included in the final response and visualized in the UI.

### Frontend Visualization
- The chat interface displays:
  - User and agent messages
  - Individual agent responses and collaboration styles
  - Shared memory (🧠) with all agent-contributed insights
  - Moderator summary (🧑‍⚖️) with a review of all agent responses and memory
- This makes the collaborative process transparent and easy to follow.

## 💡 How to Try the System

### 1. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Set up environment**
- For local development/testing (no OpenAI API needed):
  ```bash
  export MOCK_LLM=true
  ```
- Or add to your `.env` file:
  ```
  MOCK_LLM=true
  ```
- (For real LLMs, set your OpenAI API key and set `MOCK_LLM=false` or remove it.)

### 3. **Run the backend**
```bash
python backend/api.py
```

### 4. **Open the frontend**
- Open `frontend/index.html` in your browser, or if you have a static server:
  ```bash
  python -m http.server 8080
  # Then visit http://localhost:8080/frontend/index.html
  ```
- Or, if your FastAPI backend serves static files, visit http://localhost:8000

### 5. **Interact with the system**
- Type a question in the chat (e.g., "How do movie characters develop through their conversations?")
- Watch as:
  - Each agent responds with its persona and style
  - Shared memory (🧠) is updated with each agent's insight
  - The moderator (🧑‍⚖️) reviews all responses and memory, and provides a summary
  - All citations, memory, and collaboration flow are visualized in the chat

### 6. **What to Look For**
- **Agent Responses**: Each agent's unique style and knowledge
- **Shared Memory**: Insights from all agents, with attribution
- **Moderator Output**: Summary, consensus/disagreement, and conflict resolution
- **Citations**: All sources and memory are cited for transparency
- **Collaboration Flow**: See how information builds up through the workflow

## 🎬 Demo & Artifacts

- **Persona Discovery Notebook:** See [notebooks/persona_discovery.ipynb](notebooks/persona_discovery.ipynb) for full data analysis and persona clustering.
- **Demo Conversation:** See [demo_conversation.md](demo_conversation.md) for a sample multi-agent collaborative session.
- **Demo Scripts:** Try [demo.py](demo.py) or [demo_phase2.py](demo_phase2.py) for scripted runs.
- **(Optional)** If you have a video/gif demo, add a link or embed here.

## 🧪 Testing
- All tests pass with `MOCK_LLM=true` (no OpenAI API needed for development/CI)
- Run:
  ```bash
  export MOCK_LLM=true
  python -m unittest discover tests
  ```

## 🏆 Creative/Bonus Features
- **Collaborative memory**: Agents build on each other's insights, and memory is visible and cited
- **Moderator**: Ensures high-quality, consensus-driven, and transparent output
- **Visualization**: All collaboration, memory, and moderation is visible in the UI

## 📄 License
This project is part of the Vectorial AI take-home assignment and demonstrates advanced AI system design and implementation.

---

**Built with ❤️ using LangGraph, FastAPI, and modern AI techniques**

**Version 2.0+ - Enhanced Collaboration, Memory, and Moderation**

## 🚧 Limitations & Future Work

- **LLM Dependency:** The system currently relies on a single LLM backbone; future work could include agent-specific models or more dynamic model selection.
- **Dataset Coverage:** Only the Cornell Movie-Dialogs Corpus is used. Broader datasets could yield richer persona diversity.
- **Persona Evolution:** Personas are static after initial clustering. Future versions could allow agents to adapt based on feedback or collaboration history.
- **UI/UX:** The frontend is functional but could be enhanced with richer visualizations (e.g., real-time graph of agent communication).
- **Scalability:** The current system is designed for 3–4 agents; scaling to dozens of agents or larger knowledge bases may require optimizations.
- **Advanced Collaboration:** Conflict resolution and negotiation between agents are basic; more sophisticated protocols could be added.

