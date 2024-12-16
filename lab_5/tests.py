import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
from InnerLogic import Board, GameError, Ship, Dot
from Outter_logic import Player, User, AI, Game

