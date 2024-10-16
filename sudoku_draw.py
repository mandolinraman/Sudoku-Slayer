from pyx import canvas, path, style, text
import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        "text.usetex": True,
        # "font.family": "Helvetica",
        # "text.latex.preamble": r"\usepackage{xcolor}"
    }
)


def draw_pyx(solver, filename, show_candidates=True):
    """Draw the current state of a sudoku puzzle board using the PyX backend."""

    d = 1.5
    # text.set(mode="latex")
    text.set(text.LatexEngine)
    # text.preamble(r"\usepackage{cmbright}")
    # text.preamble(r"\usepackage{times}")
    # text.preamble(r"\usepackage{lmodern}\renewcommand{\familydefault}{\sfdefault}")
    text.preamble(r"\usepackage{color}\renewcommand{\familydefault}{\sfdefault}")
    c = canvas.canvas()
    for x in range(9):
        for y in range(9):
            i, j = 8 - y, x  # rotate puzzle 90 degrees
            c.stroke(path.rect(x * d, y * d, d, d))

            # get value and options at (i, j)
            candidates = "".join(str(v) for v in solver.cells[i][j])
            if solver.puzzle[i][j] > 0:
                value = str(solver.puzzle[i][j])
            elif len(candidates) == 1:
                value = r"{\textcolor{cyan}{" + candidates + "}}"
            else:
                value = ""

            if value != "":
                c.text(
                    x * d + d / 2,
                    y * d + d / 2,
                    rf"{value}",
                    [text.halign.boxcenter, text.valign.middle, text.size.Huge],
                )
            elif show_candidates:
                c.text(
                    x * d + d / 2,
                    y * d + d / 10,
                    r"{\tiny\textcolor{cyan}{" + candidates + "}}",
                    [text.halign.boxcenter, text.valign.middle, text.size.Huge],
                )

            if x % 3 == 0 and y % 3 == 0:
                c.stroke(path.rect(x * d, y * d, 3 * d, 3 * d), [style.linewidth(0.1)])

    c.writePDFfile(filename)


def draw_mpl(puzzle, filename, show_candidates=True):
    """Draw the current state of a sudoku puzzle board using the matplotlib backend."""

    def box(x, y, a, b):
        return (x, x + a, x + a, x, x), (y, y, y + b, y + b, y)

    d = 1
    plt.figure(figsize=(6, 6))
    for x in range(9):
        for y in range(9):
            i, j = 8 - y, x  # rotate puzzle 90 degrees
            plt.plot(*box(x * d, y * d, d, d), "k", linewidth=0.5)

            # get value and options at (i, j)
            candidates = "".join(str(v) for v in puzzle.cells[i][j])

            if puzzle.puzzle[i][j] > 0:
                value = str(puzzle.puzzle[i][j])
                color = "k"
            elif len(candidates) == 1:
                value = candidates
                color = "m"
            else:
                value = ""
                color = "k"

            if value != "":
                plt.text(
                    x * d + d / 2,
                    y * d + d / 2,
                    value,
                    verticalalignment="center",
                    horizontalalignment="center",
                    fontsize=28,
                    c=color,
                )
            elif show_candidates:
                plt.text(
                    x * d + d / 2,
                    y * d + d / 10,
                    candidates,
                    verticalalignment="center",
                    horizontalalignment="center",
                    fontsize=6,
                    c="m",
                )

            if x % 3 == 0 and y % 3 == 0:
                plt.plot(*box(x * d, y * d, 3 * d, 3 * d), "k", linewidth=2)

    plt.axis([0, 9, 0, 9])
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def draw(puzzle, filename, show_candidates=True, backend="pyx"):
    if backend.lower() == "pyx":
        draw_pyx(puzzle, filename, show_candidates)
    elif backend.lower() == "mpl":
        draw_mpl(puzzle, filename, show_candidates)
