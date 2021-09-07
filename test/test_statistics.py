import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import HTTP_200_OK

from model.DTO.Statistics import Statistics

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio

class TestStatistics:
    async def test_get_stats(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for('statistics:recover-statistics'))
        json_data = res.json()
        res_statistics = Statistics(**json_data)
        assert res.status_code == HTTP_200_OK
        assert res_statistics == Statistics(count_mutant_dna=1, count_human_dna=1, ratio=1.0)
