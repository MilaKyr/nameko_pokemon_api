from typing import List, Dict, TypeVar
import requests
from dataclasses import dataclass, field
from nameko.rpc import rpc

from app import errors
from app.consts import BASE_URL


MovesInfo = TypeVar("MovesInfo", bound=List[Dict[str, Dict[str, str]]])


@dataclass(frozen=True)
class PokemonResponse:
    """Stores the information from API about pokemon moves"""

    id: int
    moves_info: MovesInfo
    moves_names: List[str] = field(init=False)

    def parse_move_names(self) -> List[str]:
        """Parse moves_info into list of move names, if None or no parameters throw exception"""
        try:
            assert self.moves_info
            moves_info = [move_info.get("move") for move_info in self.moves_info]
            moves = [info.get("name") for info in moves_info]
            return moves
        except (TypeError, AttributeError) as e:
            raise errors.InvalidResponseData(
                "Something wrong with the response from API, " f"more specifically: {e}"
            )
        except AssertionError:
            raise errors.InvalidResponseData(
                "Absent information about moves in response"
            )

    def __post_init__(self):
        object.__setattr__(self, "moves_names", self.parse_move_names())

    def sort_moves(self):
        self.moves_names.sort()


class PokemonService:
    name = "pokemon_service"

    @rpc
    def get_pokemon_info(self, pokemon_id: int) -> PokemonResponse:
        try:
            response = requests.get(f"{BASE_URL}/{pokemon_id}", timeout=5)
            response.raise_for_status()

            data = response.json()
            return PokemonResponse(id=data.get("id"), moves_info=data.get("moves"))
        except requests.exceptions.HTTPError as e:
            raise errors.InvalidRequestData(e)
        except (requests.ConnectionError, requests.Timeout) as e:
            raise errors.Unavailable(e)
