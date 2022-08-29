from random import sample  # выбор случайного набора
from collections import defaultdict  # объявление словаря со значениями нужного типа

from faker import Faker  # объявление типа для фиксации случайных имен


fake = Faker('ru-RU')  # объект класса с русским набор имен


def define_cart(new_cart):
    """
    Получает карту, и возвращает множество номеров из нее.
    :param new_cart: карта с номерами.
    :return: множество номеров карты
    """
    eq = set()
    for item in new_cart:
        eq |= set(item)
    new_cart = eq - {'#', '-'}
    return new_cart


class Cart:
    """
    класс для карты
    """
    def __init__(self):
        self.cart = None
        self.create()

    def create(self):
        """
        Задание содержимого карточки 15 уникальных номеров от 1 до 100
        :return: задание свойства cart, как лист из 3 строк
        """
        self.cart = sorted(sample(list(range(1, 100)), k=15))
        app = defaultdict(list)
        for item in self.cart:
            app[item // 10].append(item)
        # создает словарь со значениями из трехэлементных листов из заданных цифр, а остальное добавляется символами "#"
        for i in range(10):
            if len(app[i]) > 3:
                k = len(app[i]) - 3
                app[i] = app[i][:3]
                j = 1
                bag = set(app[(i + j) % 10]) - set('#')
                while len(bag) >= 3:
                    j += 1
                    bag = set(app[(i + j) % 10]) - set('#')
                new_set = list(set(range(((i + j) * 10) % 100, ((i + j + 1) * 10) % 101)) - bag)
                app[(i + j) % 10] = list(set(app[(i + j) % 10]) - set('#')) + sample(new_set, k=k)
                k = 3 - len(app[(i + j) % 10])
                app[(i + j) % 10] += ['#'] * k
            elif len(app[i]) < 3:
                k = 3 - len(app[i])
                app[i] += ['#'] * k
        result = []
        # превращает из словаря в список по 10 элементов
        for i in range(3):
            result.append([app[key][i] for key in range(10)])
        self.cart = result

    @property
    def is_empty(self):
        """
        Проверка на отсутствие цифр в карточке.
        :return: bool
        """
        return len(define_cart(self.cart)) == 0

    def is_num_to_cart(self, num):
        """
        Проверка присутствия номера в карточке
        :param num: искомый номер
        :return: bool
        """
        return any([item.count(num) for item in self.cart])

    def cross_out(self, num):
        """
        Замена числа в карточке на символ "-"
        :param num: номер для поиска.
        :return: все изменения производятся в картоке
        """
        for item in self.cart:
            try:
                index = item.index(num)
                item[index] = '-'
                break
            except ValueError:
                pass

    def __str__(self):
        """
        Подготовка карточки для вывода на экран.
        :return: стока для вывода
        """
        s = ' ' + '_' * 30 + '\n'
        for item in self.cart:
            s += '|'
            for char in item:
                s += f'{str(char):^3}'
            s += '|\n'
        s += ' ' + '-' * 30 + '\n'
        return s

    def __eq__(self, other):
        if isinstance(other, Cart):
            cart1 = define_cart(self.cart)
            cart2 = define_cart(other.cart)
            return len(cart1) == len(cart2) and cart1 == cart2


class PlayerComp:
    """
    Класс для бота
    """
    def __init__(self):
        """
        Инициализируются два свойства карта игрока и его имя - генерируется автоматически
        """
        self.cart = Cart()
        self.name = fake.name()
        print(f'Имя игрока: {self.name}')

    def step(self, num):
        """
        Ход игрока
        :param num: номер бочонка
        :return: bool
        """
        print(self.cart)
        if self.cart.is_num_to_cart(num):
            self.cart.cross_out(num)
            print('Номер есть')
        else:
            print('Номера нет в карточке')
        return True


class PlayerHuman:
    """
    Ход игрока с переопределением методов.
    """
    def __init__(self):
        self.cart = Cart()
        self.name = input('Введите имя игрока: ')
        print(f'Имя игрока: {self.name}')

    def step(self, num):
        print(self.cart)
        ans = input('Зачеркнуть цифру (Д/Н)? ')
        while ans not in 'ДдНн':
            ans = input('Некорректный ввод. Зачеркнуть цифру (Д/Н)? ')
        if ans in 'Дд':
            if self.cart.is_num_to_cart(num):
                self.cart.cross_out(num)
                return True
            else:
                return False
        else:
            if self.cart.is_num_to_cart(num):
                return False
            else:

                return True


class Game:
    """
    Класс игры, свойство bag - мешок с бочонками
    """
    bag = list(range(1, 100))

    def __init__(self):
        """
        Инициация игроков
        """
        self.player1 = None
        self.player2 = None
        self.exit = self.menu()
        self.winner = None
        self.loser = None

    def menu(self):
        """
        Вывод меню и получение номера выбранного пункта.
        :return: номер пункта
        """
        mtext = """

        1. Один игрок с компьютером
        2. 2 игрока
        3. 2 Компьютера
        4. Выход

        """
        print(mtext)
        n = input('Введите номер пункта: ')
        while n not in '1234':
            n = input('Некорректный ввод. Введите номер пункта: ')
        if n == '1':
            self.player1 = PlayerHuman()
            self.player2 = PlayerComp()
        elif n == '2':
            self.player1 = PlayerHuman()
            self.player2 = PlayerHuman()
        elif n == '3':
            self.player1 = PlayerComp()
            self.player2 = PlayerComp()
        else:
            print('Выбран выход')
            return True
        return False

    def start(self):
        """
        Процесс игры
        """
        step1, step2 = False, False
        num = sample(self.bag, k=1)
        print(f'Выпал бочонок: {num[0]}')
        self.bag.remove(num[0])
        while not (self.player1.cart.is_empty or self.player2.cart.is_empty):
            step1 = self.player1.step(num[0])
            step2 = self.player2.step(num[0])
            if not (step1 and step2 and len(self.bag)):
                break
            num = sample(self.bag, k=1)
            print(f'Выпал бочонок: {num[0]}')
            self.bag.remove(num[0])
        if self.player1.cart.is_empty or not step1:
            self.winner = self.player1.name
            self.loser = self.player2.name
        elif self.player2.cart.is_empty or not step2:
            self.loser = self.player1.name
            self.winner = self.player2.name
        else:
            print('Все бочонки вынуты')
            return
        print()
        print("_" * 40)
        print(f"Победитель: {self.winner}")
        print("_" * 40)
        print(f'{self.loser} сегодня не выиграл')


if __name__ == '__main__':
    # запуск игры
    game = Game()
    if not game.exit:
        game.start()
