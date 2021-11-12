import pytest
import requests
from nameko.testing.services import worker_factory
from dataclasses import asdict
from app.errors import Unavailable, InvalidResponseData, InvalidRequestData
from app.consts import BASE_URL
from app.service import PokemonResponse, PokemonService


@pytest.fixture
def pokemon_service():
    return worker_factory(PokemonService)


@pytest.fixture
def pokemon_response():
    return PokemonResponse(
        id=0, moves_info=[{"move": {"name": "transform"}}, {"move": {"name": "jump"}}]
    )


def test_pokemon_response_past_init(pokemon_response):
    assert pokemon_response.moves_names == ["transform", "jump"]


def test_pokemon_response_sort_moves(pokemon_response):
    assert pokemon_response.moves_names == ["transform", "jump"]
    pokemon_response.sort_moves()
    assert pokemon_response.moves_names == ["jump", "transform"]


def test_pokemon_response_with_no_moves():
    with pytest.raises(InvalidResponseData):
        PokemonResponse(id=0, moves_info=[])


def test_pokemon_response_with_arbitrary_field_names():
    with pytest.raises(InvalidResponseData):
        PokemonResponse(id=0, moves_info=[{"move": "transform"}])


def test_service(requests_mock):
    pokemon_id = 1
    moves_info = [{"move": {"name": "transform"}}, {"move": {"name": "jump"}}]
    pokemon_service = worker_factory(PokemonService)
    requests_mock.get(
        f"{BASE_URL}/{pokemon_id}", json={"id": pokemon_id, "moves": moves_info}
    )
    result = pokemon_service.get_pokemon_info(pokemon_id)
    assert result == asdict(PokemonResponse(id=pokemon_id, moves_info=moves_info))


def test_service_fail(requests_mock):
    pokemon_id = 0
    pokemon_service = worker_factory(PokemonService)
    requests_mock.get(f"{BASE_URL}/{pokemon_id}", status_code=404)
    with pytest.raises(InvalidRequestData):
        pokemon_service.get_pokemon_info(pokemon_id)


def test_service_timeout(requests_mock):
    pokemon_id = 0
    pokemon_service = worker_factory(PokemonService)
    requests_mock.get(f"{BASE_URL}/{pokemon_id}", exc=requests.exceptions.Timeout)
    with pytest.raises(Unavailable):
        pokemon_service.get_pokemon_info(pokemon_id)


def test_service_connection_error(requests_mock):
    pokemon_id = 0
    pokemon_service = worker_factory(PokemonService)
    requests_mock.get(
        f"{BASE_URL}/{pokemon_id}", exc=requests.exceptions.ConnectionError
    )
    with pytest.raises(Unavailable):
        pokemon_service.get_pokemon_info(pokemon_id)


def test_service_http_error(requests_mock):
    pokemon_id = 0
    pokemon_service = worker_factory(PokemonService)
    requests_mock.get(f"{BASE_URL}/{pokemon_id}", exc=requests.exceptions.HTTPError)
    with pytest.raises(InvalidRequestData):
        pokemon_service.get_pokemon_info(pokemon_id)
