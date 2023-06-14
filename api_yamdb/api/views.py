from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from reviews.models import Reviews
from api.serializers import (
    SignUpSerializer,
    TokenSerializer,
    ReviewsSerializer,
    CommentsSerializer,
)
from api.permissions import IsAuthorOrReadOnly


class SignUpView(APIView):
    """
    Пользователь отправляет POST-запрос на добавление нового пользователя.
    YaMDB отправляет письмо с кодом подтверждения на почтовый адрес.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = get_random_secret_key()
        user.save()
        send_mail(
            'Код подтверждения',
            f'Код подтверждения: {confirmation_code}',
            'api_yamdb@yandex.ru',
            [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """
    Пользователь отправляет POST-запрос, в ответе на запрос ему приходит token.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST)
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class ReviewsViewSet(ModelViewSet):
    ...


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def get_queryset(self):
        """Возвращает queryset с комментариями выбранного отзыва."""
        commented_review = get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id')
        )
        return commented_review.comments.all()

    def perform_create(self, serializer):
        """Создание автором комментария к выбранному отзыву."""
        commented_review = get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=commented_review)
