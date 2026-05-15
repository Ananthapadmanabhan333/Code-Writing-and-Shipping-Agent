# Aether OS: The Autonomous Engineering Operating System

Aether OS is a state-of-the-art, AI-native autonomous coding platform. It functions as a complete self-operating engineering team, capable of taking high-level product requirements and delivering fully implemented, tested, and deployed software.

## 🚀 Key Features
- **LangGraph Multi-Agent Orchestration**: Specialized agents (PM, Tech Lead, Engineers) collaborating on complex tasks.
- **Sandboxed Execution**: Isolated Docker environments for running and testing generated code.
- **Recursive Self-Debugging**: Autonomous failure analysis and patch generation.
- **Vector Engineering Memory**: Long-term memory of architectural patterns and previous decisions.
- **Real-time Observability**: Cinematic dashboard for tracking agent reasoning and execution state.

## 🛠 Tech Stack
- **Frontend**: Next.js 15, Tailwind CSS, Framer Motion, Zustand.
- **Backend**: FastAPI, LangGraph, LangChain, Pydantic AI.
- **AI**: OpenAI GPT-4o, Claude 3.5 Sonnet.
- **Infrastructure**: Docker, Redis, Qdrant (Vector DB).

## 📦 Getting Started

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key
- Anthropic API Key (Optional)

### Installation
1. Clone the repository
2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
3. Start the system:
   ```bash
   docker-compose up --build
   ```

## 🏗 System Architecture
The system uses a directed acyclic graph (DAG) managed by LangGraph to orchestrate agent handoffs. Each node represents an agent (e.g., Product Manager) and each edge represents a transition or decision (e.g., "Ready for QA").

## 🛡 Security
Aether OS executes all code within isolated Docker containers to prevent host contamination. It also includes a security auditor agent that scans all generated code for potential vulnerabilities.

---
Built with ❤️ by Antigravity.
