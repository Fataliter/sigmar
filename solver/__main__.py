import contextlib, time

from solver.windows import click_new_game, get_screenshot, click_in_window
from solver.vision import detect_board
from solver.board import Element
from solver.solver import solve_game, UnsolveableBoardError

class ActiveBoard(object):
    def __init__(self, board, layout):
        self.board = board
        self.layout = layout

    def take(self, h):
        pt = self.layout.hex_to_pixel(h)
        click_in_window(pt.x, pt.y)
        return self.board.take(h)

@contextlib.contextmanager
def timer(text):
    print(f"{text}...", end="", flush=True)
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"done (took {elapsed:0.3f}s)")

def validate_board(board):
    import collections
    elements = collections.Counter()
    for h, el in board.tiles:
        elements[el] += 1

    for el in Element.Cardinals:
        assert elements[el] == 8
    for el in Element.Metals:
        assert elements[el] == 1
    assert elements[Element.SALT] == 4
    assert elements[Element.QUICKSILVER] == 5
    assert elements[Element.MORS] == 4
    assert elements[Element.VITAE] == 4

    print("Board looks legit!")

def main():
    while True:
        click_new_game()
        image = get_screenshot()

        with timer("Reading board"):
            board, layout = detect_board(image)

        try:
            validate_board(board)
        except:
            print("BAD BOARD!!! I'm just gonna try a new game since I clearly messed that up.")
            continue

        with timer("Solving game"):
            try:
                solution = solve_game(board)
            except UnsolveableBoardError:
                print(":( game was unsolveable")
                continue

        board = ActiveBoard(board, layout)
        for i, action in enumerate(solution):
            action.do(board)

if __name__ == "__main__":
    main()
