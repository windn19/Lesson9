from random import sample
from collections import defaultdict

from faker import Faker


fake = Faker('ru-RU')


def define_cart(new_cart):
    eq = set()
    for item in new_cart:
        eq |= set(item)
    new_cart = eq - {'#', '-'}
    return new_cart


class Cart:
    def __init__(self):
        self.cart = None
        self.create()

    def create(self):
        self.cart = sorted(sample(list(range(1, 100)), k=15))
        app = defaultdict(list)
        for item in self.cart:
            app[item // 10].append(item)
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
        for i in range(3):
            result.append([app[key][i] for key in range(10)])
        self.cart = result

    @property
    def is_empty(self):
        return len(define_cart(self.cart)) == 0

    def is_num_to_cart(self, num):
        return any([item.count(num) for item in self.cart])

    def cross_out(self, num):
        for item in self.cart:
            try:
                index = item.index(num)
                item[index] = '-'
                break
            except ValueError:
                pass

    def out_print(self):
        s = ' ' + '_' * 30 + '\n'
        for item in self.cart:
            s += '|'
            for char in item:
                s += f'{str(char):^3}'
            s += '|\n'
        s += ' ' + '-' * 30 + '\n'
        return s


class PlayerComp:
    def __init__(self):
        self.cart = Cart()
        self.name = fake.name()
        print(f'Имя игрока: {self.name}')

    def step(self, num):
        print(self.cart.out_print())
        if self.cart.is_num_to_cart(num):
            self.cart.cross_out(num)
            print('Номер есть')
        else:
            print('Номера нет в карточке')
        return True


class PlayerHuman:
    def __init__(self):
        self.cart = Cart()
        self.name = input('Введите имя игрока: ')
        print(f'Имя игрока: {self.name}')

    def step(self, num):
        print(self.cart.out_print())
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
    bag = list(range(1, 100))

    def __init__(self):
        self.player1 = None
        self.player2 = None

    def menu(self):
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
        return int(n)

    def start(self):
        n = self.menu()
        if n == 1:
            self.player1 = PlayerHuman()
            self.player2 = PlayerComp()
        elif n == 2:
            self.player1 = PlayerHuman()
            self.player2 = PlayerHuman()

        elif n == 3:
            self.player1 = PlayerComp()
            self.player2 = PlayerComp()
        else:
            print('Выбран выход')
            return None
        num = sample(self.bag, k=1)
        print(f'Выпал бочонок: {num[0]}')
        self.bag.remove(num[0])
        while not (self.player1.cart.is_empty or self.player2.cart.is_empty):
            step1 = self.player1.step(num[0])
            step2 = self.player2.step(num[0])
            if not step1 or not step2:
                break
            num = sample(self.bag, k=1)
            print(f'Выпал бочонок: {num[0]}')
            self.bag.remove(num[0])
        if self.player1.cart.is_empty or not step1:
            loser = self.player1
            winner = self.player2
        else:
            loser = self.player1
            winner = self.player2
        print()
        print("_"*40)
        print(f"Победитель: {winner.name}")
        print("_"*40)
        print(f'{loser.name} сегодня не выиграл')


if __name__ == '__main__':
    game = Game()
    game.start()
