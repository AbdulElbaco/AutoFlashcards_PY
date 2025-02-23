"""
Custom exceptions for the AutoFlashcards application.
"""

class AutoFlashcardsError(Exception):
    """Base exception class for AutoFlashcards"""
    pass

class PDFProcessingError(AutoFlashcardsError):
    """Raised when PDF processing fails"""
    pass

class TextExtractionError(AutoFlashcardsError):
    """Raised when text extraction fails"""
    pass

class AIProcessingError(AutoFlashcardsError):
    """Raised when AI processing fails"""
    pass

class AnkiConnectionError(AutoFlashcardsError):
    """Raised when Anki connection fails"""
    pass 