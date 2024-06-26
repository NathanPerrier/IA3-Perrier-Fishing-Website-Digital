from apps.api.serializers import *
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes
from apps.wildlifeAPI.models import *
from rest_framework.permissions import IsAuthenticated


    
from rest_framework.authentication import TokenAuthentication

class UserPermission(permissions.BasePermission):
    """
    Permission check for authenticated users with a valid token.
    """
    authentication_classes = [TokenAuthentication]

    def has_permission(self, request, _):
        if request.method == 'GET':
            return True

        is_authenticated = request.user and request.user.is_authenticated
        has_permission = request.user.is_superuser or request.user.is_staff

        return (is_authenticated and has_permission)
    
class UserViewSet(viewsets.ViewSet):
    permission_classes = [UserPermission, IsAuthenticated]
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        users = User.objects.filter(username__icontains=query)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

class WildlifePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated
    
    
class WildlifeViewSet(viewsets.ViewSet):
    permission_classes = (WildlifePermission, )
    serializer_class = WildlifeKingdomsSerializer

    def list(self, request):
        """
        List all wildlife data.
        """
        kingdoms = WildlifeKingdoms.objects.all()
        classes = WildlifeClasses.objects.all()
        families = WildlifeFamilies.objects.all()
        species = WildlifeSpecies.objects.all()

        kingdoms_serializer = WildlifeKingdomsSerializer(kingdoms, many=True)
        classes_serializer = WildlifeClassesSerializer(classes, many=True)
        families_serializer = WildlifeFamiliesSerializer(families, many=True)
        species_serializer = WildlifeSpeciesSerializer(species, many=True)

        return Response({
            'kingdoms': kingdoms_serializer.data,
            'classes': classes_serializer.data,
            'families': families_serializer.data,
            'species': species_serializer.data,
        })
        
    
class WildlifeKingdomsViewSet(viewsets.ViewSet):
    permission_classes = (WildlifePermission, )
    serializer_class = WildlifeKingdomsSerializer
    """
    A simple ViewSet for viewing and retrieving wildlife kingdoms.
    """

    def list(self, request):
        """
        List all wildlife kingdoms.
        """
        kingdoms = WildlifeKingdoms.objects.all()
        serializer = WildlifeKingdomsSerializer(kingdoms, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a wildlife kingdom by its id.
        """
        kingdoms = WildlifeKingdoms.objects.filter(id=pk)
        serializer = WildlifeKingdomsSerializer(kingdoms, many=True)
        return Response(serializer.data)

    def search(self, request):
        """
        Search for wildlife kingdoms based on a query parameter.
        
        use: /wildlife/kingdoms/search/?q=keyword
        """
        query = request.query_params.get('q', '')
        kingdoms = WildlifeKingdoms.objects.filter(common_name__icontains=query)
        serializer = WildlifeKingdomsSerializer(kingdoms, many=True)
        return Response(serializer.data)

class WildlifeClassesViewSet(viewsets.ViewSet):
    permission_classes = (WildlifePermission, )
    serializer_class = WildlifeClassesSerializer
    """
    A simple ViewSet for viewing and retrieving wildlife classes.
    """

    def list(self, request):
        """
        List all wildlife classes.
        """
        classes = WildlifeClasses.objects.all()
        serializer = WildlifeClassesSerializer(classes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a wildlife class by its id.
        """
        classes = WildlifeClasses.objects.filter(id=pk)
        serializer = WildlifeClassesSerializer(classes, many=True)
        return Response(serializer.data)

    def search(self, request):
        """
        Search for wildlife classes based on a query parameter.
        
        use: /wildlife/classes/search/?q=keyword
        """
        query = request.query_params.get('q', '')
        classes = WildlifeClasses.objects.filter(common_name__icontains=query)
        serializer = WildlifeClassesSerializer(classes, many=True)
        return Response(serializer.data)
 
class WildlifeFamiliesViewSet(viewsets.ViewSet):
    permission_classes = (WildlifePermission, )
    serializer_class = WildlifeFamiliesSerializer
    """
    A simple ViewSet for viewing and retrieving wildlife families.
    """

    def list(self, request):
        """
        List all wildlife families.
        """
        families = WildlifeFamilies.objects.all()
        serializer = WildlifeFamiliesSerializer(families, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a wildlife family by its id.
        """
        families = WildlifeFamilies.objects.filter(id=pk)
        serializer = WildlifeFamiliesSerializer(families, many=True)
        return Response(serializer.data)

    def search(self, request):
        """
        Search for wildlife families based on a query parameter.
        
        use: /wildlife/families/search/?q=keyword
        """
        query = request.query_params.get('q', '')
        families = WildlifeFamilies.objects.filter(common_name__icontains=query)
        serializer = WildlifeFamiliesSerializer(families, many=True)
        return Response(serializer.data)
    
class WildlifeSpeciesViewSet(viewsets.ViewSet):
    permission_classes = (WildlifePermission, )
    serializer_class = WildlifeSpeciesSerializer
    """
    A simple ViewSet for viewing and retrieving wildlife species.
    """

    def list(self, request):
        """
        List all wildlife species.
        """
        species = WildlifeSpecies.objects.all()
        serializer = WildlifeSpeciesSerializer(species, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a wildlife species by its id.
        """
        species = WildlifeSpecies.objects.filter(id=pk)
        serializer = WildlifeSpeciesSerializer(species, many=True)
        return Response(serializer.data)

    def search(self, request):
        """
        Search for wildlife species based on a query parameter.
        
        use: /wildlife/species/search/?q=keyword
        """
        query = request.query_params.get('q', '')
        species = WildlifeSpecies.objects.filter(common_name__icontains=query)
        serializer = WildlifeSpeciesSerializer(species, many=True)
        return Response(serializer.data)
    
class WildlifeSpeciesInfoViewSet(viewsets.ViewSet):
    permission_classes = (WildlifePermission, )
    serializer_class = WildlifeSpeciesInfoSerializer
    """
    A simple ViewSet for viewing and retrieving wildlife species.
    """

    def list(self, request):
        """
        List all wildlife species.
        """
        species = WildlifeSpeciesInfo.objects.all()
        serializer = WildlifeSpeciesInfoSerializer(species, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a wildlife species by its id.
        """
        species = WildlifeSpeciesInfo.objects.filter(id=pk)
        serializer = WildlifeSpeciesInfoSerializer(species, many=True)
        return Response(serializer.data)

    def search(self, request):
        """
        Search for wildlife species based on a query parameter.
        
        use: /wildlife/species/info/search/?q=keyword
        """
        query = request.query_params.get('q', '')
        species = WildlifeSpeciesInfo.objects.filter(species__common_name__icontains=query)
        serializer = WildlifeSpeciesInfoSerializer(species, many=True)
        return Response(serializer.data)