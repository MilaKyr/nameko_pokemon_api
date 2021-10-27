import pytest

from app.render import MovesRender
from app.service import PokemonResponse


def test_show_moves(capsys):
    pokemon_info = PokemonResponse(id=0, moves_info=[{"move": {"name": "transform"}}])
    MovesRender(pokemon_info).show_moves()
    captured = capsys.readouterr()
    print(captured.out)
    assert (
        captured.out
        == "Moves for pokemon 0 ordered alphabetically:\n"
        + "-" * 50
        + "\n"
        + "transform \t\n"
    )
