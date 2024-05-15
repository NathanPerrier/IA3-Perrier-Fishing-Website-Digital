from core.api import WildlifeDataAPI as api

class Families(api):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def get_family_names(self):
        """ 
            KWARGS required: class
            KWARGS optional: kingdom 
        """
        return self._fetch_json(self.FAMILY_URL)