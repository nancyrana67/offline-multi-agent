"""Main NiceGUI application."""
from nicegui import ui
import asyncio
import logging
from typing import Dict, Any

from core.orchestrator import AgentOrchestrator
from core.message import Message, MessageRole, MessageType
from core.task import Task, TaskStatus
from agents import (
    SupervisorAgent,
    ChatAgent,
    CodingAgent,
    DataAgent,
    WritingAgent,
    MemoryAgent,
    RAGAgent,
    CriticAgent,
)
from memory import ConversationMemory
from rag import RAGRetriever
from ui.theme import LIGHT_THEME, DARK_THEME, CSS_STYLES
from ui.components import AIWorkspaceComponents
from config import UI_HOST, UI_PORT, DEBUG

logger = logging.getLogger(__name__)


class AIWorkspace:
    """Main AI Workspace application."""

    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.memory = ConversationMemory()
        self.rag = RAGRetriever()
        self.components = AIWorkspaceComponents()
        self.current_theme = "light"
        self.active_workspace = "chat"
        
        # Initialize agents
        self._init_agents()
        
        # UI elements
        self.chat_area = None
        self.status_area = None
        self.agent_status_displays = {}

    def _init_agents(self):
        """Initialize all agents."""
        agents = [
            SupervisorAgent(),
            ChatAgent(),
            CodingAgent(),
            DataAgent(),
            WritingAgent(),
            MemoryAgent(),
            RAGAgent(),
            CriticAgent(),
        ]
        
        for agent in agents:
            self.orchestrator.register_agent(agent)
        
        # Set subordinate agents for supervisor
        supervisor = self.orchestrator.get_agent("supervisor")
        if supervisor:
            supervisor.set_subordinate_agents([
                "chat", "coding", "data", "writing", "memory", "rag", "critic"
            ])

    def build_ui(self):
        """Build the main UI."""
        # Apply theme
        ui.add_css(CSS_STYLES)
        
        # Main layout
        with ui.column().classes("w-full h-full gap-0"):
            # Header
            self._build_header()
            
            # Main content area
            with ui.row().classes("flex-grow gap-2"):
                # Sidebar
                self._build_sidebar()
                
                # Main workspace
                self._build_main_area()
            
            # Status bar
            self._build_status_bar()

    def _build_header(self):
        """Build header."""
        with ui.row().classes("w-full items-center bg-gradient px-6 py-4"):
            ui.label("🤖 Offline AI Workspace").classes("text-2xl font-bold text-white flex-grow")
            
            # Theme toggle
            ui.button(
                "🌙" if self.current_theme == "light" else "☀️",
                on_click=self._toggle_theme
            ).classes("bg-white text-gray-800 px-4 py-2 rounded-lg")
            
            # Status indicator
            ui.label("● ONLINE").classes("text-green-300 font-bold")

    def _build_sidebar(self):
        """Build sidebar navigation."""
        with ui.column().classes("w-64 bg-gradient rounded-lg p-4"):
            ui.label("WORKSPACE").classes("text-white font-bold text-lg mb-4")
            
            workspaces = [
                ("chat", "💬", "Chat"),
                ("research", "🔍", "Research"),
                ("documents", "📄", "Documents"),
                ("data", "📊", "Data Lab"),
                ("coding", "💻", "Coding"),
                ("writing", "✍️", "Writing"),
                ("memory", "🧠", "Memory"),
                ("tools", "🔧", "Tools"),
            ]
            
            for ws_id, emoji, label in workspaces:
                btn = ui.button(f"{emoji} {label}", on_click=lambda w=ws_id: self._switch_workspace(w))
                btn.classes("w-full text-left text-white hover:bg-white hover:text-gray-800 transition")

    def _build_main_area(self):
        """Build main content area."""
        with ui.column().classes("flex-grow gap-4"):
            # Chat interface
            with ui.card().classes("flex-grow"):
                ui.label("Chat with AI Agents").classes("text-lg font-bold")
                
                # Chat display
                self.chat_area = ui.column().classes("h-96 overflow-y-auto bg-gray-50 p-4 rounded-lg")
                
                # Input area
                with ui.row().classes("w-full gap-2"):
                    self.message_input = ui.input(
                        placeholder="Type your request...",
                        on_change=lambda: None
                    ).classes("flex-grow")
                    
                    ui.button(
                        "Send",
                        on_click=lambda: asyncio.create_task(self._send_message())
                    ).classes("bg-gradient text-white px-6 py-2 rounded-lg")

    def _build_status_bar(self):
        """Build status bar."""
        with ui.row().classes("w-full bg-gray-900 text-green-400 p-3 rounded-lg font-mono text-xs gap-4"):
            self.status_area = ui.label("Ready").classes("flex-grow")
            ui.label("Model: mistral").classes("text-yellow-400")
            ui.label("Agents: 8").classes("text-blue-400")

    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        ui.notify(f"Theme changed to {self.current_theme}")

    def _switch_workspace(self, workspace: str):
        """Switch active workspace."""
        self.active_workspace = workspace
        if self.status_area:
            self.status_area.text = f"Switched to {workspace} workspace"

    async def _send_message(self):
        """Handle message sending."""
        message_text = self.message_input.value
        if not message_text:
            return
        
        # Display user message
        self.components.message_display("user", message_text)
        self.message_input.value = ""
        
        # Update status
        if self.status_area:
            self.status_area.text = "Processing..."
        
        try:
            # Create task
            task = Task(
                title="User Request",
                description=message_text,
                user_request=message_text,
            )
            
            # Execute task
            result_task = await self.orchestrator.execute_task(task)
            
            # Display response
            if result_task.result:
                self.components.message_display("assistant", result_task.result)
            
            # Update status
            if self.status_area:
                self.status_area.text = "Ready"
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            if self.status_area:
                self.status_area.text = f"Error: {str(e)}"


def start_app():
    """Start the AI workspace application."""
    app = AIWorkspace()
    app.build_ui()
    ui.run(host=UI_HOST, port=UI_PORT, title="Offline AI Workspace")


if __name__ == "__main__":
    start_app()
