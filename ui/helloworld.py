import marimo

__generated_with = "0.4.2"
app = marimo.App(layout_file="layouts/helloworld.grid.json")


@app.cell
def __(mo, x):
    mo.md(f"Choose a sentence: {x} Showing sentence {x.value}")
    return


@app.cell
def __(mo):
    x = mo.ui.slider(1, 10)
    return x,


@app.cell
def __(A, F, highlights, x):
    A.pretty(F.otype.s("sentence")[x.value - 1], tupleFeatures="gloss", highlights=highlights)
    return


@app.cell
def __():
    from tf.app import use
    import marimo as mo
    return mo, use


@app.cell
def __(use):
    A = use("ETCBC/bhsa")
    return A,


@app.cell
def __(A):
    F = A.api.F
    return F,


@app.cell
def __(F):
    highlights = {}

    for s in range(1, F.otype.maxSlot + 1):
        if F.sp.v(s) == "verb":
            highlights[s] = "lightblue"
        elif F.gloss.v(s) == "god(s)":
            highlights[s] = "gold"
    return highlights, s


if __name__ == "__main__":
    app.run()
