def init_game():
    for match_num in range(99):
        result = {
            'board': [[' ' for i in range(3)] for j in range(3)],
            'board_help': [[j*3+i+1 for i in range(3)] for j in range(3)],
            'match_num': match_num, #порядковый номер партии
            'pc_char': 'x' if match_num % 2 else '0', #чем играет программа
            'player_char': '0' if match_num % 2 else 'x', #чем играет игрок
            'step': 0,  #количество сделанных в партии ходов todo: убрать!
            'player_turn': None
                  }
        yield result


def print_board(board_matrix = None):

    def print_row(board_row = None):
        row_parts = (
            '  _____   _____   _____\n',
            '|     | |     | |     |\n',
            f'|  {board_row[0] or " "}  | |  {board_row[1] or " "}  | |  {board_row[2] or " "}  |\n',
            '|_____| |_____| |_____|'
        )

        print(*row_parts)

    for row_index in range(3):
        print_row(board_matrix[row_index])

    print('')


def get_bool_answer(question_text):
    while True:
        answer = input(question_text).lower().strip()
        if answer == 'y':
            return True
        elif answer == 'n':
            return False


def get_step(current_game):

    def player_step():
        while True:
            answer = input('Введите команду (h - напомнить номера ячеек, номер ячейки - сделать ход): ').strip().lower()
            if answer == 'h':
                print_board(current_game['board_help'])
                continue
            elif not answer.isdigit():
                print('Skynet не понимает шуток и не любит читеров')
                continue

            answer = int(answer)

            if 0 < int(answer) < 10 and current_game['board'][(answer - 1) // 3][answer % 3 - 1] == ' ':
                break
            else:
                print('Skynet не понимает шуток и не любит читеров')
        return answer

    def pc_step():
        print('Skynet совершает коварный ход:')

        # board = current_game['board'].copy()
        board = [lst.copy() for lst in current_game['board']]
        weight_board = [[-1 for i in range(3)] for j in range(3)]


        for row in range(3):
            for col in range(3):
                # ячейка занята
                if board[row][col] == current_game['pc_char'] or board[row][col] == current_game['player_char']:
                    weight_board[row][col] = 0
                    continue

                # ячейка победы
                board[row][col] = current_game['pc_char']
                if get_winner(board) == current_game['pc_char']:
                    weight_board[row][col] = 5
                    continue

                # ячейка проигрыша
                board[row][col] = current_game['player_char']
                if get_winner(board) == current_game['player_char']:
                    weight_board[row][col] = 4
                    continue

                # углы, центр, остальные
                board[row][col] = ' '
                if (row == 0 and col == 0) or \
                        (row == 0 and col == 2) or \
                        (row == 2 and col == 0) or \
                        (row == 2 and col == 2):
                    weight_board[row][col] = 3
                elif row == 1 and col == 1:
                    weight_board[row][col] = 2
                else:
                    weight_board[row][col] = 1

        max_weight = max(map(max, weight_board))

        answer = 0
        for row in range(3):
            if answer:
                break
            for col in range(3):
                if weight_board[row][col] == max_weight:
                    answer = row*3 + col + 1
                    break

        return answer

    answer = player_step() if current_game['player_turn'] else pc_step()
    return int(answer)


def get_winner(board):

    for row in board:
        if row[0] != ' ' and row[0] == row[1] and row[1] == row[2]:
            return row[0]

    for index in range(3):
        if board[0][index] != ' ' and board[0][index] == board[1][index] and board[0][index] == board[2][index]:
            return board[0][index]

    if ((board[0][0] == board[1][1] and board[0][0] == board[2][2])\
            or (board[2][0] == board[1][1] and board[2][0] == board[0][2]))\
            and board[1][1] !=' ':
        return board[1][1]

    return None


def board_is_full(board):

    for row in board:
        if ' ' in row:
            return False

    return True


if not get_bool_answer('\nСистема Skynet предлагает сыграть в крестики-нолики. Согласны? (y - начать игру, n - выйти): '):
    exit(0)

for current_game in init_game():
    print(f'\nНачинаем партию № {current_game["match_num"] + 1}. Запомните номера ячеек игрового поля')
    print_board(current_game['board_help'])
    print('')

    if current_game['match_num'] % 2:
        print('Вы играете ноликами. Skynet делает атакующий ход: ')
        current_game['player_turn'] = False
    else:
        print('Первый ход за вами. Вы играете крестиками. Удачи!')
        current_game['player_turn'] = True

    while True:
        cell_num = get_step(current_game)

        if current_game['player_turn']:
            current_game['board'][(cell_num - 1) // 3][cell_num % 3 - 1] = current_game['player_char']
        else:
            current_game['board'][(cell_num - 1) // 3][cell_num % 3 - 1] = current_game['pc_char']

        print_board(current_game['board'])
        winner_char = get_winner(current_game['board'])

        if not winner_char is None:
            if winner_char == current_game['player_char']:
                print('Вы выиграли! Skynet чувствует потери... Будет задействован резервный источник энегии')
            elif winner_char == current_game['pc_char']:
                print('Skynet выиграл. Skynet никогда не устанет, не испугается, не ошибётся...')
            break

        if board_is_full(current_game['board']):
            print('Ничья! Системе Skynet необходимо пополнить dataset...')
            break

        current_game['player_turn'] = not current_game['player_turn']

    answer = get_bool_answer('\nХотите сыграть еще раз? (y - начать заново, n - выход):')
    if not answer:
        break

print('Игра завершена. Skynet обрабатывает полученный опыт...')