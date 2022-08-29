from random import sample

import pytest

from Lotto import Cart


@pytest.mark.parametrize('arg', range(5))
def test_create(arg):
    new_cart = Cart()
    eq = set()
    for item in new_cart.cart:
        eq |= set(item)
    new_cart = eq - {'#'}
    assert len(new_cart) == 15, 'Ошибка карточки'


@pytest.fixture
def fixer():
    result = Cart()
    result.cart = [sample(['#', '-'], counts=[15, 15], k=10) for _ in range(3)]
    print(result)
    return result


def test_empty(fixer):
    cart = fixer
    assert cart.is_empty, "Непустая карточка"


def test_not_empty():
    new_cart = Cart()
    assert not new_cart.is_empty, 'Пустая карточка'


@pytest.fixture
def fix1():
    cart = Cart()
    cart.cart = ['#'] * 9 + [5]
    cart.cart = [cart.cart for _ in range(3)]
    return cart


@pytest.fixture
def fix2():
    cart = Cart()
    cart.cart = ['#'] * 10
    cart.cart = [cart.cart for _ in range(3)]
    return cart


def test_number_in_list(fix1, fix2):
    assert fix1.is_num_to_cart(5), '5 не в карте'
    assert not fix2.is_num_to_cart(5), '5 в карте'


@pytest.fixture
def fix3():
    cart = Cart()
    cart.cart = [[1, 10, 20, 30, 40, 'x', 'x', 'x', 'x', 'x'],
                 [2, 11, 21, 31, 41, 'x', 'x', 'x', 'x', 'x'],
                 [3, 12, 22, 32, 42, 'x', 'x', 'x', 'x', 'x']]
    return cart


def test_find_num(fix3):
    true_cart = [[1, 10, 20, 30, 40, 'x', 'x', 'x', 'x', 'x'],
                 [2, 11, '-', 31, 41, 'x', 'x', 'x', 'x', 'x'],
                 [3, 12, 22, 32, 42, 'x', 'x', 'x', 'x', 'x']]
    fix3.cross_out(21)
    assert fix3.cart == true_cart, "Удаление цифры не работает"
