"""Custom exceptions for graph_tool calculators."""

import logging

# Module-level logger for calculator errors
logger = logging.getLogger(__name__)


class CalculationError(Exception):
    """Custom exception for calculator errors.
    
    Raised when a calculation fails due to invalid input, missing parameters,
    or other error conditions during computation.
    """
    
    def __init__(self, message: str, operation: str = None, context: dict = None):
        """Initialize CalculationError.
        
        Args:
            message: Descriptive error message explaining the failure.
            operation: The operation that was being performed.
            context: Additional context about the error (e.g., input parameters).
        """
        super().__init__(message)
        self.operation = operation
        self.context = context or {}
    
    def __repr__(self):
        parts = [f"CalculationError: {self.args[0]}"]
        if self.operation:
            parts.append(f"operation={self.operation}")
        if self.context:
            parts.append(f"context={self.context}")
        return f"({' '.join(parts)})"
