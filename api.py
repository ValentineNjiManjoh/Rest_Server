"""Public interface for omdb module
Accessible via:
    import omdb
"""

from .client import OMDBClient

# Internal client instance used for our requests.
_client = OMDBClient()


def set_default(key, default):
    """Proxy method to internal client instance that sets default params
    values.
    """
    _client.set_default(key, default)


def get(**params):
    """Generic request."""
    return _client.get(**params)


def search(string, **params):
    """Search by string."""
    return _client.search(string, **params)


def search_movie(string, **params):
    """Search movies by string."""
    return _client.search_movie(string, **params)


def search_episode(string, **params):
    """Search episodes by string."""
    return _client.search_episode(string, **params)


def search_series(string, **params):
    """Search series by string."""
    return _client.search_series(string, **params)


def imdbid(string, **params):
    """Get by IMDB ID."""
    return _client.imdbid(string, **params)


def title(string, **params):
    """Get by title."""
    return _client.title(string, **params)


def request(**params):
    """Lower-level request."""
    return _client.request(**params)