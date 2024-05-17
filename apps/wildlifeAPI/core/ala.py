import json
import urllib.request

class AlaDataAPI:
        
    ALA_SPECIES_GUIDE_URL = 'https://api.ala.org.au/species/guid/'
    ADDITIONAL_INFO_URL = 'https://api.ala.org.au/species/species/'
    ALA_SPECIES_IMAGES_URL = 'https://api.ala.org.au/species/imageSearch/'

    def __init__(self, parent):
        self.parent = parent
        
        self.kingdom = self.parent.kingdom
        
        self.debug = self.parent.debug
        self.extensive_search = self.parent.extensive_search
        self.extensive_info = self.parent.extensive_info
            
        self.params = self.parent.params

        
    
    def search(self, url, result=None, key=None):
        """ 
            Fetch the data from the specified url and return the result. 
        """
        
        self.debug_url(url)
        
        req = urllib.request.Request(url)

        json_text = urllib.request.urlopen(req).read().decode('utf-8')
        
        if result is None and key is None:
            result = json.loads(json_text)
        else: 
            result[key] = json.loads(json_text)
            
        return result
            
    
    def get_url(self, url, endpoint):
        return f"{url}{endpoint}"
        
    def get_extensive_info(self, result):
        """ 
            Fetch the additional information for the species. 
        """
        try:
            result = self.search(url=self.get_url(self.ALA_SPECIES_GUIDE_URL, self.get_name(result)), result=result, key='guide')
            result = self.search(url=self.get_url(self.ADDITIONAL_INFO_URL, result["guide"][0]["identifier"]), result=result, key='extensive_info')
            return self.search(url=self.get_url(self.ALA_SPECIES_IMAGES_URL, result["guide"][0]["identifier"]), result=result, key='images')
        except Exception as e:
            self.debug_url('ERROR', e)
            return result
    def get_name(self, result):
        """ 
            Fetch the additional information for the species. 
        """
        if isinstance(result["Species"], list):
            return result["Species"][0]["ScientificName"].replace(" ", "%20")  
        else: 
            return result["species"]["ScientificName"].replace(" ", "%20")
        
    def debug_url(self, *args):
        if self.debug:
            print('FETCHING ', *args)