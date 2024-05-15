from core.api import WildlifeDataAPI as api

class Statuses(api):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def get_epbc_statuses(self):
        """ KWARGS: None """
        return self._fetch_json(self.GET_EPBC_STATUSES_URL)
    
    def get_nca_statuses(self):
        """ KWARGS: None """
        return self._fetch_json(self.GET_NCA_STATUSES_URL)