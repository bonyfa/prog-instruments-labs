import InnerLogic
from InnerLogic import *
import random
from random import randint, choice
import time
from time import sleep

class Player:               #базовый класс-родитель для двух игроов
    def __init__(self, name: str):  #инициализация по имени игрока
        self.name = name

    def ask(self):          # пустой метод, он будет переопределен у наследников
        pass

    def move(self) -> bool:         # метод делающий ход в игре посредством вызова метода ask()
        try:
            while True:
                if not self.ask():
                    print('end')
                    break
        except GameError as e:
            print('error')
            return False


class User(Player):                     # класс игрока определен своими свойствами: своей доски и доски противника
    def __init__(self, name='Player'):
        super().__init__(name)
        self.home_board = Board(no_hid=False)
        self.enemy_board = None
        self.x = None
        self.y = None

    def ask(self, enemy_board) -> bool:                 # переопределенный метод класса-родителя запрашивает координаты для выстрела проводит проверку на диапазон и тип вводимых координат в случае необходимости выбрасывает GameError
        self.enemy_board = enemy_board
        print('input x coordinates')
        self.x = int(input())
        print('input y coordinates')
        self.y = int(input())
        if type(self.y) is not int or type(self.x) is not int:
            raise GameError
        elif 1 <= self.x <= 6 and 1 <= self.y <= 6:
            return self.enemy_board.shot((self.x, self.y))
        else:
            raise GameError


class AI(Player):      # класс ИИ self.used_shot_coord список координат совершенных выстрелов
    def __init__(self, name='AI'):
        super().__init__(name)
        self.home_board = Board(no_hid=True)
        self.enemy_board = None
        self.x = None
        self.y = None
        self.used_shot_coord = []

    def ask(self, enemy_board) -> bool:         # преопределенный метод класса-родителя с помощью генератора случайного выбора из shoot_coord производит выстрел
        self.enemy_board = enemy_board
        field_coord = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                       (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                       (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
        bad_coord = set(self.used_shot_coord)
        shoot_coord = list(set(field_coord).difference(bad_coord))
        self.x, self.y = random.choice(shoot_coord)
        self.used_shot_coord.append((self.x, self.y))
        return self.enemy_board.shot((self.x, self.y))


class Game:         # класс игры init_success переменная статуса инициализации досок игроков
    def __init__(self):
        self.init_success = False
        self.user1 = None
        self.user2 = None

    def start(self):            # метод начала игры инициализирует ввод имении, создания экземпляров соответствующих классов игроков
        self.greet()
        print('Игрок, введите свое имя:')
        player_name = input()
        if player_name:
            self.user1 = User(name=player_name)
            self.user2 = AI()
            while not self.init_success:
                print(f'{self.user1.name} board initialization')
                self.random_board(some_user=self.user1.home_board, user_name=self.user1.name)
            else:
                while not self.random_board(some_user=self.user2.home_board, user_name=self.user2.name):
                    print(f'{self.user2.name} board initialization')
                else:
                    print('Доски сформированы игра началась')
                    self.loop()
    def random_board(self, some_user, user_name: str) -> bool: # метод случайной постановки кораблей на доску, инициализация доски игроков
        field_coord = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                       (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                       (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
        quantity_ships_template = [3, 2, 2, 1, 1, 1, 1]
        len_iter = 0
        while len(some_user.ships) < 11:
                for iter in quantity_ships_template:
                    r_result = False
                    while not r_result:
                        if len_iter < 100:
                            bad = set(some_user.ships).union(set(some_user.ships_area))
                            clear_points = list(set(field_coord).difference(bad))
                            try:
                                rnd_x, rnd_y = random.choice(clear_points)
                                rnd_horizontal = random.randint(0, 1)
                                dot = Dot()
                                dot.set_dot(int(rnd_x), int(rnd_y))
                                ship = Ship(dot.get_dot(), iter, horizontal=rnd_horizontal)
                                r_result = some_user.add_ship(ship.dots(), ship.get_specification())
                                len_iter += 1
                            except GameError:
                                len_iter += 1
                                r_result = False
                        else:
                            some_user.ships = []
                            some_user.ships_area = []
                            some_user.ships_alive = {}
                            break
                if sum(some_user.ships_alive.values()) == 11:
                    print(f'{user_name}s board')
                    some_user.render_board(some_user)
                    self.init_success = True
                    return True
                else:
                    self.init_success = False
                    return False

    def greet(self):
        print('Приветствуем вас в игре!!!')
        print('_______________________________________________________________________________________________________________________')
        print(' После инициализации будут сформированы 2 доски: ваша и противника')
        print('_______________________________________________________________________________________________________________________')
        print(' координаты выстрела вводятся поочередно в формате х и у, ИЗБЕГАЙТЕ ввода НЕ ЧИСЛОВЫХ значений поскольку будет выведена ошибка')
        print('_______________________________________________________________________________________________________________________')
        print('ход компьютера осуществляется с задержкой в несколько секунд')

    def loop(self): #метод игрового цикла
        print('____________________________________________________')
        win_resul = False
        player_counter = 1
        while not win_resul:
            try:
                print('____________________________________________________')
                if player_counter % 2 != 0:
                    print(f'{self.user1.name}, Ваш ход:')
                    if self.user1.ask(self.user2.home_board):
                        pass
                    else:
                        player_counter += 1
                    Board.render_board(self.user1.enemy_board)
                    if len(self.user1.enemy_board.ships) == 0:
                        print('You WINN!!!')
                        win_resul = True
                else:
                    sleep(2)
                    print(f'Ходит {self.user2.name}:')
                    if self.user2.ask(self.user1.home_board):
                        pass
                    else:
                        player_counter += 1
                    Board.render_board(self.user2.enemy_board)
                    if len(self.user2.enemy_board.ships) == 0:
                        print('AI WINN!!!')
                        win_resul = True
            except ValueError:
                print("Ошибка ввода координат введите их заново")



