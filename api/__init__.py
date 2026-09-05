"""
FinGuard AI API package.

The API layer is kept separate from the main Flask application so that
JSON endpoints can be maintained independently from the HTML views.
"""

from .routes import api_bp

__all__ = ["api_bp"]
