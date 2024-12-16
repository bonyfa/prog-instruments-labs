import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from InnerLogic import Board, GameError, Ship, Dot
from Outter_logic import Player, User, AI, Game


def test_set_dot_valid():
    """
    Тест на установку корректных координат
    """
    dot = Dot()
    dot.set_dot(2, 3)
    assert dot.get_dot() == (1, 2)


def test_set_dot_invalid():
    """
    Тест на установку некорректных координат
    """
    dot = Dot()
    with pytest.raises(GameError):
        dot.set_dot(7, 3)
    with pytest.raises(GameError):
        dot.set_dot(2, 8)


def test_get_dot():
    """
    Тест на получение координат
    """
    dot = Dot()
    dot.set_dot(4, 5)
    assert dot.get_dot() == (3, 4)


def test_ship_creation_horizontal():
    """
    Тест на создание горизонтального корабля
    """
    ship = Ship((0, 0), 3, True)
    expected_coords = [(0, 0), (0, 1), (0, 2)]
    assert ship.dots() == expected_coords


def test_ship_creation_vertical():
    """
    Тест на создание вертикального корабля
    """
    ship = Ship((0, 0), 3, False)
    expected_coords = [(0, 0), (1, 0), (2, 0)]
    assert ship.dots() == expected_coords


def test_ship_out_of_bounds():
    """
    Тест на создание корабля за пределами игрового поля
    """
    ship = Ship((5, 5), 3, True)
    with pytest.raises(GameError):
        ship.dots()


@pytest.mark.parametrize("start, length, expected", [
    ((0, 0), 2, [(0, 0), (0, 1)]),
    ((0, 0), 3, [(0, 0), (0, 1), (0, 2)]),
    ((0, 0), 4, [(0, 0), (0, 1), (0, 2), (0, 3)])
])
def test_ship_parametrized(start, length, expected):
    """
    Параметризованный тест для создания корабля разных длин
    """
    ship = Ship(start, length, True)
    assert ship.dots() == expected


def test_add_ship_valid():
    """
    Тест на добавление корабля на доску
    """
    board = Board()
    ship = Ship((1, 1), 3, True)
    ship.dots()
    spec = ship.get_specification()
    assert board.add_ship(ship.dots(), spec)


def test_add_ship_invalid():
    """
    Тест на добавление корабля на занятые координаты
    """
    board = Board()
    ship1 = Ship((1, 1), 3, True)
    ship1.dots()
    spec1 = ship1.get_specification()
    board.add_ship(ship1.dots(), spec1)
    ship2 = Ship((0, 0), 3, True)
    ship2.dots()
    spec2 = ship2.get_specification()
    assert not board.add_ship(ship2.dots(), spec2)


@pytest.mark.parametrize("shot_coord, expected", [
    ((2, 2), True),
    ((4, 4), False),
    ((6, 6), False)
])
def test_shot_parametrized(shot_coord, expected):
    """
    Параметризованный тест на выстрел по разным координатам
    """
    board = Board()
    ship = Ship((1, 1), 3, True)
    ship.dots()
    spec = ship.get_specification()
    board.add_ship(ship.dots(), spec)
    result = board.shot(shot_coord)
    assert result == expected