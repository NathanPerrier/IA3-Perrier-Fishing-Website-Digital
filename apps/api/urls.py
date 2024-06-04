from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.api.views import *

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'wildlife', WildlifeViewSet, basename='wildlife')

urlpatterns = [
    path('', include(router.urls)),
    
    path('users/search/', UserViewSet.as_view({'get': 'search'}), name="user_api_search"),
    
    path('wildlife/kingdoms', WildlifeKingdomsViewSet.as_view({'get': 'list'}), name='wildlife-kingdoms'),
    path('wildlife/kingdoms/<int:pk>/', WildlifeKingdomsViewSet.as_view({'get': 'retrieve'}), name='wildlife-kingdoms-retrieve'),
    path('wildlife/kingdoms/search/', WildlifeKingdomsViewSet.as_view({'get': 'search'}), name='wildlife-kingdoms-search'),
    
    path('wildlife/classes', WildlifeClassesViewSet.as_view({'get': 'list'}), name='wildlife-classes'),
    path('wildlife/classes/<int:pk>/', WildlifeClassesViewSet.as_view({'get': 'retrieve'}), name='wildlife-classes-retrieve'),
    path('wildlife/classes/search/', WildlifeClassesViewSet.as_view({'get': 'search'}), name='wildlife-classes-search'),
    
    path('wildlife/families', WildlifeFamiliesViewSet.as_view({'get': 'list'}), name='wildlife-families'),
    path('wildlife/families/<int:pk>/', WildlifeFamiliesViewSet.as_view({'get': 'retrieve'}), name='wildlife-families-retrieve'),
    path('wildlife/families/search/', WildlifeFamiliesViewSet.as_view({'get': 'search'}), name='wildlife-families-search'),
    
    path('wildlife/species', WildlifeSpeciesViewSet.as_view({'get': 'list'}), name='wildlife-species'),
    path('wildlife/species/<int:pk>/', WildlifeSpeciesViewSet.as_view({'get': 'retrieve'}), name='wildlife-species-retrieve'),
    path('wildlife/species/search/', WildlifeSpeciesViewSet.as_view({'get': 'search'}), name='wildlife-species-search'),
    
    path('wildlife/species/info/', WildlifeSpeciesInfoViewSet.as_view({'get': 'list'}), name='wildlife-species-info'),
    path('wildlife/species/info/<int:pk>/', WildlifeSpeciesInfoViewSet.as_view({'get': 'retrieve'}), name='wildlife-species-info-retrieve'),
    path('wildlife/species/info/search/', WildlifeSpeciesInfoViewSet.as_view({'get': 'search'}), name='wildlife-species-info-search'),
]
