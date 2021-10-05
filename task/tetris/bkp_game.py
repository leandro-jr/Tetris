import numpy as np
from collections import deque

class Piece:
    """Piece object and related functionality"""
    def __init__(self, shape, dimensions):
        """The initializer for the class.

        Arguments:
        shape -- string with piece shape I, S, Z, L, J, O, T.
        dimensions -- list with int M and N grid dimensions
        """
        # m height n width
        self.m = dimensions[0]
        self.n = dimensions[1]
        # grid is a matrix array. M "row" arrays  with N "columns" filled with '-'
        self.grid = np.array([['-'] * self.m] * self.n)
        # shape is not been used for now
        self.shape = shape
        # rotation to be used on initial_position arrays on subclasses
        self.rotation = 0
        self.print_grid()

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
        for position in np_positions:
            # for row (// 10 % self.n) and for column  % 10 to piece move through the borders
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
        # update np_positions with the move. Calls it new_np_positions
        new_np_positions = (np_positions + move)
        go_horizontal = True
        # if any position in new_np_positions changes row after the move was added to np_positions, flag go_horizontal
        # is set to False and new_np_positions is ignored
        for index in range(len(np_positions)):
            if new_np_positions[index] // 10 != np_positions[index] // 10:
                go_horizontal = False

        if go_horizontal:
            np_positions = (new_np_positions + 10)
        else:
            np_positions = (np_positions + 10)
        # update the grid after the movement
        self.write_position(np_positions)
        return np_positions

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
        for index in range(len(np_positions)):
            if np_positions[index] // 10 == self.n - 1:
                hit_floor = True
        return hit_floor


# There is no need to create one class for each piece shape at this moment of the project. I used that to pratice inheritance
class I(Piece):
    """I object and related functionality. It is a child class from Piece class"""
    def __init__(self, dimensions):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__("I", dimensions)
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
    def __init__(self, dimensions):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__("S", dimensions)
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
    def __init__(self, dimensions):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__("Z", dimensions)
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
    def __init__(self, dimensions):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__("L", dimensions)
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
    def __init__(self, dimensions):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__("J", dimensions)
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
    def __init__(self, dimensions):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__("O", dimensions)
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
    def __init__(self, dimensions):
        """The initializer for the class. Inherits the methods of Piece class and creates others.

        Arguments:
        dimensions -- list with int M and N grid dimensions
        """
        super().__init__("T", dimensions)
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
    """Input piece shape, grid dimensions and piece movements.

    First input is the Tetris piece shape. Shapes can be I, S, Z, L, J, O, T.
    Second input is the Tetris grid dimension MxN. Where M is the number of columns and N the number of rows. After the
    second input is provided, a blank grid and a grid with the chosen piece is displayed.
    Next inputs are the movements of the piece. Options are: right, left, down, rotate(to rotate the piece). After each
    movement input the piece moves down on the grid as well. The grid is displayed after each movement input.
    Input break to finish the game.

    Example:
    T
    10 20
    right
    break
    """
    # shape = input("piece: ")
    shape = input()
    # dimensions = [int(x) for x in input("dimensions: ").split()]
    dimensions = [int(x) for x in input().split()]
    # create the movements deque where the player movements will be stored
    movements = deque()
    # based on shape creates the class instance. The variable with the instance is "piece"
    if shape == 'I':
        piece = I(dimensions)
    elif shape == 'S':
        piece = S(dimensions)
    elif shape == 'Z':
        piece = Z(dimensions)
    elif shape == 'L':
        piece = L(dimensions)
    elif shape == 'J':
        piece = J(dimensions)
    elif shape == 'O':
        piece = O(dimensions)
    elif shape == 'T':
        piece = T(dimensions)

    # calls the class method based on the movement
    while True:
        command = input()
        if command == "exit":
            break
        # verify if piece achieved the floor. If yes, ignore command and print the grid
        if piece.floor(piece.np_positions):
            piece.write_position(piece.np_positions)
        else:
            # for "right", move method is called. +1 is sent to move and added to movements
            if command == "right":
                piece.np_positions = piece.move(piece.np_positions, 1)
                movements.append(1)
            # for "left", move method is called. -1 is sent to move and added to movements
            elif command == "left":
                piece.np_positions = piece.move(piece.np_positions, -1)
                movements.append(-1)
            # for "down", move method is called. 0 is added to movements
            elif command == "down":
                piece.np_positions = piece.move(piece.np_positions)
                movements.append(0)
            # for "rotate", rotate method is called. 0 is added to movements
            elif command == "rotate":
                # shifts the initial_positions array when user wants to rotate the piece
                piece.rotation = (piece.rotation + 1) % len(piece.initial_positions)
                movements.append(0)
                piece.np_positions = piece.rotate(piece.initial_positions[piece.rotation], movements)

if __name__ == '__main__':
    main()