from apps.api.serializers import ProductSerializer, UserSerializer
from apps.common.models import Product
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions


class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (ProductPermission, )
    lookup_field = 'id'
    
class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated and request.user.is_superuser or request.user.is_staff

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (UserPermission, )
    lookup_field = 'id'