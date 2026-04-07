class Piece:
    def __init__(self, color, piece_type, col, row):
        self.color = color
        self.piece_type = piece_type
        self.col = col
        self.row = row

    def update_pos(self, col, row):
        self.col = col
        self.row = row

    def to_prolog(self):
        return f"piece({self.color}, {self.piece_type}, {self.col}, {self.row})"

    def __repr__(self):
        return self.to_prolog()


class Board:
    def __init__(self, pieces=None):
        """
        pieces: list of Piece objects
        If None, initializes standard starting position
        """
        if pieces is not None:
            self.pieces = pieces
        else:
            self.pieces = self._starting_position()

    def _starting_position(self):
        pieces = []
        for row in range(1, 9):
            for col in range(1, 9):
                if (col + row) % 2 == 0:  # dark square
                    if row <= 3:
                        pieces.append(Piece("black", "man", col, row))
                    elif row >= 6:
                        pieces.append(Piece("white", "man", col, row))
        return pieces

    def to_prolog(self):
        return "[" + ", ".join(p.to_prolog() for p in self.pieces) + "]"

    def __repr__(self):
        return self.to_prolog()

