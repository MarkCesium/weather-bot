class Params:
    def __init__(self, city: str | None = None, location: tuple | None = None):
        if city is not None:
            self.q = city
            self.lat = None
            self.lon = None
        elif location is not None:
            self.lat = location[0]
            self.lon = location[1]
            self.q = None
        else:
            raise ValueError("No city or location provided")
        self.utits = "metric"
        self.lang = "en"
        self.appid = WEATHER_TOKEN

    def __call__(self) -> dict:
        params: dict = {
            "units": self.utits,
            "lang": self.lang,
            "appid": self.appid,
        }
        if self.q is not None:
            params.update({"q": self.q})
        else:
            params.update({"lat": self.lat, "lon": self.lon})

        return params
