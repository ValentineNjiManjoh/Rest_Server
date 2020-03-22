import re


class Parser:
    def get_awards(self, data):
        """ Gets awards """
        p = r'(\d*)\s\b(\w*wins\w*)\b\s.\s(\d*)\s\b(\w*nomination*\w*)\b'
        m = re.search(p, data)
        awards = int(m.group(1)) if m is not None else 0
        return awards

    def get_nominations(self, data):
        """ Gets nominations """
        p = r'(\d*)\s\b(\w*wins\w*)\b\s.\s(\d*)\s\b(\w*nomination*\w*)\b'
        m = re.search(p, data)
        nominations = int(m.group(3)) if m is not None else 0
        return nominations

    def get_oscars(self, data):
        """ Gets oscars """
        p = r'\b(\w*Won\w*)\b\s(\d*)\s\b(\w*Oscar*\w*)\b'
        m = re.search(p, data)
        oscars = int(m.group(2)) if m is not None else 0
        return oscars

    def str_to_int(self, string):
        """ Parse string to int """
        s = ''
        try:
            i = (s.join(filter(lambda x: x.isdigit(), string)))
        except TypeError:
            i = 0
        return int(i) if i else 0


class Highscore():
    def __init__(self):
        self.highest_runtime = ('', '')
        self.highest_box_office = ('', '')
        self.oscar_highscore = ('', 0)
        self.nominations_highscore = ('', 0)
        self.awards_highscore = ('', 0)
        self.highest_rating = ('', 0.0)
        self.parser = Parser()

    def get_highest_runtime(self, movies):
        highest_runtime = self.highest_runtime
        for movie in movies:
            if movie[1] is not None and \
                    int(self.parser.str_to_int(movie[1])) > \
                    int(self.parser.str_to_int(highest_runtime[1])):
                highest_runtime = (movie[0], movie[1])
        return highest_runtime

    def get_highest_box_office(self, movies):
        highest_box_office = self.highest_box_office
        for movie in movies:
            if movie[2] is not None and \
                    int(self.parser.str_to_int(movie[2])) > \
                    int(self.parser.str_to_int(highest_box_office[1])):
                highest_box_office = (movie[0], movie[2])
        return highest_box_office

    def get_highest_imdb_rating(self, movies):
        highest_rating = self.highest_rating
        for movie in movies:
            rating = movie[4] if movie[4] is not None else 0
            if rating > int(highest_rating[1]):
                highest_rating = (movie[0], rating)
        return highest_rating

    def get_oscars_highscore(self, movies):
        """ Helper function getting highest oscar wins """
        oscar_highscore = self.oscar_highscore
        for movie in movies:
            oscars = self.parser.get_oscars(movie[3]) \
                if movie[3] is not None else 0
            if oscars > int(oscar_highscore[1]):
                oscar_highscore = (movie[0], oscars)
        return oscar_highscore

    def get_nominations_highscore(self, movies):
        """ Helper function getting nominations highscore """
        nominations_highscore = self.nominations_highscore
        for movie in movies:
            nominations = self.parser.get_nominations(movie[3]) \
                if movie[3] is not None else 0
            if nominations > int(nominations_highscore[1]):
                nominations_highscore = (movie[0], nominations)
        return nominations_highscore

    def get_awards_highscore(self, movies):
        """ Helper function getting awards highscore """
        awards_highscore = self.awards_highscore
        for movie in movies:
            awards = self.parser.get_awards(movie[3]) \
                if movie[3] is not None else 0
            if awards > int(awards_highscore[1]):
                awards_highscore = (movie[0], awards)
        return awards_highscore


class Compare():
    def __init__(self, movies):
        self.parser = Parser()
        self.movie1 = movies[0]
        self.movie2 = movies[1]

    def compare(self):
        pass


class CompareNumeric(Compare):
    def compare(self):
        return self.movie1[0] if self.parser.str_to_int(self.movie1[1]) > \
            self.parser.str_to_int(self.movie2[1]) else self.movie2[0]


class CompareAwards(Compare):
    def compare(self):
        return self.movie1[0] if self.parser.get_awards(self.movie1[1]) > \
            self.parser.get_awards(self.movie2[1]) else self.movie2[0]