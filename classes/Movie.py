class Movie:
    #Movie class

    def __init__(
        self, title='N/A', year=0, runtime='N/A', genre='N/A',
        director='N/A', cast='N/A', writer='N/A',
        language='N/A', country='N/A', awards='N/A',
        imdb_rating=0.0, imdb_votes=0, box_office=0
    ):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.cast = cast
        self.writer = writer
        self.language = language
        self.country = country
        self.awards = awards
        self.imdb_rating = imdb_rating
        self.imdb_votes = imdb_votes
        self.box_office = box_office

    def __str__(self):
        return self.title

    @staticmethod
    def json_to_movie(data):
        """ Parse JSON data to Movie object """
        return Movie(
            title=data['Title'],
            year=data['Year'],
            runtime=data['Runtime'],
            genre=data['Genre'],
            director=data['Director'],
            cast=data['Actors'],
            writer=data['Writer'],
            language=data['Language'],
            country=data['Country'],
            awards=data['Awards'],
            imdb_rating=data['imdbRating'],
            imdb_votes=data['imdbVotes'],
            box_office=data['BoxOffice']
            )