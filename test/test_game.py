from random import sample
import random
import os

import pytest
from faker import Faker
from mock import patch


from Lotto import Cart, PlayerComp, PlayerHuman, Game

fake = Faker('ru-RU')


@pytest.mark.parametrize('num_menu, p1, p2', (['1', PlayerHuman, PlayerComp],
                                              ['2', PlayerHuman, PlayerHuman],
                                              ['3', PlayerComp, PlayerComp]))
def test_start(num_menu, p1, p2):
    with patch('builtins.input', lambda x: num_menu):
        game = Game()
        assert isinstance(game.player1, p1) and isinstance(game.player2, p2), \
            f'Ошибка определения игроков в {num_menu} пункте'


@pytest.fixture
def fix5():
    p1 = PlayerComp()
    p1.name = 'First'
    p1.cart = Cart()
    p1.cart.cart = [['#', '#', '#', 30, '#', '#', '#', '#', '#', '#'],
                    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]
    p2 = PlayerComp()
    p2.name = 'Second'
    p2.cart = Cart()
    p2.cart.cart = [['#', '#', 20, '#', '#', '#', '#', '#', '#', '#'],
                    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]
    with patch('builtins.input', lambda x: '3'):
        game = Game()
    game.player1 = p1
    game.player2 = p2
    return game


@pytest.mark.parametrize('num, ans, not_ans', ([30, 'First', 'Second'], [20, 'Second', 'First']))
def test_exit(fix5, num, ans, not_ans):
    fix5.bag = [num]
    fix5.start()
    assert fix5.winner == ans and fix5.loser == not_ans, 'Ошибка результата'
