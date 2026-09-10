"""Calculator tool."""
import math
import logging

logger = logging.getLogger(__name__)


class Calculator:
    """Simple calculator tool."""

    @staticmethod
    def evaluate(expression: str) -> float:
        """Safely evaluate mathematical expression."""
        try:
            # Only allow safe operations
            allowed_names = {
                'abs': abs, 'round': round, 'pow': pow,
                'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
                'tan': math.tan, 'log': math.log, 'exp': math.exp,
                'pi': math.pi, 'e': math.e
            }
            return eval(expression, {"__builtins__": {}}, allowed_names)
        except Exception as e:
            logger.error(f"Calculator error: {str(e)}")
            return 0

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
