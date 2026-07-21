"""
SupplyMind Enterprise AI

Application Entry Point

Exposes the configured ASGI application to the application server.
"""

from supplymind.application.factory import create_application


app = create_application()
