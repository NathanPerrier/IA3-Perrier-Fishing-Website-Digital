from core.api import WildlifeDataAPI as api

class Sites(api):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def get_sites(self):
        """ 
            KWARGS required: projid 
            KWARGS optional: proj, pagecount, pageindex, bbox, circle
        """
        return self._fetch_json(self.GET_SITES_URL)