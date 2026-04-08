% Valid colors
color(white).
color(black).

% Valid pieces
piece_type(man).
piece_type(queen).

valid_piece(piece(Color, Type,Col, Row)) :-
    color(Color), piece_type(Type), dark_square(Col, Row).

% Board
valid_board([]).
valid_board([Pieces | Rest]) :-
    valid_piece(Pieces),
    valid_board(Rest).

% Helpers
valid_square(Col, Row) :-
    Col >= 1, Col =< 8,
    Row >= 1, Row =< 8.
% If even it is a dark square
dark_square(Col, Row) :-
    valid_square(Col, Row),
    0 is (Col + Row) mod 2.

back_row(white, 8).
back_row(black, 1).

should_promote(Player, Row) :-
    back_row(Player, Row).

piece_at(Board, Col, Row, Color, Type) :-
    member(piece(Color, Type, Col, Row), Board).

empty_square(Board, Col, Row) :-
    valid_square(Col, Row),
    \+ piece_at(Board, Col, Row, _, _).

oponent(white, black).
oponent(black, white).

is_oponent_piece(Board, Player, Col, Row) :-
    oponent(Player, Oponent),
    piece_at(Board, Col, Row, Oponent, _).

forward_direction(white, -1).
forward_direction(black, 1).

is_diagonal(Col1, Row1, Col2, Row2) :-
    ColDiff is abs(Col1 - Col2),
    RowDiff is abs(Row1 - Row2),
    ColDiff =:= RowDiff,
    ColDiff > 0.

diagonal_direction(Col1, Row1, Col2, Row2, ColDir, RowDir) :-
    is_diagonal(Col1, Row1, Col2, Row2),
    ColDir is sign(Col2 - Col1),
    RowDir is sign(Row2 - Row1).

middle_square(Col1, Row1, Col2, Row2, MidCol, MidRow) :-
    is_diagonal(Col1, Row1, Col2, Row2),
    MidCol is (Col1 + Col2) // 2,
    MidRow is (Row1 + Row2) // 2.

squares_between(Col1, Row1, Col2, Row2, Squares) :-
    diagonal_direction(Col1, Row1, Col2, Row2, ColDir, RowDir),
    NextCol is Col1 + ColDir,
    NextRow is Row1 + RowDir,
    squares_between_acc(NextCol, NextRow, Col2, Row2, ColDir, RowDir, Squares).

squares_between_acc(Col2, Row2, Col2, Row2, _, _, []) :- !.
squares_between_acc(Col, Row, Col2, Row2, ColDir, RowDir, [(Col,Row)|Rest]) :-
    NextCol is Col + ColDir,
    NextRow is Row + RowDir,
    squares_between_acc(NextCol, NextRow, Col2, Row2, ColDir, RowDir, Rest).

valid_man_move(Board, Player, Col1, Row1, Col2, Row2) :-
    piece_at(Board, Col1, Row1, Player, man),
    empty_square(Board, Col2, Row2),
    diagonal_direction(Col1, Row1, Col2, Row2, _, RowDir),
    forward_direction(Player, RowDir),
    ColDiff is abs(Col2 - Col1),
    ColDiff =:= 1.

valid_man_capture(Board, Player, Col1, Row1, Col2, Row2) :-
    piece_at(Board, Col1, Row1, Player, man),
    % generate all possible jump destinations
    member(ColDir, [-1, 1]),
    member(RowDir, [-1, 1]),
    Col2 is Col1 + 2 * ColDir,
    Row2 is Row1 + 2 * RowDir,
    valid_square(Col2, Row2),
    empty_square(Board, Col2, Row2),
    MidCol is Col1 + ColDir,
    MidRow is Row1 + RowDir,
    is_oponent_piece(Board, Player, MidCol, MidRow).

% base case
valid_chain_capture(Board, Player, [(Col1,Row1), (Col2,Row2)]) :-
    valid_man_capture(Board, Player, Col1, Row1, Col2, Row2),
    middle_square(Col1, Row1, Col2, Row2, MidCol, MidRow),
    oponent(Player, Oponent),
    piece_at(Board, MidCol, MidRow, Oponent, Type),
    % Remove captures piece
	select(piece(Oponent, Type, MidCol, MidRow), Board, TempBoard),
    % Remove old piece
    piece_at(Board, Col1, Row1, Player, MyType),
    select(piece(Player, MyType, Col1, Row1), TempBoard, TempBoard2),
    NewBoard = [piece(Player, queen, Col2, Row2) | TempBoard2],
    \+ capture_available(NewBoard, Player).

