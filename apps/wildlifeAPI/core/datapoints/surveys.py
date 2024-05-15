from core.api import WildlifeDataAPI as api

class Surveys(api):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def get_surveys(self):
        """ 
            KWARGS required: projids
            KWARGS optional: proj, p, min, max, pagecount, pageindex, bbox, circle
        """
        return self._fetch_json(self.GET_SURVEYS_URL)
    
    def get_surveys_by_species(self):
        """ 
            KWARGS optional: kingdom, proj, p, min, max, pagecount, pageindex, bbox, circle
        """
        return self._fetch_json(self.GET_SURVEYS_BY_SPECIES_URL)