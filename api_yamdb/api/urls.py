from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpView, TokenView, TitlesViewSet, GenreViewSet, CategoryViewSet

router_v1 = DefaultRouter()

router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
]
