from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.api.views import ProductViewSet, UserViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