valid_chain_capture(Board, Player, [(Col1,Row1), (Col2,Row2) | Rest]) :-
    valid_man_capture(Board, Player, Col1, Row1, Col2, Row2),
    middle_square(Col1, Row1, Col2, Row2, MidCol, MidRow),
    oponent(Player, Oponent),
    piece_at(Board, MidCol, MidRow, Oponent, Type),
    % Remove captures piece
	select(piece(Oponent, Type, MidCol, MidRow), Board, TempBoard),
    % Remove old piece
    piece_at(Board, Col1, Row1, Player, MyType),
    select(piece(Player, MyType, Col1, Row1), TempBoard, TempBoard2),
    
    % check if promoted
    ( should_promote(Player, Row2)
    -> 
    % becomes queen, continue as queen chain        
        NewBoard = [piece(Player, queen, Col2, Row2) | TempBoard2],
       	valid_queen_chain_capture(NewBoard, Player, [(Col2,Row2) | Rest]);  	
    % stays man, continue as man chain
        NewBoard = [piece(Player, MyType, Col2, Row2) | TempBoard2],
       	valid_chain_capture(NewBoard, Player, [(Col2,Row2) | Rest])
    ).

squares_empty(_, []).
squares_empty(Board, [(Col, Row) | Rest]) :-
    empty_square(Board, Col, Row),
    squares_empty(Board, Rest).

valid_queen_move(Board, Player, Col1, Row1, Col2, Row2) :-
    piece_at(Board, Col1, Row1, Player, queen),
    is_diagonal(Col1, Row1, Col2, Row2),
    empty_square(Board, Col2, Row2),
    squares_between(Col1, Row1, Col2, Row2, Squares),
    squares_empty(Board, Squares).

valid_queen_capture(Board, Player, Col1, Row1, Col2, Row2) :-
    piece_at(Board, Col1, Row1, Player, queen),
    % pick a diagonal direction
    member(ColDir, [-1, 1]),
    member(RowDir, [-1, 1]),
    % walk along diagonal to find opponent piece
    find_opponent_on_diagonal(Board, Player, Col1, Row1, ColDir, RowDir, OppCol, OppRow),
    % generate a landing square past the opponent
    LandCol is OppCol + ColDir,
    LandRow is OppRow + RowDir,
    generate_landing(Board, LandCol, LandRow, ColDir, RowDir, Col2, Row2).

find_opponent_on_diagonal(Board, Player, Col, Row, ColDir, RowDir, OppCol, OppRow) :-
    NextCol is Col + ColDir,
    NextRow is Row + RowDir,
    valid_square(NextCol, NextRow),
    is_oponent_piece(Board, Player, NextCol, NextRow),
    OppCol = NextCol,
    OppRow = NextRow.
find_opponent_on_diagonal(Board, Player, Col, Row, ColDir, RowDir, OppCol, OppRow) :-
    NextCol is Col + ColDir,
    NextRow is Row + RowDir,
    valid_square(NextCol, NextRow),
    empty_square(Board, NextCol, NextRow),
    find_opponent_on_diagonal(Board, Player, NextCol, NextRow, ColDir, RowDir, OppCol, OppRow).

generate_landing(Board, Col, Row, _, _, Col, Row) :-
    valid_square(Col, Row),
    empty_square(Board, Col, Row).
generate_landing(Board, Col, Row, ColDir, RowDir, Col2, Row2) :-
    valid_square(Col, Row),
    empty_square(Board, Col, Row),
    NextCol is Col + ColDir,
    NextRow is Row + RowDir,
    generate_landing(Board, NextCol, NextRow, ColDir, RowDir, Col2, Row2).

valid_queen_chain_capture(Board, Player, [(Col1,Row1), (Col2,Row2)]) :-
    valid_queen_capture(Board, Player, Col1, Row1, Col2, Row2).

valid_queen_chain_capture(Board, Player, [(Col1,Row1), (Col2,Row2) | Rest]) :-
    valid_queen_capture(Board, Player, Col1, Row1, Col2, Row2),
    oponent(Player, Oponent),
    member(ColDir, [-1, 1]),
    member(RowDir, [-1, 1]),
    find_opponent_on_diagonal(Board, Player, Col1, Row1, ColDir, RowDir, OppCol, OppRow),
    % Remove captures piece
    piece_at(Board, OppCol, OppRow, Oponent, Type),
	select(piece(Oponent, Type, OppCol, OppRow), Board, TempBoard),
    % Remove old piece
    piece_at(Board, Col1, Row1, Player, MyType),
    select(piece(Player, MyType, Col1, Row1), TempBoard, TempBoard2),
    NewBoard = [piece(Player, MyType, Col2, Row2) | TempBoard2],
    
    valid_queen_chain_capture(NewBoard, Player, [(Col2, Row2) | Rest]).

capture_available(Board, Player) :-
    member(piece(Player, man, Col, Row), Board),
    valid_man_capture(Board, Player, Col, Row, _, _).
capture_available(Board, Player) :-
    member(piece(Player, queen, Col, Row), Board),
    valid_queen_capture(Board, Player, Col, Row, _, _).

valid_move(Board, Player, [(Col1,Row1), (Col2,Row2)]) :-
    valid_board(Board),
    \+ capture_available(Board, Player),
    (valid_man_move(Board, Player, Col1, Row1, Col2, Row2) ;
     valid_queen_move(Board, Player, Col1, Row1, Col2, Row2)).

valid_move(Board, Player, Move) :-
    valid_board(Board),
    length(Move, Len), Len >= 2,
    (valid_chain_capture(Board, Player, Move) ;
     valid_queen_chain_capture(Board, Player, Move)).
