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
from app.render import print_pokemon_moves
from app.utils import check_input


logging.basicConfig(level=logging.WARNING)


if __name__ == "__main__":
    successful_input = False
    while not successful_input:
        try:
            id_to_check = input("Enter a number as integer: ")
            pokemon_id = check_input(id_to_check)
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
