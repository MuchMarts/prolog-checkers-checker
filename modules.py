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
    
    def has_won(self, player:str):
        if player not in ["white", "black"]: 
            print("INCORRECT PLAYER")
            return
        opp_counter = 0
        player_counter = 0
        opp = ""
        if player == "white":
            opp = "black"
        else:
            opp = "white"
        
        for p in self.pieces:
            if p.color == opp:
                opp_counter +=1
            else: 
                player_counter += 1

        if player_counter == 0:
            print(f"Opponent {opp} has won!")
            return 1
        elif opp_counter == 0:
            print(f"You {player} won!")
            return 1
        
        return 0

    def to_string(self):
        cell_w = "---"
        cell_h = "|"
        board_str = ""

        board_str += "   "
        for i in range (1,9):
            board_str += f"  {i} "
        board_str += "\n"

        for row in range(1, 9):
            board_str += "   "
            board_str += cell_h + (cell_w + cell_h) * 8
            board_str += "\n"
            
            board_str += f" {row} "
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

    def update_moves(self, moves: str):
        """
        moves format:
        "(c1,r1),(c2,r2),(c3,r3)..."
        """

        # Parse input string into list of tuples
        coords = []
        parts = moves.strip().split("),")
        for part in parts:
            part = part.replace("(", "").replace(")", "").strip()
            col, row = map(int, part.split(","))
            coords.append((col, row))

        if len(coords) < 2:
            return  # nothing to do

        start_col, start_row = coords[0]
        piece = self.pieces_kvp.get((start_col, start_row))
        if not piece: raise ValueError("No piece at starting position")
        del self.pieces_kvp[(start_col, start_row)]

        # Process each move step
        for i in range(1, len(coords)):
            prev_col, prev_row = coords[i - 1]
            new_col, new_row = coords[i]

            if piece.piece_type == "man":
                if piece.color == "white" and new_row == 1:
                    piece.piece_type = "queen"
                elif piece.color == "black" and new_row == 8:
                    piece.piece_type = "queen"
            
            delta_col = new_col - prev_col
            delta_row = new_row - prev_row
            col_negative = False
            row_negative = False
            
            if delta_col < 0: col_negative = True
            if delta_row < 0: row_negative = True

            # Remove *captured* pieces
            for d_row in range(abs(delta_row)):
                for d_col in range(abs(delta_col)):
                    calculated_col = prev_col + (d_col + 1) * (-1 if col_negative else 1)
                    calculated_row = prev_row + (d_row + 1) * (-1 if row_negative else 1)

                    captured_piece = self.pieces_kvp.get((calculated_col, calculated_row))
                    if captured_piece:
                        self.pieces.remove(captured_piece)
                        del self.pieces_kvp[(calculated_col, calculated_row)]
  
        # Update piece position to final square
        final_col, final_row = coords[-1]
        piece.update_pos(final_col, final_row)

        self.pieces_kvp[(final_col, final_row)] = piece