class PrettyPrinter():
    def __init__(self, data):
        def get_width(data):
            """ Helper function getting table width """
            width = 2
            max_length = 5
            for item in data:
                if len(str((item[0]))) > max_length:
                    max_length = len(item[0])
            return width+max_length

        self.width = get_width(data)

    def print(self, columns, data):
        pass


class PrintFiltered(PrettyPrinter):
    def print(self, columns, data):
        col1 = columns[0].title()
        col2 = columns[1].title()
        print(col1.ljust(self.width), col2.ljust(self.width))
        for (title, value) in data:
            print(str(title).ljust(self.width), str(value))


class PrintHighscores(PrettyPrinter):
    def print(self, data):
        rows = [
            'Runtime', 'Box Office', 'Awards',
            'Nominations', 'Oscars', 'IMDb Rating'
        ]
        rows_width = 13
        highscores = zip(rows, data)
        for column, (title, value) in highscores:
            print(
                str(column).ljust(rows_width),
                str(title).ljust(self.width),
                value
            )