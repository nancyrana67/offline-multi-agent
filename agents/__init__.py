"""Agents module initialization."""
from agents.supervisor import SupervisorAgent
from agents.chat import ChatAgent
from agents.coding import CodingAgent
from agents.data import DataAgent
from agents.writing import WritingAgent
from agents.memory import MemoryAgent
from agents.rag import RAGAgent
from agents.critic import CriticAgent

__all__ = [
    "SupervisorAgent",
    "ChatAgent",
    "CodingAgent",
    "DataAgent",
    "WritingAgent",
    "MemoryAgent",
    "RAGAgent",
    "CriticAgent",
]
