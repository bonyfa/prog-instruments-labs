import random
from random import randint, choice
class GameError(ValueError):            # класс игровой ошибки
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'Game Error, {self.message}'
        else:
            return 'Game Error has been raised!!!!'


class Dot:
    """Класс описывает базовую сущность игры "точку" с соответствующими атрибутами: координаты x и y"""

    def __init__(self):
        self.x = None
        self.y = None

    def get_dot(self) -> tuple:
        return tuple([self.x, self.y])             # преобразует координаты в кортеж

    def set_dot(self, x: int, y: int):             # проверяет координаты на принадлежность адресному пространству игрового поля
        if 1 <= x <= 6 and 1 <= y <= 6:                            # производит соответствующее смещение полученных координат на -1 с целью приведения в систему координат объектов питона
            self.x = x - 1
            self.y = y - 1
        else:
            raise GameError


class Ship:
    """Описывает класс Ship с экземляром класса корабль и атрибутами: точка начала, длина/кол-во жизней, ориентация, общими координатами, словарем спецификации(координаты: кол-во жизней)"""

    def __init__(self, start: tuple, length: int = 1, horizontal: bool = True):
        self.start = start
        self.length = length
        self.lives = length
        self.horizontal = horizontal
        self.common_coordinates = []
        self.specification = {}

    def dots(self) -> list:
        x = self.start[0]
        y = self.start[1]
        if self.horizontal and y + self.length <= 6:            #проверка на вместимость в рамках игрового поля
            for i in range(self.length):
                self.common_coordinates.append((x, y + i))      # в зависимости от ориентации и длины дополняет список координат корабля
            return self.common_coordinates
        elif not self.horizontal and x + self.length <= 6:      #проверка на вместимость в рамках игрового поля
            for i in range(self.length):
                self.common_coordinates.append((x + i, y))
            return self.common_coordinates
        else:
            raise GameError(f"Внимание, данный корабль {self.start} вне диапазона игрового поля!!!!")

    def get_specification(self) -> dict:                                #заполняет и возвращает словарь спецификации по объекту корабль {кортеж координат: кол-во жизней}
        if self.common_coordinates and self.lives:
            self.specification = {tuple(self.common_coordinates): self.lives}
        return self.specification


class Board:
 # """Класс игровой Доски, создает экземпляр игровой доски с атрибутами размерности идентификатора отрисовки, с динамическим списком всех координат живых кораблей на текущей доске и словарем характеристик жизни каждого из кораблей"""
 #    ships_template = {}     игровой шаблон для условия сравнения

    def __init__(self, m: int = 6, n: int = 6, no_hid: bool = True):
        self.field = [[" " for row in range(m)]for column in range(n)]
        self.no_hid = no_hid      # идентификатор отрисовки по умолчанию дает возможность отрисовать поле
        self.m = m
        self.n = n
        self.ships = []             # список всех координат живых кораблей на доске
        self.ships_area = []        # список координат клеток вокруг кораблей доски
        self.ships_alive = {}       # словарь с характеристикой всех кораблей

    @staticmethod
    def render_board(self):         # метод отрисовки текущей доски
        if self.no_hid:             # идентификатор отрисовки кораблей на доске
            some = 0
            print('  | 1  | 2  | 3  | 4  | 5  | 6  |')
            for i in range(6):
                some += 1
                print(
                    f'{some} | {self.field[i][0]}  | {self.field[i][1]}  | {self.field[i][2]}  | {self.field[i][3]}  | {self.field[i][4]}  | {self.field[i][5]}  |')
        else:
            for el in self.ships:
                cx, cy = el
                self.field[cx][cy] = '*'
            some = 0
            print('  | 1  | 2  | 3  | 4  | 5  | 6  |')
            for i in range(6):
                some += 1
                print(
                    f'{some} | {self.field[i][0]}  | {self.field[i][1]}  | {self.field[i][2]}  | {self.field[i][3]}  | {self.field[i][4]}  | {self.field[i][5]}  |')

    def add_ship(self, sh_coordinates: list, sh_specification: dict) -> bool:  #метод добавляет корабль на текущую доску а также проверяет возможность поставновки корабля исходя и з текущего состояния точек на доске и входящих координат
        a = tuple(sh_coordinates)
        ship_area = list(self.contour(self, a))
        if not set(ship_area).intersection(set(self.ships)) and a not in self.ships_alive.keys():
            self.ships_area += ship_area
            self.ships += sh_coordinates
            self.ships_alive.update(sh_specification)
            return True
        else:
            return False

    @staticmethod
    def contour(self, a: tuple) -> tuple:     #метод определяющий контур в диапазоне одной клетки вокруг корабля, возвращает кортеж координат всех этих клеток в рамках поля
        result = []
        for item in a:
            x, y = item
            for i in range(3):
                for j in range(3):
                    if 0 <= (x - 1 + i) <= 5 and 0 <= (y - 1 + j) <= 5:
                        result.append((x - 1 + i, y - 1 + j))
        return tuple((set(result).difference(set(a))))

    def shot(self, shot_coord: tuple):      #метод корректирует вводимые координаты выстрела а также проверяет выстрел на случай повторений, определяет статус выстрела hit, kill or miss
        a, b = shot_coord
        a -= 1
        b -= 1
        shot_coord = (a, b)
        if self.field[a][b] != "T":
            if shot_coord in self.ships:
                self.ships.remove(shot_coord)
                self.field[a][b] = 'X'
                for i in self.ships_alive.keys():
                    if shot_coord in i:
                        self.ships_alive[i] -= 1
                        if self.ships_alive[i] == 0:
                            print("Ship is killed")
                            for element in self.contour(self, i):
                                x, y = element
                                self.field[x][y] = 'T'
                            return True
                        else:
                            print('Hit the Ship')
                            return True
            else:
                print('Missed')
                self.field[a][b] = "T"
                return False
        else:
            print('Выберите другие координаты, поскольку вы уже сюда стреляли')# Требуется изменить логику поскольку она распространяется на ИИ
            return True



