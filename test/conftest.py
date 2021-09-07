import os
import pytest
import alembic
import warnings

from alembic.config import Config
from fastapi import FastAPI
from httpx import AsyncClient


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope='session')
def apply_migrations():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    config = Config('alembic.ini')

    os.environ['TESTING'] = '1'

    alembic.command.upgrade(config, 'head')
    yield
    alembic.command.downgrade(config, 'base')


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from api.server import get_application

    return get_application()


# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url='http://testserver',
        headers={'Content-Type': 'application/json'}
    ) as client:
        yield client