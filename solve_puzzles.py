import csv
from sudoku import Sudoku
from draw_sudoku import draw

# csv_file = "hard_puzzles.csv"
csv_file = "medium_puzzles.csv"
with open(csv_file, newline="") as f:
    reader = csv.reader(f)
    rows = list(reader)

num_solved = 0
for i, row in enumerate(rows):
    if len(row) >= 4:
        print(f"Puzzle {i:04}: {row[2]} clues, difficulty = {row[3]}", end="")
    else:
        print(f"Puzzle {i:04}", end="")

    Sx = Sudoku(row[0])
    Sx.solve()
    if Sx.solved:
        print("  -> 😊 Solved")
        num_solved += 1
    else:
        print("  -> 😡 Failed")

    # print("Drawing output...")
    # draw(Sx, f"images/puzzle{i}.pdf")

print(f"{num_solved}/{len(rows)} puzzles sloved")
