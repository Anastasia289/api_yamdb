from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'
router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewsViewSet,
    basename='review'
)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet,
    basename='comments'
)

router_v1.register('titles', views.TitlesViewSet, basename='titles')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.SignUpView.as_view()),
    path('v1/auth/token/', views.TokenView.as_view()),
]
