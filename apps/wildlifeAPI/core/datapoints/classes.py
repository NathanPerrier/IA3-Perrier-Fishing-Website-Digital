from ..api import WildlifeDataAPI as api

class Classes(api):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_class_names(self):
        """ KWARGS optional: kingdom """
        return self._fetch_json(self.CLASS_URL)