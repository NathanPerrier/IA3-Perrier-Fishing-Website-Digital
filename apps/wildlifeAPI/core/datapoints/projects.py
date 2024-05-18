from ..api import WildlifeDataAPI as api

class Projects(api):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def get_projects(self):
        """ KWARGS optional: org, bbox, circle """
        return self._fetch_json(self.PROJECTS_URL)
    
    def get_projects_by_id(self):
        """ KWARGS required: projids (Comma separated list of project ids) """
        return self._fetch_json(self.PROJECTS_BY_ID_URL)
    
    def get_projects_metadata_by_id(self):
        """ KWARGS required: projids (Comma separated list of project ids) """
        return self._fetch_json(self.PROJECTS_METADATA_BY_ID_URL)

    def project_search(self):
        """ KWARGS required: projtitle """
        return self._fetch_json(self.PROJECTS_SEARCH_URL)