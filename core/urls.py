"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("", include("home.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("apps.api.urls")),
    path("users/", include("apps.users.urls")),
    path('social/', include('social_django.urls', namespace='social')),  
    path('species/', include('apps.wildlifeAPI.urls')),
    path("tasks/", include("apps.tasks.urls")),
    path("social/", include("apps.social.urls")),
    path('microsoft/', include('apps.microsoft_auth.urls', namespace='microsoft_auth')),
    path("club/", include("apps.club.urls")),
    path('api/docs/redoc/' , SpectacularRedocView.as_view(url_name='schema'), name='redoc'), 
    path('api/docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/'      , SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("__reload__/", include("django_browser_reload.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
] 

urlpatterns += static(settings.CELERY_LOGS_URL, document_root=settings.CELERY_LOGS_DIR)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'