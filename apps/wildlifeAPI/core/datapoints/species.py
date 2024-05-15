from core.api import WildlifeDataAPI as api

class Species(api):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def get_species(self):
        """ KWARGS required: family """
        return self._fetch_json(self.SPECIES_URL)

    def get_species_by_id(self):
        """ KWARGS required: taxonid """
        return self._fetch_json(self.SPECIES_BY_ID_URL)

    def species_search(self):
        """ 
            KWARGS required: species
            KWARGS optional: kingdom, class, family
        """
        return self._fetch_json(self.SPECIES_SEARCH)
    
    def get_species_list(self):
        """ KWARGS: None """
        return self._fetch_json(self.GET_SPECIES_LIST_URL)
