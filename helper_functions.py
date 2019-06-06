import pychromecast


# Helper Functions
def discover_casts(cast):
    chromecasts = pychromecast.get_chromecasts()
    for _cast in chromecasts:
        if _cast.name == cast:
            cast = _cast
            return cast


# The cast in this case will be the same as the cast passed into play_spotify
def get_cast(cast_ip, cast):
    _cast = pychromecast.Chromecast(cast_ip)
    if(_cast and _cast.name == cast):
        return _cast
    else:
        return discover_casts(cast)
