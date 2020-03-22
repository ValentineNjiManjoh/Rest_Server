import sqlite3 as sql


def dict_from_class(cls):
    """ Returns dictionary from Movie class"""
    return dict((key, value) for (key, value) in cls.__dict__.items())


class DB:
    """ Database class """
    def __init__(self):
        self.conn = sql.connect('movies.sqlite')
        self.cursor = self.conn.cursor()

    def insert(self, movie):
        """ Inserts movie title to database"""
        params = (movie, )
        return self.cursor.execute(
            "insert into movies ('title') \
            select :title where not exists \
            (select 1 from movies where title=:title)", params
        )

    def update(self, movie):
        """ Updates movie data in database"""
        params = dict_from_class(movie)
        return self.cursor.execute(
            "update movies set year=:year, runtime=:runtime, \
            genre=:genre, director=:director, cast=:cast, \
            writer=:writer, language=:language, country=:country, \
            awards=:awards, imdb_rating=:imdb_rating, imdb_votes=:imdb_votes, \
            box_office=:box_office where title=:title", params
            )

    def get_all_titles(self):
        """ Gets all movie titles from database """
        return self.cursor.execute(
            "select title from movies"
        )

    def get_all(self):
        """ Gets all records from database """
        return self.cursor.execute(
            "select * from movies"
        )

    def get_by_title(self, movie):
        """ Gets movie by title """
        params = dict_from_class(movie)
        return self.cursor.execute(
            "select * from movies where title=:title", params
        )

    def get_sorted_by(self, column):
        """ Gets movies sorted by given column """
        query = ""f"select title, {column} \
            from movies order by {column} desc"""
        return self.cursor.execute(query)

    def get_sorted_by_runtime(self):
        """ Gets movies sorted by given column """
        def str_to_int(item):
            """ Regex helper function"""
            s = ''
            try:
                i = (s.join(filter(lambda x: x.isdigit(), item)))
            except TypeError:
                i = 0
            return int(i) if i else 0
        self.conn.create_function("STR_TO_INT", 1, str_to_int)
        return self.cursor.execute(
            "select title, runtime \
            from movies order by cast(str_to_int(runtime) as int) desc"
        )

    def get_filtered_by_director(self, director):
        """ Gets movies filtered by director """
        param = ('%'+director+'%',)
        return self.cursor.execute(
            "select title, director \
            from movies where director like ?", param
        )

    def get_filtered_by_actor(self, actor):
        """ Gets movies filtered by actor """
        param = ('%'+actor+'%', )
        return self.cursor.execute(
            "select title, movies.cast \
            from movies where movies.cast like ?", param
        )

    def get_filtered_by(self, Filter, value):
        """ Gets movies filtered by given value """
        params = ('%'+value+'%', )
        return self.cursor.execute(
            f"select title, {Filter} \
            from movies where {Filter} like ?", params
        )

    def get_oscar_nominated(self):
        """ Gets movies nominated to Oscar """
        return self.cursor.execute(
            "select title, awards \
            from movies where awards like 'nominated%'"
        )

    def get_awarded(self):
        """ Gets movies titles with awards """
        return self.cursor.execute(
            "select title, awards from movies"
        )

    def get_boxoffice_over_hundred_million(self):
        """ Gets movies with income over $100 mln """
        def str_to_int(item):
            """ Regex helper function"""
            s = ''
            try:
                i = (s.join(filter(lambda x: x.isdigit(), item)))
            except TypeError:
                i = 0
            return int(i) if i else 0
        self.conn.create_function("STR_TO_INT", 1, str_to_int)
        return self.cursor.execute(
            "select title, box_office \
            from movies \
            where cast(str_to_int(box_office) as int) > '100000000'"
        )

    def get_by_language(self, language):
        """ Gets movies filtered by language """
        param = ('%'+language+'%', )
        return self.cursor.execute(
            "select title, language \
            from movies where language like ?", param
        )

    def get_imdb_rating(self, movie1, movie2):
        """ Gets two given movies with rating """
        params = (movie1, movie2, )
        return self.cursor.execute(
            "select title, imdb_rating \
            from \
            (select title, imdb_rating \
            from movies where title like ? \
            union select title, imdb_rating \
            from movies where title like ?)", params
        )

    def get_box_office(self, movie1, movie2):
        """ Gets two given movies with box office """
        params = (movie1, movie2, )
        return self.cursor.execute(
            "select title, box_office \
            from \
            (select title, box_office \
            from movies where title like ? \
            union select title, box_office \
            from movies where title like ?)", params
        )

    def get_runtime(self, movie1, movie2):
        """ Gets two given movies with box runtime """
        params = (movie1, movie2, )
        return self.cursor.execute(
            "select title, runtime \
            from movies where title like ? \
            union select title, runtime \
            from movies where title like ?", params
        )

    def get_for_highscores(self):
        """ Gets movies with columns for highscores """
        return self.cursor.execute(
            "select title, runtime, box_office, awards, imdb_rating \
            from movies"
        )

    def get_awards(self, movie1, movie2):
        """ Gets two given movies with awards """
        params = (movie1, movie2, )
        return self.cursor.execute(
            "select title, awards \
            from movies where title like ? \
            union select title, awards \
            from movies where title like ?", params
        )