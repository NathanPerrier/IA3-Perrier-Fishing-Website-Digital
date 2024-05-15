import os, sys
from django.test import TestCase
from core.__init__ import *

sys.path.append(os.path.abspath('.'))

import pytest

from core.api import WildlifeDataAPI

class TestAPI(TestCase):
    def setUp(self):
        self.api = WildlifeDataAPI(kingdom='animal', species='whiting', debug=1)


    def test_api(self):
        assert WildlifeDataAPI() is not None
        
    def test_search_species(self):
        species = Species(species='Sillago sihama').species_search() 
        assert species is not None
        assert species['species']['acceptedcommonname'] == 'northern whiting'
        assert species['species']['scientificname'] == 'Sillago sihama'
        assert species['species']['taxonid'] == 27069

    def test_kingdoms(self):
        assert Kingdoms().get_kingdom_names() is not None
    
    def test_extensive_search(self):
        species = Species(species='whiting', extensive_search=True).species_search()
        assert species is not None
    
    #! add more