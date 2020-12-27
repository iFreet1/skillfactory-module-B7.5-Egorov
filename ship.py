import random
from game_board import GameBoard


# Класс кораблей
class Ship:
    def __init__(self, id_ship, coords, direction, size):
        self.id_ship = id_ship      # Идентификатор корабля
        self.coords = coords        # Начальные координаты корабля
        self.direction = direction  # Направление расположения корабля на поле (горизонтальное или вертикальное)
        self.size = size            # Размер корабля
        self.condition = True       # Корабль не уничтожен

    # Функция проверки ввода координат и направления корабля на поле
    @staticmethod
    def check_correct_input(input_data, directing=False):
        result = False

        # Если фаза ввода координат корабля, проверяем их корректность, иначе проверяем корректность ввода направления
        if not directing:
            while True:
                try:
                    x = int(input_data[0])
                    y = int(input_data[1])

                    if all([x > 0, y > 0]):
                        input_data[0] = x - 1
                        input_data[1] = y - 1
                        break
                    else:
                        input_data = input(
                            'Введено некорректное значение координат корабля на поле! Введите повторно: ').split()
                except ValueError as e:
                    input_data = input(
                        'Введено некорректное значение координат корабля на поле! Введите повторно: ').split()
                else:
                    result = True
                    break
        else:
            while True:
                if any([input_data == 'g', input_data == 'v']):
                    break
                else:
                    input_data = input('Введено некорректное значение расположения корабля на поле! Введите повторно: ')

        return input_data

    # Функция попытки расположить корабль на игровом поле
    def ship_placing(self, board_field, ship, auto_placement):
        test_coord = ship.coords.copy()  # Копируем начальные координаты корабля

        # проверяем каждую клетку корабля на поле
        for cell in range(ship.size):
            # Корабль не должен выходить за пределы игрового поля
            if any([test_coord[0] < 0, test_coord[0] > 5, test_coord[1] < 0, test_coord[1] > 5]):
                if not auto_placement:
                    print('Данное расположение корабля невозможно! Введите повторно...')
                return False

            # Проверяем не находится ли корабль слишком близко к другому кораблю
            # Расстояние не должно быть меньше клетки
            for row in range(test_coord[0] - 1, test_coord[0] + 2):
                for col in range(test_coord[1] - 1, test_coord[1] + 2):
                    if any([row < 0, row > 5, col < 0, col > 5]):
                        continue

                    if board_field[row][col]["cell"] == '■' and ship.id_ship != board_field[row][col].get('id_ship'):
                        if not auto_placement:
                            print('Корабль находится слишком близко к другому кораблю! Введите повторно...')
                        return False

            # Если текущую клетку корабля можно расположить на поле, помечаем её символом и записываем ссылку
            # на объект корабля
            board_field[test_coord[0]][test_coord[1]]["cell"] = '■'
            board_field[test_coord[0]][test_coord[1]]["id_ship"] = ship.id_ship
            board_field[test_coord[0]][test_coord[1]]["ship"] = ship

            # Если корабль располагается горизонтально, итерируем его клетки по строкам, иначе по колонкам
            if ship.direction == 'g':
                test_coord[1] += 1
            else:
                test_coord[0] += 1

        return True

    # Функция расстановки кораблей игрока и компьютера на игровых полях
    @staticmethod
    def ships_placement(ai=False):
        # Если расставляет игрок, предлагаем ему, расставить корабли автоматически
        if not ai:
            while True:
                auto_placement = input('Расставить корабли автоматически? (y - да, n - нет)')

                if auto_placement == 'y':
                    auto_placement = True
                    break
                elif auto_placement == 'n':
                    auto_placement = False
                    break
                else:
                    print('Команда не распознана, введите повторно!')
        else:
            auto_placement = True   # Если расставляет компьютер, делаем расстановку автоматически

        # Процедура быстрого отображения игрового поля во время расстановки кораблей
        def show_quick_board():
            parse_border = lambda i: f'|{i}|' if i > 0 else '  '
            border_game_board = list(parse_border(i) for i in range(7))

            if not auto_placement:
                print(*border_game_board, sep='')

            for id_row, row in enumerate(data_game_board):
                row_line = ''

                for id_col, col in enumerate(row):
                    if id_col == 0:
                        row_line += str(id_row + 1) + ' '

                    row_line += f'|{col["cell"]}|'

                if not auto_placement:
                    print(row_line)

        # Список содержащий словари с данными кораблей (идентификатор, размер и название)
        ships = ({'id_ship': 0, 'size': 3, 'name': 'Трехпалубный'}, {'id_ship': 1, 'size': 2, 'name': 'Двухпалубный'},
                 {'id_ship': 2, 'size': 2, 'name': 'Двухпалубный'}, {'id_ship': 3, 'size': 1, 'name': 'Однопалубный'},
                 {'id_ship': 4, 'size': 1, 'name': 'Однопалубный'}, {'id_ship': 5, 'size': 1, 'name': 'Однопалубный'},
                 {'id_ship': 6, 'size': 1, 'name': 'Однопалубный'})
        result = []

        except_coords = []  # Клетки которые надо исключить при автоматической расстановке
        free_ships = 7      # Число нерасставленных кораблей

        # Цикл пока не будут расставлены все корабли
        while len(result) < 7:
            data_game_board = GameBoard.make_game_field()   # Создаем временное игровое поле

            # Показываем поле для расстановки кораблей только если делаем это вручную
            if not auto_placement:
                show_quick_board()

            # Проходим по списку кораблей и производим расстановку
            for ship in ships:
                ship_placed = False                     # Флаг обозначающий, что корабль установлен на поле
                random_step_x, random_step_y = 1, 1     # Шаг для случайной расстановки кораблей

                # Пока корабль не будет успешно установлен на поле и клетки "исключения" не заполнят всё игровое поле
                # продолжаем попытки установить корабль на поле
                while not ship_placed and len(except_coords) < 36:
                    # Если расставляем корабли вручную, запрашиваем ввод координат и направления корабля
                    if not auto_placement:
                        print(f'Введите позицию и расположение (вертикальное или горизонтальное) для - {ship["name"]}')
                        coords = Ship.check_correct_input(input('Введите координаты на поле (через пробел): ').split())
                        direction = Ship.check_correct_input(
                            input('Введите расположение на поле (g - горизонтальный | v - '
                                  'вертикальный): '), True)
                    else:
                        # Иначе, если расстановка происходит автоматически
                        while True:
                            # Пока нерасставленых кораблей больше 3, выбираем случайные координаты на поле
                            if free_ships > 3:
                                coords = [random.randrange(0, 7, random_step_x), random.randrange(0, 7, random_step_y)]
                                random_step_x = random.randrange(1, 7)
                                random_step_y = random.randrange(1, 7)

                                random_step_x = 1 if random_step_x > 6 else random_step_x + 1
                                random_step_y = 1 if random_step_y > 6 else random_step_y + 1

                                if not coords in except_coords:
                                    break
                            else:
                                # Если осталось три или меньше нерасставленных корабля, проходим по каждой клетке
                                # на поле (кроме клеток "исключений") и пытаемся поставить корабли в данные клетки
                                coords = []

                                for id_row, row in enumerate(data_game_board):
                                    for id_col, col in enumerate(row):
                                        if not [id_row, id_col] in except_coords:
                                            except_coords.append([id_row, id_col])
                                            coords = [id_row, id_col]
                                            break
                                    if coords:
                                        break
                                if coords:
                                    break

                        # Выбираем случайное направление корабля (горизонтальное или вертикальное)
                        direction = 'g' if random.randrange(1, 3) == 1 else 'v'

                    # Создаем временный объект корабля
                    temp_ship = Ship(ship["id_ship"], coords, direction, ship["size"])
                    # Пробуем разместить корабль на временном игровом поле
                    ship_placed = temp_ship.ship_placing(data_game_board, temp_ship, auto_placement)

                # В случае если клетки "исключения" заняли всё поле и расставлены не все корабли, начинаем
                # расстановку заново
                if len(except_coords) == 36 and len(result) < 7:
                    except_coords = []
                    result = []
                    free_ships = 7
                    break

                # После каждого успешного шага установки корабля убавляем число нерасставленных кораблей, добавляем
                # установленый корабль в результирующий список и показываем временное игровое поле
                free_ships -= 1
                result.append(temp_ship)
                show_quick_board()

        return result   # возвращаем список хранящий ссылки на объекты расставленных кораблей

    # Проверка состояния корабля
    def check_condition(self, game_field):
        hits = 0                            # Число попаданий по кораблю
        check_coord = self.coords.copy()    # Копируем начальные координаты корабля

        # Проходим по каждой клетке корабля
        for i in range(self.size):
            # Если в клетке стоит символ попадания "X", увеличиваем счетчик попаданий по кораблю
            if game_field[check_coord[0]][check_coord[1]]["cell"] == 'X':
                hits += 1

            # Если корабль располагается горизонтально, итерируем его клетки по строкам, иначе по колонкам
            if self.direction == 'g':
                check_coord[1] += 1
            else:
                check_coord[0] += 1

        # Если попадания по кораблю равны его размеру, значит корабль уничтожен
        if hits == self.size:
            GameBoard.field_mark_destroyd_ship(self.coords, self.direction, self.size, game_field)
            self.condition = False
            print('')
            print('!!!!!!!!!!!     Корабль уничтожен     !!!!!!!!!!!')
            print('')