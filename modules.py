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
        
        self._pieces_to_key_pairs() # used for quick access

    def _pieces_to_key_pairs(self):
        self.pieces_kvp = {}
        for p in self.pieces:
            self.pieces_kvp[(p.col, p.row)] = p

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
    
    def to_string(self):
        cell_w = "---"
        cell_h = "|"
        board_str = ""
        
        for row in range(1, 9):
            board_str += cell_h + (cell_w + cell_h) * 8
            board_str += "\n"
            board_str += cell_h
            for col in range(1, 9):
                indicator = " "
                color = " "
                if (col, row) in self.pieces_kvp:
                    piece = self.pieces_kvp[(col, row)]
                    
                    if piece.color == "white":
                        color = "w"
                    elif piece.color == "black":
                        color = "b"
                    
                    if piece.piece_type == "man":
                        indicator = "M"
                    elif piece.piece_type == "queen":
                        indicator = "Q"
                board_str += f"{color + indicator} " + cell_h
            board_str += "\n"

        return board_str

