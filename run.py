import sys
import logging

from app.errors import (
    ValueTooSmall,
    InvalidValueType,
    ValueTooBig,
    Unavailable,
    InvalidRequestData,
    InvalidResponseData,
)
from app.service import PokemonService
from app.render import MovesRender
from app.utils import check_if_float, check_range, check_if_int


logging.basicConfig(level=logging.WARNING)


def print_pokemon_moves(for_id: int) -> None:
    pokemon_info = PokemonService().get_pokemon_info(for_id)
    MovesRender(pokemon_info).show_moves()


if __name__ == "__main__":
    successful_input = False
    while not successful_input:
        try:
            id_to_check = input("Enter a number as integer: ")
            id_converted_to_float = check_if_float(id_to_check)
            pokemon_id = check_if_int(id_converted_to_float)
            check_range(pokemon_id)
            successful_input = True
        except (ValueTooSmall, ValueTooBig, InvalidValueType) as e:
            logging.warning(f"{e}. Try again! \t")
        except EOFError as e:
            logging.warning("Stopping the program")
            sys.exit()
        else:
            try:
                print_pokemon_moves(pokemon_id)
            except (InvalidRequestData, InvalidResponseData) as e:
                logging.critical(e)
                sys.exit()
            except Unavailable as e:
                logging.critical("Server is unavailable, please try again later")
                sys.exit()
