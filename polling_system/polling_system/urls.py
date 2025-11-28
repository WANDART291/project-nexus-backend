from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from core.viewsets import (
    ProjectViewSet, ProjectImageViewSet,
    RatingViewSet, CommentViewSet, CriteriaViewSet
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)

router.register(r"projects/(?P<project_pk>\d+)/images", ProjectImageViewSet, basename="project-images")
router.register(r"projects/(?P<project_pk>\d+)/ratings", RatingViewSet, basename="project-ratings")
router.register(r"projects/(?P<project_pk>\d+)/comments", CommentViewSet, basename="project-comments")
router.register(r"criteria", CriteriaViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    path('api/auth/jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),

    # --- UPDATED: API VERSIONING ADDED HERE ---
    # Old path: path("api/", include(router.urls)),
    # New path:
    path("api/v1/", include(router.urls)),
    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)