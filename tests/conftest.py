import os
import socket
from urllib.parse import urlparse

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


def db_available(database_url: str) -> bool:
    try:
        parsed = urlparse(database_url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 5432
        with socket.create_connection((host, port), timeout=1):
            return True
    except Exception:
        return False


@pytest.fixture()
async def client():
    os.environ.setdefault("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/prisma")
    if not db_available(os.environ["DATABASE_URL"]):
        pytest.skip("Database not available")
    
    transport = ASGITransport(app=app)
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
            yield ac
