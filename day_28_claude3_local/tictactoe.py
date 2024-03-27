# Define the board
board = [' ' for _ in range(9)]

# Define the player symbols
player_symbols = ['X', 'O']

# Define the winning combinations
winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
    [0, 4, 8], [2, 4, 6]  # Diagonals
]

# Function to print the board
def print_board():
    for i in range(0, 9, 3):
        print(f' {board[i]} | {board[i+1]} | {board[i+2]} ')
        if i < 6:
            print('---+---+---')

# Function to check for a winner
def check_winner(player_symbol):
    for combination in winning_combinations:
        if all(board[pos] == player_symbol for pos in combination):
            return True
    return False

# Function to check if the board is full
def is_board_full():
    return all(cell != ' ' for cell in board)

# Main game loop
current_player = 0
while True:
    print_board()
    position = int(input(f"Player {player_symbols[current_player]}, enter a position (1-9): ")) - 1

    if board[position] == ' ':
        board[position] = player_symbols[current_player]

        if check_winner(player_symbols[current_player]):
            print_board()
            print(f"Player {player_symbols[current_player]} wins!")
            break
        elif is_board_full():
            print_board()
            print("It's a tie!")
            break

        current_player = (current_player + 1) % 2
    else:
        print("That position is already taken. Try again.")