from tf.advanced.app import App


class TfApp(App):
    def __init__(app, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def getLexId(app, n):
        api = app.api
        F = api.F

        lex = F.lex.v(n)
        lan = F.language.v(n)
        return "{}{}".format(
            "1" if lan == "Hebrew" else "2",
            lex.replace(">", "A")
            .replace("<", "O")
            .replace("[", "v")
            .replace("/", "n")
            .replace("=", "i"),
        )
