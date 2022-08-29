import pytest
import mock

from Lotto import PlayerComp, Cart, PlayerHuman


@pytest.fixture
def fix3():
    cart = Cart()
    cart.cart = [[1, 10, 20, 30, 40, '#', '#', '#', '#', '#'],
                 [2, 11, 21, 31, 41, '#', '#', '#', '#', '#'],
                 [3, 12, 22, 32, 42, '#', '#', '#', '#', '#']]
    return cart


def test_comp_step(fix3):
    human = PlayerComp()
    human.cart = fix3
    assert human.step(10), 'Error step'
    print(human.cart.out_print())
    assert human.step(51) is True, 'OverTime'


@pytest.mark.parametrize('num, y, result', ([21, 'д', True], [21, 'н', False], [51, 'д', False], [51, 'н', True]))
def test_human_step(fix3, num, y, result):
    with mock.patch('builtins.input', lambda x: y):
        human = PlayerHuman()
        human.cart = fix3
        assert human.step(num) is result, 'Error'


@pytest.fixture
def fix4():
    cart = Cart()
    cart.cart = [[1, 14, 22, 32, 40, 51, '#', 76, 86, 95],
                 ['#', '#', 29, 33, 41, 53, '#', '#', '#', '#'],
                 ['#', '#', '#', '#', 43, 52, '#', '#', '#', '#']]
    return cart


def test_comp_step1(fix4):
    test_cart = [[1, 14, 22, '-', 40, 51, '#', 76, 86, 95],
                 ['#', '#', 29, 33, 41, 53, '#', '#', '#', '#'],
                 ['#', '#', '#', '#', 43, 52, '#', '#', '#', '#']]
    comp = PlayerComp()
    comp.cart = fix4
    comp.step(32)
    assert comp.cart.cart == test_cart, 'Error'
    comp.step(34)
    assert comp.cart.cart == test_cart, 'Error'


def test_comp_num(fix4):
    comp = PlayerComp()
    comp.cart = fix4
    assert comp.cart.is_num_to_cart(32), "Есть номер"
    assert not comp.cart.is_num_to_cart(34), "Нет номера"
