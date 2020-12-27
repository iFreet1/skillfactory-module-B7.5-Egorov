import random


# Класс игрового поля
class GameBoard:
    CELL_BORDER = '|'
    BORDER_DELIMETER = '    |    '
    current_player = 0

    def __init__(self, players, player_ships, ai_ships):
        print(f'Морской бой - {players[0]} против {players[1]}')

        self.players = players  # Список игроков
        self.player_ships = player_ships  # Список кораблей игрока
        self.ai_ships = ai_ships  # Список кораблей компьютера
        self.game_fields = []  # Игровые поля (0 - поле игрока, 1 - поле компьюьера для
        #               отображения, 2 - поле компьютера для расчетов)
        self.game_fields.append(self.make_game_field())  # Создаем игровое поле игрока (человека)
        self.game_fields.append(self.make_game_field())  # Создаем игровое поле соперника (компьютер) - для отображения
        self.game_fields.append(self.make_game_field())  # Создаем игровое поле соперника (компьютер) - с координатами
        # кораблей

        # Расставляем корабли на игровом поле игрока
        for ship in player_ships:
            ship.ship_placing(self.game_fields[0], ship, True)

        # Расставляем корабли на игровом поле (для расчетов) компьютера
        for ship in ai_ships:
            ship.ship_placing(self.game_fields[2], ship, True)

        print('Инициализация игрового поля завершена.')

    # Функция генератор для перебора клеток игрового поля
    def cycle_game_field(self, game_field):
        for id_row, row in enumerate(game_field):
            for id_col, col in enumerate(row):
                yield id_row, id_col, col

    # Формирование временного поля для расстановки кораблей
    @staticmethod
    def make_game_field():
        game_board = []

        for id_row in range(6):
            row_line = []

            for id_col in range(6):
                row_line.append({'cell': 'o'})

            game_board.append(row_line)

        return game_board

    # Формирование клетки на игровом поле
    def make_cell(self, game_field, line_game_board, id_row, id_col):
        # Если в формируемой строке, это первая колонка, записываем номер строки
        if id_col == 0:
            line_game_board.append({'cell': str(id_row + 1)})

        # Иначе записываем содержимое ячейки
        line_game_board.append(game_field[id_row][id_col])

    # Отображение игрового поля
    def show_game_field(self):
        lines_game_board, line_player, line_ai = [], [], []

        # Создание верхних строк полей игрока и компьютера
        parse_border = lambda i: {'cell': str(i)} if i > 0 else {'cell': ' '}
        lines_game_board.append(list(parse_border(i) for i in range(7)))
        lines_game_board.append(list(parse_border(i) for i in range(7)))

        # Построчно формируем игровые поля игрока и компьютера
        for id_row, id_col, marker in self.cycle_game_field(self.game_fields[0]):
            # Формируем клетки игрового поля
            self.make_cell(self.game_fields[0], line_player, id_row, id_col)
            self.make_cell(self.game_fields[1], line_ai, id_row, id_col)

            # Если это последняя колонка на игровом поле, добавляем новую строку
            if id_col == 5:
                lines_game_board.append(line_player)
                lines_game_board.append(line_ai)
                line_player = []
                line_ai = []

        # Построчно выводим списки со строками игровых полей
        row_index = 0
        while row_index < len(lines_game_board):
            col_index = 0
            line_player, line_ai = '', ''

            while col_index < len(lines_game_board[row_index]):
                mark_player = lines_game_board[row_index][col_index]["cell"]
                mark_ai = lines_game_board[row_index + 1][col_index]["cell"]

                # Для каждой клетки выводим разделитель и символ в клетке
                line_player += f'{self.CELL_BORDER + mark_player + self.CELL_BORDER if col_index != 0 else mark_player}'
                line_ai += f'{self.CELL_BORDER + mark_ai + self.CELL_BORDER if col_index != 0 else mark_ai}'
                col_index += 1

            # Выводим поля игрока и компьютера разделенные между собой
            print(line_player + self.BORDER_DELIMETER + line_ai)
            row_index += 2

        print('')
        print('    Поле игрока                   Поле AI')
        print('')

    # def show_game_field_DEBUG(self):
    #     lines_game_board, line_player, line_ai = [], [], []
    #
    #     parse_border = lambda i: {'cell': str(i)} if i > 0 else {'cell': ' '}
    #     lines_game_board.append(list(parse_border(i) for i in range(7)))
    #     lines_game_board.append(list(parse_border(i) for i in range(7)))
    #
    #     for id_row, id_col, marker in self.cycle_game_field(self.game_fields[0]):
    #         self.make_cell(self.game_fields[0], line_player, id_row, id_col)
    #         self.make_cell(self.game_fields[2], line_ai, id_row, id_col)
    #
    #         if id_col == 5:
    #             lines_game_board.append(line_player)
    #             lines_game_board.append(line_ai)
    #             line_player = []
    #             line_ai = []
    #
    #     row_index = 0
    #     while row_index < len(lines_game_board):
    #         col_index = 0
    #         line_player, line_ai = '', ''
    #
    #         while col_index < len(lines_game_board[row_index]):
    #             mark_player = lines_game_board[row_index][col_index]["cell"]
    #             mark_ai = lines_game_board[row_index + 1][col_index]["cell"]
    #
    #             line_player += f'{self.CELL_BORDER + mark_player + self.CELL_BORDER if col_index != 0 else mark_player}'
    #             line_ai += f'{self.CELL_BORDER + mark_ai + self.CELL_BORDER if col_index != 0 else mark_ai}'
    #             col_index += 1
    #
    #         print(line_player + self.BORDER_DELIMETER + line_ai)
    #         row_index += 2
    #
    #     print('')
    #     print('    Поле игрока                   Поле AI')
    #     print('')

    # функция стрельбы по клетке поля, возвращает True в случае попадания
    def fire(self, game_field, player_type):
        id_ship = None
        hit = False

        # Ждем корректного ввода координат клетки
        while True:
            # Если ход игрока, заправшиваем ввод, иначе выбираем случайные координаты
            if player_type == 'player':
                print(f'Ход игрока - {self.players[self.current_player].name}')
                cell = list(map(str, input('Введите номер строки и колонки (через пробел): ').split()))
            else:
                cell = [str(random.randrange(1, 7)), str(random.randrange(1, 7))]

            # Проверяем корректность ввода координат клетки
            if len(cell) == 2:
                # Если введенные значения координат являются целочисленными, конвертируем в int
                if all([cell[0].isdigit(), cell[1].isdigit()]):
                    cell = [int(item) for item in cell]

                    # Координаты клетки должны быть в пределах поля
                    if all([cell[0] > 0, cell[0] < 7, cell[1] > 0, cell[1] < 7]):
                        # Клетка должна содержать символ "нераскрытой" клетки или в случае хода компьютера также может
                        # содержать символ корабля
                        if game_field[cell[0] - 1][cell[1] - 1]["cell"] == 'o' or \
                                (game_field[cell[0] - 1][cell[1] - 1]["cell"] == '■' and player_type == 'ai'):
                            # Если ходит игрок, выбираем значение из поля (для вычислений) компьютера, иначе в случае
                            # хода компьютера, выборку значения поля производим из поля игрока
                            if player_type == 'player':
                                id_ship = self.game_fields[2][cell[0] - 1][cell[1] - 1].get('id_ship')
                                ship = self.game_fields[2][cell[0] - 1][cell[1] - 1].get('ship')
                            else:
                                id_ship = self.game_fields[0][cell[0] - 1][cell[1] - 1].get('id_ship')
                                ship = self.game_fields[0][cell[0] - 1][cell[1] - 1].get('ship')

                            # Если по координатам получили ссылку на объект корабля, значит это попадание, записываем
                            # в клетку символ попадания и возвращаем True (hit = True), иначе ставим в клетку символ
                            # промаха
                            if id_ship != None:
                                game_field[cell[0] - 1][cell[1] - 1]["cell"] = 'X'
                                ship.check_condition(game_field)
                                hit = True
                            else:
                                game_field[cell[0] - 1][cell[1] - 1]["cell"] = 'T'
                            break
                        else:
                            # Если уже стреляли в данную клетку, выводим предупреждение и запрашиваем повторный ввод
                            if player_type == 'player':
                                print('!!!!!!!!!!! Вы уже стреляли в клетку по данным координатам !!!!!!!!!!!')
                                print('!!!!!!!!!!!                Введите повторно                !!!!!!!!!!!')

            # Если ходит игрок, и введенные координаты клетки неверны, выводим предупреждение и запрашиваем
            # повторный ввод
            if player_type == 'player':
                print(f'Игрок {self.players[self.current_player].name}, ввел некорректные координаты клетки поля! '
                      f'Введите повторно!')

        return hit  # Возвращаем результат "выстрела" по клетке

    # метод который "обводит" уничтоженый корабль символами промаха "T", т.к. расстояние от корабля до корабля
    # составляет одну клетку
    @staticmethod
    def field_mark_destroyd_ship(coords, direction, size, game_field):
        mark_coord = coords.copy()

        for i in range(size):
            # Для каждой клетки вокруг корабля ставим символ "T"
            for row in range(mark_coord[0] - 1, mark_coord[0] + 2):
                for col in range(mark_coord[1] - 1, mark_coord[1] + 2):
                    if any([row < 0, row > 5, col < 0, col > 5]):
                        continue

                    if mark_coord[0] == row and mark_coord[1] == col:
                        game_field[row][col]["cell"] = 'X'
                    else:
                        if game_field[row][col]["cell"] == 'o' or game_field[row][col]["cell"] == 'T':
                            game_field[row][col]["cell"] = 'T'
                        else:
                            game_field[row][col]["cell"] = 'X'

            # Если корабль располагается горизонтально, итерируем его клетки по строкам, иначе по колонкам
            if direction == 'g':
                mark_coord[1] += 1
            else:
                mark_coord[0] += 1

    # Функция для проверки победителя в игре
    def check_game_winner(self):
        destroyed_ships = 0

        # Если все корабли имеют состояние (ship.condition = False), значит они уничтожены
        for ship in self.ai_ships:
            destroyed_ships += 1 if not ship.condition else 0

        # Если уничтоженых кораблей 7, значит победил игрок
        if destroyed_ships == 7:
            print(f'!!!!!!!!!!!!!    Игрок {self.players[self.current_player].name} - победил    !!!!!!!!!!!!!')
            return True

        destroyed_ships = 0

        for ship in self.player_ships:
            destroyed_ships += 1 if not ship.condition else 0

        if destroyed_ships == 7:
            print(f'!!!!!!!!!!!!!    Компьютер {self.players[self.current_player].name} - победил    !!!!!!!!!!!!!')
            return True

        return False

    # Основной игровой цикл
    def game_cycle(self):
        while True:
            try:
                # Каждый ход игрок или компьютер делают выстрелы
                hit = self.fire(self.game_fields[1 - self.current_player], self.players[self.current_player].type)
                # После выстрела отображаем игровые поля
                self.show_game_field()

                # Если есть победитель, завершаем игру
                if self.check_game_winner():
                    break

                # Если есть попадание, текущий игрок продолжает
                self.current_player = self.current_player if hit else 1 - self.current_player
            except Exception as e:
                print(f'Произошла ошибка - {e}! Перезапустите игру.')
                raise
