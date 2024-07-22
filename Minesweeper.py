import random
import re
class Board:
    """
    Class describing the tic tac toe game state
    """
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()

        # keep truck over tiles we already dig in
        self.dug = set()
    
    def __str__(self):
        text = ' '
        for c in range(self.dim_size):
            if c <= 9:
                text += f'  {c} '
            else:
                text += f'  {c}'
        for row in range(self.dim_size):
            if row <= 9:
                text += f'\n{row} '
            else:
                text += f'\n{row}'
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    text += f'|{self.board[row][col]}| '
                else:
                    text += '|_| '

        return text

    def make_new_board(self):
        """
        Create new board at the start of the game. Empty space signifies safe place, * signifies a bomb
        """

        board = {
            (row, col) : None
            for row in range(self.dim_size)
            for col in range(self.dim_size)
        }
        

        # plant the bombs
        bombs_planted = 0
        
        while bombs_planted < self.num_bombs:
            row_bomb = random.randint(0, self.dim_size - 1)
            col_bomb = random.randint(0, self.dim_size - 1)

            # If there is no bomb in the chosen location plant it
            if board[(row_bomb, col_bomb)] != '*':
                board[(row_bomb, col_bomb)] = '*'
                bombs_planted += 1

        return board

    def assign_values_to_board(self):
        """
        Assigns number to every field, which signifies the number of neighboring mines
        """
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[(r, c)] is None:
                    count = 0
                    for r2 in range(r - 1, r + 2):
                        if r2 >= 0 and r2 < self.dim_size:
                            for c2 in range(c - 1, c + 2):
                                if c2 >= 0 and c2 < self.dim_size:
                                    if self.board[(r2, c2)] == '*':
                                        count += 1
                    self.board[(r, c)] = count

    def dig(self, row, col):
        """
        Dig at the location (row, col).
        """
        # dig at that location!
        # returns true if no bomb, false if the bomb present
        self.dug.add((row, col))

        if self.board[(row, col)] == '*':
            return False

        if self.board[(row, col)] > 0:
            return True

        else:
            for r in range(row - 1, row + 2):
                if r >= 0 and r < self.dim_size:
                    for c in range(col - 1, col + 2):
                        if c >= 0 and c < self.dim_size:
                            if (r, c) in self.dug:
                                continue
                            self.dig(r, c)
            return True

    

def play (dim_size = 20, num_bombs = 10):
    """
    The main function
    """

    board = Board(dim_size, num_bombs)

    safe = True
    while len(board.dug) < board.dim_size * board.dim_size - board.num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input('Where would you like to dig? Input as row, col: '))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print('Invalid location, Try again. ')
            continue

        safe = board.dig(row, col)
        if not safe:
            break
    print(board)
    if safe:
        print('Gratulation, you have won ')
    else:
        print('You have lost ')

        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__':
    play()
