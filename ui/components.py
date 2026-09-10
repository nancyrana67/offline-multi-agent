"""NiceGUI components."""
from nicegui import ui
from typing import Callable, Optional, List, Dict, Any


class AIWorkspaceComponents:
    """Reusable AI workspace components."""

    @staticmethod
    def status_indicator(status: str, label: str = ""):
        """Create a status indicator."""
        color = {
            "idle": "gray",
            "working": "orange",
            "complete": "green",
            "error": "red",
            "waiting": "blue",
        }.get(status, "gray")
        
        with ui.row():
            ui.icon("circle").props(f"size=sm color={color}")
            if label:
                ui.label(label).classes("text-sm")

    @staticmethod
    def agent_card(agent_name: str, status: str = "idle", progress: float = 0.0):
        """Create an agent status card."""
        with ui.card().classes("w-full"):
            with ui.row():
                color = {"idle": "gray", "working": "orange", "complete": "green", "error": "red"}.get(status, "gray")
                ui.icon("smart_toy").props(f"size=md color={color}")
                ui.label(agent_name).classes("text-lg font-bold")
                ui.label(status).classes(f"text-sm text-{color}-500")
            
            if progress > 0:
                ui.linear_progress(value=progress).classes("w-full")

    @staticmethod
    def task_progress_panel(task_name: str, subtasks: List[Dict[str, Any]]):
        """Create a task progress panel."""
        with ui.card().classes("w-full"):
            ui.label(f"Task: {task_name}").classes("text-lg font-bold")
            
            for subtask in subtasks:
                status_icon = "check_circle" if subtask.get("status") == "complete" else "hourglass_empty"
                with ui.row():
                    ui.icon(status_icon).props("size=sm")
                    ui.label(subtask.get("name", "Subtask")).classes("flex-grow")

    @staticmethod
    def message_display(role: str, content: str, timestamp: str = ""):
        """Display a message."""
        bg_color = "bg-blue-100" if role == "user" else "bg-gray-100"
        with ui.card().classes(f"w-full {bg_color}"):
            with ui.row().classes("w-full items-center"):
                ui.label(f"{role.upper()}").classes("font-bold text-xs")
                if timestamp:
                    ui.label(timestamp).classes("text-xs text-gray-500 flex-grow text-right")
            ui.label(content).classes("whitespace-pre-wrap")

    @staticmethod
    def workspace_nav(items: List[str], on_select: Callable):
        """Create navigation for workspaces."""
        with ui.column().classes("w-full gap-2"):
            for item in items:
                ui.button(item, on_click=lambda i=item: on_select(i)).classes("w-full")
