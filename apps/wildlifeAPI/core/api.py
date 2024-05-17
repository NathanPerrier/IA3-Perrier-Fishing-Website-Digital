import json
import urllib.request
from ala import AlaDataAPI

class WildlifeDataAPI:
    """
    This code snippet defines a class called WildlifeDataAPI. It provides methods to interact with the Queensland Government Wildlife Data API and retrieve various types of wildlife data.

    Variables:
    - API_BASE: The base URL of the API.
    - KINGDOM_URL: The endpoint for retrieving kingdom names.
    - CLASS_URL: The endpoint for retrieving class names.
    - FAMILY_URL: The endpoint for retrieving family names.
    - SPECIES_URL: The endpoint for retrieving species.
    - debug: A boolean flag to enable debug mode.
    - extensive_search: A boolean flag to enable extensive search mode (relays data for nested urls in result).
    - FORMAT: The format of the data to be retrieved (JSON).
    - ACKNOWLEDGEMENT: A string indicating the source of the data.

    Methods:
    - __init__: Initializes the WildlifeDataAPI object. Accepts optional parameters for the kingdom and debug mode.
    - _fetch_json: Fetches JSON data from the specified endpoint.
    - search: Performs a search using the specified URL and returns the result.
    - get_secondary_results: Helper method to handle nested URLs in the search results.
    - debug_url: Prints the URL being fetched if debug mode is enabled.
    - clean_data: Cleans the retrieved data by converting keys to snake_case and removing empty values.
    - get_epbc_statuses: Retrieves the EPBC statuses.
    - get_nca_statuses: Retrieves the NCA statuses.
    
    NOTE: when defining a species' class you must use class_

    Example usage:
        data = WildlifeDataAPI(debug=True, species="whiting", class_="ray-finned fishes").species_search()
    """
    
    API_BASE = 'http://apps.des.qld.gov.au/species/'
    
    # API endpoints
    KINGDOM_URL = 'getkingdomnames'
    CLASS_URL = 'getclassnames'
    FAMILY_URL = 'getfamilynames'
    SPECIES_URL = 'getspecies'
    SPECIES_BY_ID_URL = 'getspeciesbyid' 
    SPECIES_SEARCH = 'speciessearch'
    ORGANISATIONS_URL = 'getorganisations'
    PROJECTS_URL = 'getprojects'
    PROJECTS_BY_ID_URL = 'getprojectsmetadatabyid'
    PROJECTS_METADATA_BY_ID_URL = 'getprojectsmetadatabyid'
    PROJECTS_SEARCH_URL = 'projectsearch'
    GET_SITES_URL = 'getsites'
    GET_SURVEYS_URL = 'getsurveys'
    GET_SURVEYS_BY_SPECIES_URL = 'getsurveysbyspecies'
    GET_SPECIES_LIST_URL = 'getspecieslist'
    GET_EPBC_STATUSES_URL = 'getepbcstatuses'
    GET_NCA_STATUSES_URL = 'getncastatuses'
    
    FORMAT = 'json'
    
    ACKNOWLEDGEMENT = 'Data courtesy of the Queensland Government Wildlife Data API'
    

    def __init__(self, kingdom='animals', debug=False, extensive_search=False, extensive_info=False, **kwargs):
        self.kingdom = kingdom
        
        self.debug = debug
        self.extensive_search = extensive_search
        self.extensive_info = extensive_info
        
        if kwargs.get('class_'):
            kwargs['class'] = kwargs.pop('class_')
            
        if not kwargs.get('kingdom'):
            kwargs['kingdom'] = self.kingdom
            
        self.params = kwargs

        self.acknowledgment = self.ACKNOWLEDGEMENT

    def _fetch_json(self, endpoint): 
        """ 
            Fetch the data from the specified endpoint with custom parameters and return the result. 
        """
        
        url = f"{self.API_BASE}?op={endpoint}&f={self.FORMAT}"

        if self.params:
            url += '&' + urllib.parse.urlencode(self.params)
        
        return self.search(url)
        
    def search(self, url, result=None, key=None):
        """ 
            Fetch the data from the specified url and return the result. 
        """
        
        self.debug_url(url)
            
        try:
            result = self.search_request(url, result, key)

            if self.extensive_info: result = AlaDataAPI(self).get_extensive_info(result) 
            if self.extensive_search: result = self.get_secondary_results(result)
            
            return self.clean_data(result)
        
        except urllib.error.HTTPError as e:
            print(f"Error fetching {url}: {e}")
            return None
        
   
    def search_request(self, url, result=None, key=None):
        """
            Fetch the data from the specified url and return the result.
        """
        req = urllib.request.Request(url)

        json_text = urllib.request.urlopen(req).read().decode('utf-8')
        
        if result is None and key is None:
            result = json.loads(json_text)
        else: 
            result[key] = json.loads(json_text)
            
        return result
        
    def get_secondary_results(self, result):
        """ 
            Recursively search for nested urls in the result and fetch the data. 
            
            Only if extensive_search is enabled.
        """
        result = self.clean_result(result)
        for key in result:
            if 'url' in key.lower():  
                if 'http' in result[key]: 
                    result = self.search_request(result[key], key=key, result=result)
            try:
                for secondary_key in (result[key] if isinstance(result[key], dict) else (result[key][0] if isinstance(result[key], list) else {})):
                    if 'url' in secondary_key.lower():
                        if 'http' in (result[key][secondary_key] if isinstance(result[key], dict) else result[key][0][secondary_key]):
                            result = (self.search_request(result[key][secondary_key], key=secondary_key, result=result[key]) if isinstance(result[key], dict) else self.search(result[key][0][secondary_key], key=secondary_key, result=result[key][0]))
            except Exception as e: self.debug_url('ERROR,', e)
            
        return result
    
    def debug_url(self, *args):
        if self.debug:
            print('FETCHING ', *args)
            
    def clean_data(self, data):
        """ 
            Recursively clean the data by converting keys to snake_case and removing empty values.
        """
        if isinstance(data, dict):
            cleaned_data = {}
            for key, value in data.items():
                cleaned_key = key.lower().replace(' ', '_')  
                if isinstance(value, (dict, list)):
                    cleaned_data[cleaned_key] = self.clean_data(value)  
                elif value is not None:
                    cleaned_data[cleaned_key] = value  
            return cleaned_data
        elif isinstance(data, list):
            return [self.clean_data(item) for item in data]  
        else:
            return data  

    def clean_result(self, result):
        """ 
            Clean the result by converting keys to snake_case and removing empty values.
        """
        print('CLEANING')
        try:
            return result['species'][0]
        except: 
            return result

