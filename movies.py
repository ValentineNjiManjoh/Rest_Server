#CLI app fetching data from OMDb API and storing in local sqlite database
import argparse

from HelperClass import Parser, \
    Highscore, CompareAwards, CompareNumeric
from DB import DB
from OMDBapi import OMDBapi
from Printer import PrintFiltered, PrintHighscores


class Main():
    def __init__(self):
        self.award_parser = Parser()
        self.db = DB()
        self.highscore = Highscore()
        self.repo = OMDBapi(db=self.db, parser=self.award_parser,
                               highscore=self.highscore)
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "-p", "--populate",
            help="Use this option to download data from OMDb \
                  and populate your database",
            action="store_true")
        self.parser.add_argument(
            "-f", "--filter_by",
            help="Filtering by column. Options: awarded, nominated, \
                earned, director [name], actor [name], language [lang]",
            action='store', nargs='*', type=str)
        self.parser.add_argument(
            "--highscores", help="Show Highscores", action='store_true')
        self.parser.add_argument(
            "-c", "--compare",
            help="Compare two movie titles by given column. \
            Options: imdb_rating, box_office, awards, runtime.",
            action='store', nargs='*', type=str)
        self.parser.add_argument(
            "-a", "--add", help="Add movie to database",
            action='store', nargs='*', type=str)
        self.parser.add_argument(
            "-s", "--sort_by",
            help="Sort output data by one or multiple columns",
            action='store', nargs='+',
            choices=[
                'title', 'year', 'runtime', 'genre', 'director',
                'cast', 'writer', 'language', 'country', 'awards',
                'imdb_rating', 'imdb_votes', 'box_office'
                ]
            )

    def main(self):
        """ Main function"""
        args = self.parser.parse_args()
        repo = self.repo

        if args.populate:
            print(repo.populate())

        if args.highscores:
            data = repo.get_highscores()
            PrintHighscores(data).print(data)

        if args.sort_by:
            sorter = args.sort_by[0]
            columns = ('Title', sorter)
            if sorter == 'cast':
                sorter = 'movies.cast'
            if sorter == 'runtime':
                data = repo.get_sorted_by_runtime()
            else:
                data = repo.get_sorted_by(sorter)
            PrintFiltered(data).print(columns, data)

        if args.filter_by:
            choices = [
                'director', 'actor', 'language',
                'awarded', 'nominated', 'earned'
                ]
            if list(args.filter_by) == [] or args.filter_by[0] not in choices:
                print(f"usage: movies.py [-f] filter - choose from: {choices}")

            filter = args.filter_by[0]
            if args.filter_by[0] not in ['nominated', 'awarded', 'earned']:
                value = args.filter_by[1]
            else:
                value = ''

            if filter == 'director':
                columns = ('Title', filter)
                data = repo.get_filtered_by(filter, value)
                PrintFiltered(data).print(columns, data)

            if filter == 'actor':
                columns = ('Title', filter)
                filter = 'movies.cast'
                data = repo.get_filtered_by(filter, value)
                PrintFiltered(data).print(columns, data)

            if filter == 'language':
                columns = ('Title', filter)
                data = repo.get_filtered_by(filter, value)
                PrintFiltered(data).print(columns, data)

            if filter == 'nominated':
                columns = ('Title', filter)
                data = repo.get_nominated()
                PrintFiltered(data).print(columns, data)

            if filter == 'awarded':
                columns = ('Title', filter)
                data = repo.get_awarded()
                awarded = []
                for movie in data:
                    wins = self.award_parser.get_awards(str(movie))
                    nominations = self.award_parser.get_nominations(str(movie))
                    if nominations != 0 and wins/nominations > 0.8:
                        awarded.append(movie)
                PrintFiltered(awarded).print(columns, awarded)

            if filter == 'earned':
                columns = ('Title', filter)
                data = repo.get_earned()
                PrintFiltered(data).print(columns, data)

        if args.add:
            title = args.add[0]
            repo.add(title)

        if args.compare:
            comparator = args.compare[0]
            movies = (args.compare[1], args.compare[2])

            if comparator == 'imdb_rating':
                print(CompareNumeric(repo.get_imdb_rating(movies)).compare())

            if comparator == 'runtime':
                print(CompareNumeric(repo.get_runtime(movies)).compare())

            if comparator == 'box_office':
                print(CompareNumeric(repo.get_box_office(movies)).compare())

            if comparator == 'awards':
                print(CompareAwards(repo.get_awards(movies)).compare())


if __name__ == '__main__':
    Main().main()