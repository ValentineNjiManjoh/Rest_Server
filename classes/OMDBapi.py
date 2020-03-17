import json
import requests
from classes.Movie import Movie

URL = 'http://omdbapi.com/'


def get_apikey():
    """ Gets API key from JSON"""
    with open('apikey.json', 'r') as f:
        apikey = json.load(f)
    return apikey


def get_movie(url, params):
    """ Gets movie data from API"""
    res = requests.get(url, params)
    return res.json()


class OMDBapi():
    def __init__(self, db, parser, highscore):
        self.db = db
        self.parser = parser
        self.highscore = highscore

    def populate(self):
        """ Populates database with data from API"""
        print("Downloading data from OMDb...")
        cursor = self.db.get_all_titles()
        movie_list = cursor.fetchall()
        key = get_apikey()['apikey']
        for (title, ) in movie_list:
            params = dict(apikey=key, t=title, type='movie')
            response = get_movie(URL, params=params)
            movie = Movie.json_to_movie(response)
            self.db.update(movie)
            print(f"Succesfully retrieved data from OMDb for {title}\n")
        self.db.conn.commit()

    def add(self, title):
        print(f'Succesfully added {title} to database')
        key = get_apikey()['apikey']
        params = dict(apikey=key, t=title, type='movie')
        try:
            response = get_movie(URL, params=params)
            movie = Movie.json_to_movie(response)
            self.db.update(movie)
            self.db.conn.commit()
            print(f"Succesfully retrieved data from OMDb for {title}\n")
        except Exception:
            self.db.conn.rollback()
            print(f"Couldn't find data in OMDb - rolling back {title}\n")

    def get_awards(self, movies):
        cursor = self.db.get_awards(movies[0], movies[1])
        return cursor.fetchall()

    def get_box_office(self, movies):
        cursor = self.db.get_box_office(movies[0], movies[1])
        return cursor.fetchall()

    def get_runtime(self, movies):
        cursor = self.db.get_runtime(movies[0], movies[1])
        return cursor.fetchall()

    def get_imdb_rating(self, movies):
        cursor = self.db.get_imdb_rating(movies[0], movies[1])
        return cursor.fetchall()

    def get_filtered_by(self, filter, value):
        cursor = self.db.get_filtered_by(filter, value)
        return cursor.fetchall()

    def get_awarded(self):
        cursor = self.db.get_awarded()
        return cursor.fetchall()

    def get_earned(self):
        cursor = self.db.get_boxoffice_over_hundred_million()
        return cursor.fetchall()

    def get_nominated(self):
        cursor = self.db.get_oscar_nominated()
        return cursor.fetchall()

    def get_highscores(self):
        cursor = self.db.get_for_highscores()
        data = cursor.fetchall()
        runtime = self.highscore.get_highest_runtime(data)
        box_office = self.highscore.get_highest_box_office(data)
        awards = self.highscore.get_awards_highscore(data)
        nominations = self.highscore.get_nominations_highscore(data)
        oscars = self.highscore.get_oscars_highscore(data)
        rating = self.highscore.get_highest_imdb_rating(data)
        return [runtime, box_office, awards, nominations, oscars, rating]

    def get_sorted_by_runtime(self):
        cursor = self.db.get_sorted_by_runtime()
        return cursor.fetchall()

    def get_sorted_by(self, sorter):
        cursor = self.db.get_sorted_by(sorter)
        try:
            data = cursor.fetchall()
        except TypeError:
            pass
        return data