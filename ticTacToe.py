import random
import os

"""
Box characters for the layout of the Tic Tac Toe board
https://en.wikipedia.org/wiki/Box-drawing_character
https://www.copyandpastesymbols.net/line-symbols.html

Strategy used for the computer
https://en.wikipedia.org/wiki/Tic-tac-toe
"""


def clear_terminal():
    # 'nt' == windows
    _ = os.system('cls') if os.name == 'nt' else os.system('clear')


def display_board(positions):
    clear_terminal()
    print(f"""
\t                    
\t    {positions[6]}  │  {positions[7]}  │  {positions[8]}  
\t  ─────┼─────┼─────
\t    {positions[3]}  │  {positions[4]}  │  {positions[5]}  
\t  ─────┼─────┼─────
\t    {positions[0]}  │  {positions[1]}  │  {positions[2]}  
\t                    
"""
          )


def valid_position_on_the_board(board_positions):
    return ' ' in board_positions


def computer_turn(board_positions, all_current_position_on_board: dict, shape='O'):
    if len(all_current_position_on_board['X']) == 0 and len(all_current_position_on_board['O']) == 0:  # First move
        if board_positions[4] == ' ':  # if center is empty
            board_positions[4] = 'O'
            display_board(board_positions)
            return board_positions, 4, shape  # return updated positions

    # Finding all possible moves
    all_possible_moves = [index for index, value in enumerate(board_positions) if value == ' ']

    # Checking if computer can win the game in the next turn
    for each_move in all_possible_moves:
        board_positions_copy = board_positions.copy()
        all_current_position_on_board_copy = {'O': all_current_position_on_board['O'].copy()}

        board_positions_copy[each_move] = 'O'
        all_current_position_on_board_copy['O'].append(each_move)

        computer_won_game, which_player = game_status(all_current_position_on_board_copy, shape='O')
        if computer_won_game:
            board_positions[each_move] = 'O'
            display_board(board_positions)
            return board_positions, each_move, shape

    # Checking if player can win the game in the next turn
    for each_move in all_possible_moves:
        board_positions_copy = board_positions.copy()
        all_current_position_on_board_copy = {'X': all_current_position_on_board['X'].copy()}

        board_positions_copy[each_move] = 'X'
        all_current_position_on_board_copy['X'].append(each_move)

        player_won_game, which_player = game_status(all_current_position_on_board_copy, shape='X')
        if player_won_game:
            board_positions[each_move] = 'O'
            display_board(board_positions)
            return board_positions, each_move, shape

    # Checking if computer can fork
    # TODO - add fork for computer

    # Checking if player is forking, block it
    for corner in [0, 2, 6, 8]:
        if board_positions[corner] == 'X' and board_positions[4] == 'O':
            if 1 in all_possible_moves or 3 in all_possible_moves or 5 in all_possible_moves or 7 in all_possible_moves:
                edge_available = [x for x in all_possible_moves if x in [1, 3, 5, 7]]
                pos = random.choice(edge_available)
                board_positions[pos] = 'O'
                display_board(board_positions)
                return board_positions, pos, shape  # return updated positions

    # Check if the center is available, if yes, play center
    if board_positions[4] == ' ':
        board_positions[4] = 'O'
        display_board(board_positions)
        return board_positions, 4, shape  # return updated positions

    # Check if user played corner, play opposite corner if available
    for p in all_current_position_on_board['X']:
        #     0 = 8     2 = 6
        if p == 0 and board_positions[8] == ' ':
            board_positions[8] = 'O'
            display_board(board_positions)
            return board_positions, 8, shape  # return updated positions
        elif p == 8 and board_positions[0] == ' ':
            board_positions[0] = 'O'
            display_board(board_positions)
            return board_positions, 0, shape  # return updated positions
        elif p == 2 and board_positions[6] == ' ':
            board_positions[6] = 'O'
            display_board(board_positions)
            return board_positions, 6, shape  # return updated positions
        elif p == 6 and board_positions[2] == ' ':
            board_positions[2] = 'O'
            display_board(board_positions)
            return board_positions, 2, shape  # return updated positions

    # Play corner if available
    if 0 in all_possible_moves or 2 in all_possible_moves or 6 in all_possible_moves or 8 in all_possible_moves:
        while True:
            corner = random.choice(all_possible_moves)
            if corner in [0, 2, 6, 8]:
                board_positions[corner] = 'O'
                display_board(board_positions)
                return board_positions, corner, shape  # return updated positions

    # Play empty edge
    edge = random.choice([1, 3, 5, 7])
    board_positions[edge] = 'O'
    display_board(board_positions)
    return board_positions, edge, shape  # return updated positions


def player_turn(board_positions, shape='X'):
    while True:
        try:
            player_input = int(input(f"Enter position ({shape}): "))
        except ValueError:
            print("Not a position on the board, try again!")
            continue
        if not 0 < player_input <= 9:
            print("Not a position on the board, try again!")
            continue
        if board_positions[player_input - 1] == ' ':
            # Placing position on the board
            board_positions[player_input - 1] = shape
            display_board(board_positions)
            return board_positions, player_input - 1, shape  # return new board positions
        else:
            print("Invalid position, it is already taken")


def game_status(players_location: dict, shape='X'):
    all_possible_winning_scenario = (
        (6, 3, 0), (7, 4, 1), (8, 5, 2),  # Vertical
        (6, 7, 8), (3, 4, 5), (0, 1, 2),  # Horizontal
        (6, 4, 2), (8, 4, 0)  # Diagonal
    )
    # Did someone win the game?
    for x in all_possible_winning_scenario:
        if all(y in players_location[shape] for y in x):  # TODO - Learn this line
            return True, shape
    return False, shape


