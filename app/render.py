import logging

from app.consts import ORDERED
from app.service import PokemonResponse


class MovesRender:
    """Prints pokemon moves in the user-friendly way"""

    def __init__(self, pokemon_info: PokemonResponse):
        self.pokemon_info = pokemon_info

    def show_moves(self) -> None:
        msg = f"Moves for pokemon {self.pokemon_info.id}"
        if ORDERED:
            self.pokemon_info.sort_moves()
            msg += " ordered alphabetically"
        print(f"{msg}:")
        print("-" * 50)
        for move in self.pokemon_info.moves_names:
            print(move, "\t")
