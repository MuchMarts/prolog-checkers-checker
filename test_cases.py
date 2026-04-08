from modules import Board, Piece

def make_board(*pieces):
    """Helper to build a board from piece tuples (color, type, col, row)."""
    return Board([Piece(color, piece_type, col, row) 
                  for color, piece_type, col, row in pieces])

tests = [
    # Basic man movement
    (
        "black man valid forward move",
        make_board(("black", "man", 2, 2)),
        "black", [(2,2),(3,3)], True
    ),
    (
        "white man valid forward move",
        make_board(("white", "man", 4, 4)),
        "white", [(4,4),(3,3)], True
    ),
    (
        "black man invalid backward move",
        make_board(("black", "man", 4, 4)),
        "black", [(4,4),(3,3)], False
    ),
    (
        "white man invalid backward move",
        make_board(("white", "man", 4, 4)),
        "white", [(4,4),(5,5)], False
    ),
    (
        "man blocked destination",
        make_board(("white", "man", 2, 2), ("black", "man", 3, 3)),
        "white", [(2,2),(3,3)], False
    ),
    (
        "man move to white square",
        make_board(("white", "man", 2, 2)),
        "white", [(2,2),(3,2)], False
    ),
    (
        "man move off board",
        make_board(("white", "man", 8, 8)),
        "white", [(8,8),(9,9)], False
    ),

    # Forced capture
    (
        "non-capture move when capture available",
        make_board(("white", "man", 2, 2), ("black", "man", 3, 3)),
        "white", [(2,2),(1,3)], False
    ),
    (
        "correct capture taken when available",
        make_board(("white", "man", 2, 2), ("black", "man", 3, 3)),
        "white", [(2,2),(4,4)], True
    ),

    # Man captures
    (
        "valid capture forward",
        make_board(("white", "man", 2, 2), ("black", "man", 3, 3)),
        "white", [(2,2),(4,4)], True
    ),
    (
        "valid capture backward",
        make_board(("white", "man", 4, 4), ("black", "man", 3, 3)),
        "white", [(4,4),(2,2)], True
    ),
    (
        "cannot capture own piece",
        make_board(("white", "man", 2, 2), ("white", "man", 3, 3)),
        "white", [(2,2),(4,4)], False
    ),
    (
        "landing square occupied",
        make_board(("white", "man", 2, 2), ("black", "man", 3, 3), ("white", "man", 4, 4)),
        "white", [(2,2),(4,4)], False
    ),

    # Chain captures
    (
        "valid two jump chain",
        make_board(("white", "man", 2, 2), ("black", "man", 3, 3), ("black", "man", 5, 5)),
        "white", [(2,2),(4,4),(6,6)], True
    ),
    (
        "chain stopped early",
        make_board(("white", "man", 2, 2), ("black", "man", 3, 3), ("black", "man", 5, 5)),
        "white", [(2,2),(4,4)], False
    ),
    (
        "cannot jump same piece twice",
        make_board(("white", "man", 2, 2), ("black", "man", 3, 3)),
        "white", [(2,2),(4,4),(2,2)], False
    ),

    # Promotion
    (
        "man reaches back row",
        make_board(("black", "man", 3, 7)),
        "black", [(3,7),(4,8)], True
    ),
    (
        "man captures onto back row",
        make_board(("black", "man", 2, 6), ("white", "man", 3, 7)),
        "black", [(2,6),(4,8)], True
    ),
    (
        "man promotes mid chain continues as queen",
        make_board(("black", "man", 2, 6), ("white", "man", 3, 7), ("white", "man", 5, 7)),
        "black", [(2,6),(4,8),(8,4)], True
    ),

    # Queen movement
    (
        "queen valid move any distance",
        make_board(("white", "queen", 2, 2)),
        "white", [(2,2),(6,6)], True
    ),
    (
        "queen moves backward",
        make_board(("white", "queen", 6, 6)),
        "white", [(6,6),(2,2)], True
    ),
    (
        "queen blocked by own piece",
        make_board(("white", "queen", 2, 2), ("white", "man", 4, 4)),
        "white", [(2,2),(6,6)], False
    ),

    # Queen captures
    (
        "queen valid capture",
        make_board(("white", "queen", 2, 2), ("black", "man", 4, 4)),
        "white", [(2,2),(6,6)], True
    ),
    (
        "queen can stop close to captured piece",
        make_board(("white", "queen", 2, 2), ("black", "man", 4, 4)),
        "white", [(2,2),(5,5)], True
    ),
    (
        "queen cannot jump two pieces",
        make_board(("white", "queen", 2, 2), ("black", "man", 4, 4), ("black", "man", 6, 6)),
        "white", [(2,2),(8,8)], False
    ),
    (
        "queen chain capture",
        make_board(("white", "queen", 2, 2), ("black", "man", 4, 4), ("black", "man", 4, 6)),
        "white", [(2,2),(5,5),(2,8)], True
    ),
]