class Params:
    utits = "metric"
    lang = "en"
    q: str | None
    lat: float | None
    lon: float | None

    def __init__(
        self, appid: str, city: str | None = None, location: tuple | list | None = None
    ):
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
        self.appid = appid

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

    def cache_key(self) -> str:
        if self.q is not None:
            return self.q.lower()
        return f"{self.lat:.5f},{self.lon:.5f}"
