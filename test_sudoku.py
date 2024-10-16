from sudoku import Sudoku
from draw_sudoku import draw

puzzle = [
    [0, 0, 6, 1, 0, 0, 0, 0, 8],
    [0, 8, 0, 0, 9, 0, 0, 3, 0],
    [2, 0, 0, 0, 0, 5, 4, 0, 0],
    [4, 0, 0, 0, 0, 1, 8, 0, 0],
    [0, 3, 0, 0, 7, 0, 0, 4, 0],
    [0, 0, 7, 9, 0, 0, 0, 0, 3],
    [0, 0, 8, 4, 0, 0, 0, 0, 6],
    [0, 2, 0, 0, 5, 0, 0, 8, 0],
    [1, 0, 0, 0, 0, 2, 5, 0, 0],
]

solution = [
    [3, 4, 6, 1, 2, 7, 9, 5, 8],
    [7, 8, 5, 6, 9, 4, 1, 3, 2],
    [2, 1, 9, 3, 8, 5, 4, 6, 7],
    [4, 6, 2, 5, 3, 1, 8, 7, 9],
    [9, 3, 1, 2, 7, 8, 6, 4, 5],
    [8, 5, 7, 9, 4, 6, 2, 1, 3],
    [5, 9, 8, 4, 1, 3, 7, 2, 6],
    [6, 2, 4, 7, 5, 9, 3, 8, 1],
    [1, 7, 3, 8, 6, 2, 5, 9, 4],
]

S1 = Sudoku(puzzle)
S1.solve()
assert S1.solution == solution
draw(S1, "S1.pdf", True)

str_puzzles = [
    "600010000001302600027608510048000950900000001016000340069403180104906700000050000",
    "900703004600090200007060000080000500006040700009000080000050800001020003200901005",
    "160000700094070020000001000000005002009806400400100000000500000040080390003000046",
    "005000080700405000090600705200000006001204800300000024903002010000506009070000200",
    "480007019000000000007010300001604900004000800060070020009701500028050730000030090",
    "000007050300060704000520090000010009080602130060080200270000000006490000004270010",
    "001000800300490000000002090700803024108004500640907008010700000000049001006000700",
    "003500640100002000004000703002900008001827000900004200205000300000200004036009100",
    "006007010400000005005900020000020800060000050001090000090003500800000007020800400",
    "890670000050800000300020084107008006080050010500000308400080009000001020000032041",
]

for i, str_puz in enumerate(str_puzzles):
    print(f"Puzzle {i}")
    Sx = Sudoku(str_puz)
    Sx.solve()
    if Sx.solved:
        print("  -> 😊 Solved")
    else:
        print("  -> 😡 Failed")
    print("Drawing output...")
    draw(Sx, f"puzzle{i}.pdf")
