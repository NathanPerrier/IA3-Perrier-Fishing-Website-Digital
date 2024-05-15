from core.api import WildlifeDataAPI as api

class Organisations(api):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def get_organisations(self):
        """ KWARGS: None """
        return self._fetch_json(self.ORGANISATIONS_URL)
    
