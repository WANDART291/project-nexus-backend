from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import JsonResponse

# Define a simple home view directly here
def home(request):
    return JsonResponse({
        "message": "Welcome to the Project Nexus API 🚀",
        "status": "Live",
        "endpoints": {
            "projects": "/api/v1/projects/",
            "admin": "/admin/",
            "documentation": "/api/docs/"
        }
    })

urlpatterns = [
    # The Homepage (Root URL)
    path('', home),

    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/v1/', include('core.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    
    # Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]