def one_player_game(x_starts):
    board_positions = [' ' for _ in range(9)]
    all_players_position_on_board = {'X': [], 'O': []}
    display_board(board_positions)
    while True:
        if x_starts:
            # Player one turn 
            board_positions, player_index, player_shape = player_turn(board_positions)
            all_players_position_on_board[player_shape].append(player_index)

            # Status of the game
            won_game, which_player = game_status(all_players_position_on_board)
            if won_game:
                return which_player

            # is there any empty position on the board?
            if not valid_position_on_the_board(board_positions):
                return False

            # Computer turn
            board_positions, computer_index, computer_shape = computer_turn(board_positions, all_players_position_on_board)
            all_players_position_on_board[computer_shape].append(computer_index)

            # Status of the game
            won_game, which_player = game_status(all_players_position_on_board, shape='O')
            if won_game:
                return which_player
        else:  # 'O' starts first
            board_positions, computer_index, computer_shape = computer_turn(board_positions, all_players_position_on_board)
            all_players_position_on_board[computer_shape].append(computer_index)

            # Status of the game
            won_game, which_player = game_status(all_players_position_on_board, shape='O')
            if won_game:
                return which_player

            if not valid_position_on_the_board(board_positions):
                return False

            board_positions, player_index, player_shape = player_turn(board_positions)
            all_players_position_on_board[player_shape].append(player_index)

            # Status of the game
            won_game, which_player = game_status(all_players_position_on_board)
            if won_game:
                return which_player


def two_player_game(x_starts):
    board_positions = [' ' for _ in range(9)]
    all_players_position_on_board = {'X': [], 'O': []}
    display_board(board_positions)
    while True:
        if x_starts:
            # Player one turn
            board_positions, player_index, player_shape = player_turn(board_positions)
            all_players_position_on_board[player_shape].append(player_index)

            # Status of the game
            won_game, which_player = game_status(all_players_position_on_board)
            if won_game:
                return which_player

            # is there any empty position on the board?
            if not valid_position_on_the_board(board_positions):
                return False

            # Player 2 turn
            board_positions, player_index, player_shape = player_turn(board_positions, shape='O')
            all_players_position_on_board[player_shape].append(player_index)

            # Status of the game
            won_game, which_player = game_status(all_players_position_on_board, shape='O')
            if won_game:
                return which_player
        else:  # 'O' starts first
            board_positions, player_index, player_shape = player_turn(board_positions, shape='O')
            all_players_position_on_board[player_shape].append(player_index)

            # Status of the game
            won_game, which_player = game_status(all_players_position_on_board, shape='O')
            if won_game:
                return which_player

            if not valid_position_on_the_board(board_positions):
                return False

            board_positions, player_index, player_shape = player_turn(board_positions)
            all_players_position_on_board[player_shape].append(player_index)

            # Status of the game
            won_game, which_player = game_status(all_players_position_on_board)
            if won_game:
                return which_player


def display_scoreboard(res: dict, width):
    clear_terminal()
    print(f"""
\t ┌──────{'─' * width}───────┐
\t │      {'SCOREBOARD':^{width}}       │
\t │      {'──────────':^{width}}       │
\t │      {res['X']['name']:<{width}}  {res['X']['wins']:^3}  │
\t │      {res['O']['name']:<{width}}  {res['O']['wins']:^3}  │
\t └──────{'─' * width}───────┘
"""
          )


# -----------------------------------------------------------------------------------------------
def main():
    player_number = False
    x_first_turn = True

    while not 1 <= player_number < 3:
        try:
            player_number = int(input('1 or 2 player(s)? [1/2] '))
        except ValueError:
            continue
        if player_number == 0:  # faster way to exit i
            exit(0)

    # Getting the player(s) name
    if player_number == 1:
        first_player_name = input('Enter Player 1 name: ').strip()
        score = {
            'X': {
                'name': first_player_name if len(first_player_name) > 0 else "Player 1",
                'wins': 0
            },
            'O': {
                'name': '*Computer*',
                'wins': 0
            }
        }

    else:
        first_player_name = input('Enter Player 1 name: ').strip()
        second_player_name = input('Enter Player 2 name: ').strip()
        score = {
            'X': {
                'name': first_player_name if len(first_player_name) > 0 else "*Player 1*",
                'wins': 0
            },
            'O': {
                'name': second_player_name if len(second_player_name) > 0 else "*Player 2*",
                'wins': 0
            }
        }

    # Start Game & Start Menu
    if player_number == 1:
        while True:
            result = one_player_game(x_first_turn, )
            # Switching who starts first, X or O
            x_first_turn = False if x_first_turn is True else True
            if result:  # Someone won the game
                score[result]['wins'] += 1
            else:
                print("The game ended in a draw")
            display_scoreboard(score, len(first_player_name) if len(first_player_name) > 10 else 10)  # display scoreboard
            if input("Another round? Y/N  ").lower() == 'n':
                break
    else:
        while True:
            result = two_player_game(x_first_turn)
            # Switching who starts first, X or O
            x_first_turn = False if x_first_turn is True else True
            if result:  # Someone won the game
                score[result]['wins'] += 1
            else:
                print("The game ended in a draw")
            # Getting higher len name
            bigger_len = len(sorted([first_player_name, second_player_name], key=len, reverse=True)[0])
            display_scoreboard(score, bigger_len if bigger_len >= 10 else 10)  # display scoreboard
            if input("Another round? Y/N  ").lower() == 'n':
                break


if __name__ == '__main__':
    main()
