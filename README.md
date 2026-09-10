# Offline Multi-Agent AI Workspace

A production-quality, fully offline multi-agent AI workspace built with Python, Ollama, and NiceGUI.

## Features

- ✅ **Multi-Agent System** - 10+ specialized AI agents working collaboratively
- ✅ **Offline First** - No cloud APIs required, runs completely locally
- ✅ **Supervisor Agent** - Intelligent task orchestration and planning
- ✅ **Tool Calling** - Dynamic tool selection and execution
- ✅ **RAG System** - Local document indexing and semantic search
- ✅ **Memory System** - Persistent conversation and long-term memory
- ✅ **Modern UI** - NiceGUI with light/dark theme support
- ✅ **Real-time Visualization** - Agent activity and task progress monitoring
- ✅ **Code Execution** - Controlled Python execution for data analysis
- ✅ **Data Lab** - Interactive CSV/Excel analysis
- ✅ **Document Workspace** - PDF, DOCX, TXT processing
- ✅ **Coding Workspace** - Code generation and debugging
- ✅ **Writing Assistant** - Grammar, rewriting, summarization
- ✅ **Presentation Generator** - Create PPTX presentations

## Quick Start

### Prerequisites

- Python 3.10+
- Ollama installed and running
- At least 8GB RAM

### Installation

```bash
# Clone repository
git clone https://github.com/nancyrana67/offline-multi-agent.git
cd offline-multi-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Make sure Ollama is running
ollama serve

# In another terminal
python app.py
```

The application will start at `http://localhost:8000`

## Project Structure

```
offline-multi-agent/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── README.md
│
├── agents/               # AI agents
│   ├── __init__.py
│   ├── supervisor.py
│   ├── chat.py
│   ├── research.py
│   ├── document.py
│   ├── data.py
│   ├── coding.py
│   ├── writing.py
│   ├── math.py
│   ├── presentation.py
│   ├── memory.py
│   ├── rag.py
│   └── critic.py
│
├── core/                 # Core functionality
│   ├── __init__.py
│   ├── agent_base.py
│   ├── message.py
│   ├── task.py
│   └── orchestrator.py
│
├─��� tools/               # Tool definitions
│   ├── __init__.py
│   ├── calculator.py
│   ├── python_executor.py
│   ├── file_reader.py
│   ├── pdf_reader.py
│   ├── docx_reader.py
│   ├── csv_analyzer.py
│   ├── excel_analyzer.py
│   ├── chart_generator.py
│   ├── code_executor.py
│   ├── file_search.py
│   └── tool_manager.py
│
├── rag/                 # RAG System
│   ├── __init__.py
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── retriever.py
│
├── memory/              # Memory System
│   ├── __init__.py
│   ├── conversation_memory.py
│   ├── long_term_memory.py
│   ├── project_memory.py
│   └── memory_manager.py
│
├── models/              # Model management
│   ├── __init__.py
│   └── model_manager.py
│
├── prompts/             # Prompt templates
│   ├── supervisor.txt
│   ├── chat.txt
│   ├── research.txt
│   ├── coding.txt
│   ├── data.txt
│   ├── writing.txt
│   ├── rag.txt
│   └── critic.txt
│
├── ui/                  # NiceGUI interface
│   ├── __init__.py
│   ├── pages.py
│   ├── components.py
│   ├── theme.py
│   └── styles.css
│
├── data/               # Data storage (git ignored)
├── uploads/            # User uploads (git ignored)
├── outputs/            # Generated outputs (git ignored)
└── tests/             # Tests
    ├── __init__.py
    └── test_agents.py
```

## Architecture

### Multi-Agent Flow

```
User Request
     ↓
Supervisor Agent
     ↓
Task Understanding & Planning
     ↓
Agent Selection & Delegation
     ↓
Agent Collaboration & Tool Usage
     ↓
RAG/Memory Integration
     ↓
Critic Verification
     ↓
Final Response
```

## Configuration

Create a `.env` file in the project root:

```env
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=mistral
EMBEDDING_MODEL=nomic-embed-text
DEBUG=false
```

## Available Models (Ollama)

- **Chat**: `mistral`, `neural-chat`, `openchat`
- **Coding**: `codellama`, `mistral`
- **Embeddings**: `nomic-embed-text`, `all-minilm`

Install with: `ollama pull model-name`

## Performance Tips

1. Use smaller models (7B) for general tasks
2. Use specialized models for specific tasks (codellama for coding)
3. Use embedding models with fewer parameters
4. Batch document processing
5. Clear memory periodically

## Development

The project follows a modular architecture:

- Each agent is independent but communicates through the Supervisor
- Tools are composable and reusable
- UI components are built with NiceGUI
- All configurations are externalized

## License

MIT

## Author

Nancy Rana (@nancyrana67)
