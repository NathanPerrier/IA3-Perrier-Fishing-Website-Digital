from ..api import WildlifeDataAPI as api

class Kingdoms(api):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def get_kingdom_names(self):
        """ KWARGS: None """
        return self._fetch_json(self.KINGDOM_URL)