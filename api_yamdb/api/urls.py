from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpView, TokenView

router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
]
