import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_422_UNPROCESSABLE_ENTITY

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio

MUTANT_DNA = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
HUMAN_DNA = ["ATGCGA", "CAGTGC", "TTATTT", "AGACGG", "GCGTCA", "TCACTG"]


class TestDNARoutes:
    async def test_dna_not_a_list(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for('mutants:check-store-dna'), json={'dna': ''})
        json_data = res.json()
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert json_data['detail'][0]['msg'] == 'value is not a valid list'
    
    async def test_dna_must_contain_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for('mutants:check-store-dna'), json={'dna': ['string']})
        json_data = res.json()
        assert res.status_code == HTTP_403_FORBIDDEN
        assert json_data['detail'] == 'DNA must contain only A, T, C, G'

    async def test_dna_empty_list_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for('mutants:check-store-dna'), json={'dna': []})
        json_data = res.json()
        assert res.status_code == HTTP_403_FORBIDDEN
        assert json_data['detail'] == 'Empty DNA'

    async def test_dna_mutant(self, app: FastAPI, client: AsyncClient):
        res = await client.post(app.url_path_for('mutants:check-store-dna'), json={'dna': MUTANT_DNA})
        json_data = res.json()
        assert res.status_code == HTTP_200_OK
        assert json_data == 'The dna is from a mutant'

    async def test_dna_human(self, app: FastAPI, client: AsyncClient):
        res = await client.post(app.url_path_for('mutants:check-store-dna'), json={'dna': HUMAN_DNA})
        json_data = res.json()
        assert res.status_code == HTTP_200_OK
        assert json_data == 'The dna is from a human'
