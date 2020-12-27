from ship import Ship
from game_board import GameBoard
from player import Player

players = [Player(input('Введите имя игрока: '), 'player'),
           Player(input('Введите имя игрока-компьютера: '), 'ai')]  # Вводим имена игроков

# Создаем список объектов расставленных кораблей для игрока и компьютера
try:
    player_ships = Ship.ships_placement()
    ai_ships = Ship.ships_placement(True)
except Exception as e:
    print(f'Произошла ошибка - {e}! Перезапустите игру.')
    # raise e
else:
    # Создаем объект класса игрового поля и передаем в него списки игроков и расставленных кораблей
    game_board = GameBoard(players, player_ships, ai_ships)
    # Показываем сформированное игровое поле
    game_board.show_game_field()
    # Запускаем игровой цикл
    game_board.game_cycle()
