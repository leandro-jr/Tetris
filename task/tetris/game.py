import numpy as np
from collections import deque

class Piece:
    """Piece object and related functionality"""
    def __init__(self, dimensions, stored_pieces):
        """The initializer for the class.

        Arguments:
        shape -- string with piece shape I, S, Z, L, J, O, T.
        dimensions -- list with int M and N grid dimensions
        """
        # m width n height
        self.m = dimensions[0]
        self.n = dimensions[1]
        # grid is a matrix array. M "row" arrays  with N "columns" filled with '-'
        self.grid = np.array([['-'] * self.m] * self.n)
        # rotation to be used on initial_position arrays on subclasses
        self.rotation = 0
        self.stored_pieces = stored_pieces

    def print_grid(self):
        """Print the MxN grid.
        """
        # for each row, prints each column. self.m - 1 is used because the array index starts at 0
        for row in self.grid:
            for index, column in enumerate(row):
                # if it is the end of the row, don't add blank space after the {column} and go to next line
                if index == self.m - 1:
                    print(f"{column}")
                # else remains in line and add blank space to {column} content
                else:
                    print(f"{column} ", end="")
        # this print is necessary to pass the question test
        print()

    def write_position(self, np_positions):
        """Recreate the original grid with '-' and replace '-' for '0' where the piece is placed at the moment.

        Arguments:
        np_positions - - numpy array with the current position of the piece on the grid.E.g[4 14 24 34]
        """
        self.grid = np.array([['-'] * self.m] * self.n)
        # write grid with saved pieces
        if self.stored_pieces:
            for position in self.stored_pieces:
                row = position // 10
                column = position % 10
                try:
                    self.grid[row][column] = 0
                except IndexError:
                    print(self.stored_pieces)
                    print(f"row: {row}, column: {column}")
        # write grid with np_positions
        if len(np_positions) != 0:
            for position in np_positions:
                row = (position // 10) % self.n
                column = position % 10
                self.grid[row][column] = 0
        self.print_grid()

    def move(self, np_positions, move=0):
        """Add +1/-1/0 to positions numpy array, making it moves 'right'/'left'/'down'. Limit movement within grid walls.
        Then, add +10 making it moves 'down'.

        Arguments:
        np_positions -- numpy array with the current position of the piece on the grid. E.g [4 14 24 34]
        move -- int with +1 to right, -1 to left and 0 to down
        Return the np_positions updated
        """
        # update np_positions with the command move. Saves it as new_np_positions
        new_np_positions = (np_positions + move)
        # if go_horizontal is True, move is allowed
        go_horizontal = True
        # if go_vertical is True, piece movement down is allowed
        go_vertical = True
        # if any position in new_np_positions changes row after the move was added to np_positions, flag go_horizontal
        # is set to False and new_np_positions is ignored
        for index in range(len(np_positions)):
            if new_np_positions[index] // 10 != np_positions[index] // 10:
                go_horizontal = False

        # if any position in new_np_positions matches a position in piece.stored_pieces, flag go_horizontal and
        # go_vertical are set to False and new_np_positions is ignored
        if self.stored_pieces:
            for position in self.stored_pieces:
                if position in new_np_positions + 10:
                    go_horizontal = False
                    go_vertical = False

        if go_horizontal and go_vertical:
            np_positions = (new_np_positions + 10)
        elif not go_horizontal and go_vertical:
            np_positions = (np_positions + 10)

        # update the grid after the movement
        self.write_position(np_positions)
        return np_positions, go_vertical


    def rotate(self, positions, movements):
        """Movements has all piece movements made in the game. Using it as a queue, remake all the piece movements
        (+1/-1/0) or 'right'/'left'/'down' to the rotated piece. Then, add +10 making it moves 'down' for each movement.

        Arguments:
        positions -- list with initial position of the rotated piece on the grid. E.g [4, 14, 24, 34]
        movements -- deque with ints: +1 to right, -1 to left and 0 to down
        Return the np_positions updated
        """
        np_positions = np.array(positions)
        for movement in movements:
            np_positions = (np_positions + movement)
            np_positions = (np_positions + 10)
        # update the grid after the movement
        self.write_position(np_positions)
        return np_positions

    def floor(self, np_positions):
        """Verify if piece achieved the floor of the grid.

        Arguments:
        np_positions -- numpy array with the current position of the piece on the grid. E.g [4 14 24 34]
        Return boolean True if piece touched the floor. False otherwise
        """
        hit_floor = False
        if (np_positions // 10 == self.n - 1).any():
            hit_floor = True
            self.stored_pieces = self.stored_pieces + deque(np_positions.tolist())
        return hit_floor

    def erase_row(self):
        """Verify if row must be erased and update grid accordingly.

        Return boolean True if row was erased. False otherwise.
        """
        test_width_sorted = deque(sorted(self.stored_pieces.copy()))
        count_col = 0
        last_row = self.n - 1
        row_erased = False
        while len(test_width_sorted) > 0:
            i = test_width_sorted.pop()
            if i // 10 == last_row:
                count_col += 1
                if count_col == self.m:
                    np_test_width_sorted = np.array(test_width_sorted) + 10
                    test_width_sorted = deque(np_test_width_sorted.tolist())
                    count_col = 0
                    row_erased = True
            else:
                break
        if row_erased:
            self.stored_pieces = deque(np_test_width_sorted.tolist())
        return row_erased


    def game_over(self, np_positions):
        """Verify if a column of the grid was completely filled. If yes, it's game over.

        Arguments:
        np_positions -- numpy array with the current position of the piece on the grid. E.g [4 14 24 34]
        Return boolean True if it's game over. False otherwise.
        """
        test_height = self.stored_pieces.copy()
        for position in np_positions:
            test_height.append(position)
        test_height_sorted = deque(sorted(test_height))
        while True:
            i = test_height_sorted.popleft()
            increment = 10
            count_row = 1
            if i // 10 == 0:
                while i + increment in test_height_sorted and count_row < self.n:
                    increment += 10
                    count_row += 1
                if count_row == self.n:
                    return True
            else:
                break
        return False



# There is no need to create one class for each piece shape at this moment of the project. I used that to pratice inheritance
class I(Piece):
    """I object and related functionality. It is a child class from Piece class"""
    def __init__(self, dimensions, stored_pieces):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__(dimensions, stored_pieces)
        self.shape = "I"
        # possible initial positions of the piece for each rotation on the grid
        self.initial_positions = [[4, 14, 24, 34], [3, 4, 5, 6]]
        # chooses an initial position based on the rotation. Index 0 is been used.
        self.positions = self.initial_positions[self.rotation]
        self.np_positions = np.array(self.positions)
        # update the grid after the piece is created
        self.write_position(self.np_positions)

    def __repr__(self):
        """Print of the piece"""
        return f"Shape: {self.shape}; Initial positions: {self.initial_positions}; Rotation: {self.rotation}; np_positions: {self.np_positions}"


class S(Piece):
    """S object and related functionality. It is a child class from Piece class"""
    def __init__(self, dimensions, stored_pieces):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__(dimensions, stored_pieces)
        self.shape = "S"
        # possible initial positions of the piece for each rotation on the grid
        self.initial_positions = [[5, 4, 14, 13], [4, 14, 15, 25]]
        # chooses an initial position based on the rotation. Index 0 is been used.
        self.positions = self.initial_positions[self.rotation]
        self.np_positions = np.array(self.positions)
        # update the grid after the piece is created
        self.write_position(self.np_positions)

    def __repr__(self):
        """Print of the piece"""
        return f"Shape: {self.shape}; Initial positions: {self.initial_positions}; Rotation: {self.rotation}; np_positions: {self.np_positions}"


class Z(Piece):
    """Z object and related functionality. It is a child class from Piece class"""
    def __init__(self, dimensions, stored_pieces):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__(dimensions, stored_pieces)
        self.shape = "Z"
        # possible initial positions of the piece for each rotation on the grid
        self.initial_positions = [[4, 5, 15, 16], [5, 15, 14, 24]]
        # chooses an initial position based on the rotation. Index 0 is been used.
        self.positions = self.initial_positions[self.rotation]
        self.np_positions = np.array(self.positions)
        # update the grid after the piece is created
        self.write_position(self.np_positions)

    def __repr__(self):
        """Print of the piece"""
        return f"Shape: {self.shape}; Initial positions: {self.initial_positions}; Rotation: {self.rotation}; np_positions: {self.np_positions}"


class L(Piece):
    """L object and related functionality. It is a child class from Piece class"""
    def __init__(self, dimensions, stored_pieces):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__(dimensions, stored_pieces)
        self.shape = "L"
        # possible initial positions of the piece for each rotation on the grid
        self.initial_positions = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
        # chooses an initial position based on the rotation. Index 0 is been used.
        self.positions = self.initial_positions[self.rotation]
        self.np_positions = np.array(self.positions)
        # update the grid after the piece is created
        self.write_position(self.np_positions)

    def __repr__(self):
        """Print of the piece"""
        return f"Shape: {self.shape}; Initial positions: {self.initial_positions}; Rotation: {self.rotation}; np_positions: {self.np_positions}"


class J(Piece):
    """J object and related functionality. It is a child class from Piece class"""
    def __init__(self, dimensions, stored_pieces):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__(dimensions, stored_pieces)
        self.shape = "J"
        # possible initial positions of the piece for each rotation on the grid
        self.initial_positions = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
        # chooses an initial position based on the rotation. Index 0 is been used.
        self.positions = self.initial_positions[self.rotation]
        self.np_positions = np.array(self.positions)
        # update the grid after the piece is created
        self.write_position(self.np_positions)

    def __repr__(self):
        """Print of the piece"""
        return f"Shape: {self.shape}; Initial positions: {self.initial_positions}; Rotation: {self.rotation}; np_positions: {self.np_positions}"


class O(Piece):
    """O object and related functionality. It is a child class from Piece class"""

    def __init__(self, dimensions, stored_pieces):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__(dimensions, stored_pieces)
        self.shape = "O"
        # possible initial positions of the piece for each rotation on the grid
        self.initial_positions = [[4, 14, 15, 5]]
        # chooses an initial position based on the rotation. Index 0 is been used.
        self.positions = self.initial_positions[self.rotation]
        self.np_positions = np.array(self.positions)
        # update the grid after the piece is created
        self.write_position(self.np_positions)

    def __repr__(self):
        """Print of the piece"""
        return f"Shape: {self.shape}; Initial positions: {self.initial_positions}; Rotation: {self.rotation}; np_positions: {self.np_positions}"


class T(Piece):
    """T object and related functionality. It is a child class from Piece class"""
    def __init__(self, dimensions, stored_pieces):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__(dimensions, stored_pieces)
        self.shape = "T"
        # possible initial positions of the piece for each rotation on the grid
        self.initial_positions = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
        # chooses an initial position based on the rotation. Index 0 is been used.
        self.positions = self.initial_positions[self.rotation]
        self.np_positions = np.array(self.positions)
        # update the grid after the piece is created
        self.write_position(self.np_positions)

    def __repr__(self):
        """Print of the piece"""
        return f"Shape: {self.shape}; Initial positions: {self.initial_positions}; Rotation: {self.rotation}; np_positions: {self.np_positions}"

def main():
    """Input grid dimensions, piece shape and piece movements.

    First input is the Tetris grid dimension MxN. Where M is the number of columns and N the number of rows. After the
    input is provided, a blank grid with MxN dimension is displayed.
    After that, user input 'piece' followed by the Tetris piece shape. Shapes can be I, S, Z, L, J, O, T.
    Next inputs are the movements of the piece. Options are: right, left, down, rotate(to rotate the piece). After each
    movement input the piece moves down on the grid as well. The grid is displayed after each movement input.
    If an entire row is occupied by pieces, the row disappears.
    If an entire column is occupied by pieces, it's game over.
    Input 'break' to stop and 'exit' to finish the game.

    Example:
    10 10
    piece
    T
    right
    down
    break
    """
    # MxN grid dimensions
    dimensions = [int(x) for x in input().split()]
    # stored_pieces will save pieces that hit the floor or that touched other pieces
    stored_pieces = deque()
    # display empty grid
    empty_grid = Piece(dimensions, stored_pieces)
    empty_grid.print_grid()
    # calls the class method based on the movement
    while True:
        command = input()
        if command == "exit":
            break
        elif command == "break":
            piece.write_position([])
        elif command == "piece":
            shape = input()
            # create the movements deque where the player movements will be stored for a given piece
            movements = deque()
            # based on shape creates the class instance. The variable with the instance is "piece"
            if shape == 'I':
                piece = I(dimensions, stored_pieces)
            elif shape == 'S':
                piece = S(dimensions, stored_pieces)
            elif shape == 'Z':
                piece = Z(dimensions, stored_pieces)
            elif shape == 'L':
                piece = L(dimensions, stored_pieces)
            elif shape == 'J':
                piece = J(dimensions, stored_pieces)
            elif shape == 'O':
                piece = O(dimensions, stored_pieces)
            elif shape == 'T':
                piece = T(dimensions, stored_pieces)

        # verify if game over condition was reached
        elif piece.game_over(piece.np_positions):
            piece.write_position(piece.np_positions)
            print("Game Over!")
            break

        # verify if piece achieved the floor. If yes, saves the piece position, ignore command, print the grid and
        # verifies if row must be erased
        elif piece.floor(piece.np_positions):
            stored_pieces = piece.stored_pieces.copy()
            piece.write_position(piece.np_positions)
            if piece.erase_row():
                stored_pieces = piece.stored_pieces.copy()

        # for "right", move method is called. +1 is sent to move and added to movements
        # go_vertical is a flag that if false means that a piece touched another and need to be saved
        elif command == "right":
            piece.np_positions, go_vertical = piece.move(piece.np_positions, 1)
            movements.append(1)
            if not go_vertical:
                piece.stored_pieces = piece.stored_pieces + deque(piece.np_positions.tolist())
                stored_pieces = piece.stored_pieces.copy()
        # for "left", move method is called. -1 is sent to move and added to movements
        elif command == "left":
            piece.np_positions, go_vertical = piece.move(piece.np_positions, -1)
            movements.append(-1)
            if not go_vertical:
                piece.stored_pieces = piece.stored_pieces + deque(piece.np_positions.tolist())
                stored_pieces = piece.stored_pieces.copy()
        # for "down", move method is called. 0 is added to movements
        elif command == "down":
            piece.np_positions, go_vertical = piece.move(piece.np_positions)
            movements.append(0)
            if not go_vertical:
                piece.stored_pieces = piece.stored_pieces + deque(piece.np_positions.tolist())
                stored_pieces = piece.stored_pieces.copy()
        # for "rotate", rotate method is called. 0 is added to movements
        elif command == "rotate":
            # shifts the initial_positions array when user wants to rotate the piece
            piece.rotation = (piece.rotation + 1) % len(piece.initial_positions)
            movements.append(0)
            piece.np_positions = piece.rotate(piece.initial_positions[piece.rotation], movements)

if __name__ == '__main__':
    main()