from pyswip import Prolog
from test_cases import tests as TEST_CASES
from modules import Board, Piece
import argparse

prolog = Prolog()
prolog.consult("checkers_checker.pl")

def move_to_prolog(move):
    """Convert list of (col, row) tuples to Prolog term string."""
    squares = [f"({col},{row})" for col, row in move]
    return "[" + ", ".join(squares) + "]"


def verify_move(board: Board, player, move):
    board_str = board.to_prolog()
    move_str = move_to_prolog(move)
    query = f"valid_move({board_str}, {player}, {move_str})"
    return bool(list(prolog.query(query)))


def run_test(name, board, player, move, expected):
    result = verify_move(board, player, move)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    if not passed:
        print(f"       Expected: {expected}, Got: {result}")
        print(f"       Board: {board}")
        print(f"       Move: {move}")
    return passed

def run_tests():
    passed = 0
    failed = 0

    print("Running checkers verifier tests...\n")

    for test in TEST_CASES:
        name, board, player, move, expected = test
        try:
            if run_test(name, board, player, move, expected):
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed out of {passed + failed}")


def run_app():
    print("Running normal app mode...")
    board = Board()
    print(board.to_string())
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["test", "run"],
        default="run",
        help="Execution mode"
    )

    args = parser.parse_args()

    if args.mode == "test":
        run_tests()
    else:
        run_app()