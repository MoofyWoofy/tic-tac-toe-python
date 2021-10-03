import random


# https://en.wikipedia.org/wiki/Box-drawing_character     https://www.copyandpastesymbols.net/line-symbols.html


def display_board(positions):
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


def computer_turn(board_positions, shape='O'):
    computer_position = 4  # Default center,
    while board_positions[computer_position] != ' ':
        computer_position = random.randint(0, 8)
    # Placing position on the board
    board_positions[computer_position] = 'O'
    display_board(board_positions)
    return board_positions, computer_position, shape  # return new positions


def player_turn(board_positions, shape='X'):
    while True:
        try:
            player_input = int(input(f"Enter position ({shape}): "))
        except ValueError:
            print("Not a position on the board, try again!")
            continue
        if not 0 < player_input <= 9:
            print("Not a position on the board, try again!")
        if board_positions[player_input - 1] == ' ':
            # Placing position on the board
            board_positions[player_input - 1] = shape
            display_board(board_positions)
            return board_positions, player_input - 1, shape  # return new board positions
        else:
            print("Invalid position, it is already taken")


def game_status(players_location: dict, shape='X'):
    all_possible_winning_scenario = [
        [6, 3, 0], [7, 4, 1], [8, 5, 2],  # Vertical
        [6, 7, 8], [3, 4, 5], [0, 1, 2],  # Horizontal
        [6, 4, 2], [8, 4, 0]  # Diagonal
    ]
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
            board_positions, computer_index, computer_shape = computer_turn(board_positions)
            all_players_position_on_board[computer_shape].append(computer_index)

            # Status of the game
            won_game, which_player = game_status(all_players_position_on_board, shape='O')
            if won_game:
                return which_player
        else:  # 'O' starts first
            board_positions, computer_index, computer_shape = computer_turn(board_positions)
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
    print(f"""
\t ┌──────{'─'*width}───────┐
\t │      {'SCOREBOARD':^{width}}       │
\t │      {'──────────':^{width}}       │
\t │      {res['X']['name']:<{width}}  {res['X']['wins']:^3}  │
\t │      {res['O']['name']:<{width}}  {res['O']['wins']:^3}  │
\t └──────{'─'*width}───────┘
"""
          )


# -----------------------------------------------------------------------------------------------

player_number = False
x_first_turn = True
# X O

while not 1 <= player_number < 3:
    try:
        player_number = int(input('1 or 2 player(s)? [1/2] '))
    except ValueError:
        pass


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
"""
return == False
    game was a draw
"""
if player_number == 1:
    while True:
        result = one_player_game(x_first_turn)
        # Switching who starts first, X or O
        x_first_turn = False if x_first_turn is True else True
        if result:
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
        if result:
            score[result]['wins'] += 1
        else:
            print("The game ended in a draw")
        # Getting higher len name
        bigger_len = len(sorted([first_player_name, second_player_name], key=len, reverse=True)[0])
        display_scoreboard(score, bigger_len if bigger_len >= 10 else 10)  # display scoreboard
        if input("Another round? Y/N  ").lower() == 'n':
            break

