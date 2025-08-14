import logging
import traceback
from functools import wraps
from typing import Any, Callable, Optional, Dict
from dataclasses import dataclass
from enum import Enum

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ParseError:
    """Structured error information"""
    code: str
    message: str
    severity: ErrorSeverity
    component: str
    details: Optional[Dict] = None
    recoverable: bool = True

class ResumeParsingException(Exception):
    """Custom exception for resume parsing errors"""
    
    def __init__(self, error: ParseError, original_exception: Exception = None):
        self.error = error
        self.original_exception = original_exception
        super().__init__(error.message)

class ErrorHandler:
    """Centralized error handling and logging"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def handle_error(self, error: ParseError, exception: Exception = None) -> None:
        """Log and handle errors based on severity"""
        log_message = f"[{error.component}] {error.code}: {error.message}"
        
        if error.details:
            log_message += f" | Details: {error.details}"
        
        if exception:
            log_message += f" | Original: {str(exception)}"
        
        # Log based on severity
        if error.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message)
            if exception:
                self.logger.critical(traceback.format_exc())
        elif error.severity == ErrorSeverity.HIGH:
            self.logger.error(log_message)
        elif error.severity == ErrorSeverity.MEDIUM:
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def create_error(self, code: str, message: str, severity: ErrorSeverity, 
                    component: str, **kwargs) -> ParseError:
        """Create a structured error"""
        return ParseError(
            code=code,
            message=message,
            severity=severity,
            component=component,
            details=kwargs.get('details'),
            recoverable=kwargs.get('recoverable', True)
        )

def handle_parsing_errors(component: str):
    """Decorator for handling parsing errors"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            error_handler = ErrorHandler()
            
            try:
                return func(*args, **kwargs)
            
            except ResumeParsingException:
                # Re-raise our custom exceptions
                raise
            
            except FileNotFoundError as e:
                error = error_handler.create_error(
                    code="FILE_NOT_FOUND",
                    message=f"File not found: {str(e)}",
                    severity=ErrorSeverity.HIGH,
                    component=component,
                    recoverable=False
                )
                error_handler.handle_error(error, e)
                raise ResumeParsingException(error, e)
            
            except PermissionError as e:
                error = error_handler.create_error(
                    code="PERMISSION_DENIED",
                    message=f"Permission denied: {str(e)}",
                    severity=ErrorSeverity.HIGH,
                    component=component,
                    recoverable=False
                )
                error_handler.handle_error(error, e)
                raise ResumeParsingException(error, e)
            
            except MemoryError as e:
                error = error_handler.create_error(
                    code="MEMORY_EXHAUSTED",
                    message="Insufficient memory to process file",
                    severity=ErrorSeverity.CRITICAL,
                    component=component,
                    recoverable=False
                )
                error_handler.handle_error(error, e)
                raise ResumeParsingException(error, e)
            
            except Exception as e:
                error = error_handler.create_error(
                    code="UNEXPECTED_ERROR",
                    message=f"Unexpected error in {component}: {str(e)}",
                    severity=ErrorSeverity.MEDIUM,
                    component=component,
                    details={"exception_type": type(e).__name__}
                )
                error_handler.handle_error(error, e)
                raise ResumeParsingException(error, e)
        
        return wrapper
    return decorator

# Global error handler instance
error_handler = ErrorHandler()
