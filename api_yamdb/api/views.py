from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import (IsAdminOrSuperUserOrReadOnly,
                             IsSuperUserIsAdminIsModerIsAuthor)
from api.serializers import (CategorySerializer, CommentsSerializer,
                             GenreSerializer, ReviewsSerializer,
                             SignUpSerializer, TitlesChangeSerializer,
                             TitlesGetSerializer, TokenSerializer,
                             UserSerializer)

from reviews.models import Category, Genre, Reviews, Titles
from users.models import User


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


class UserViewSet(viewsets.ModelViewSet):
    """Управление пользователями."""
    queryset = User.objects.all()
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def profile(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    queryset = Titles.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializer
        return TitlesChangeSerializer


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminIsModerIsAuthor,
    )

    def get_queryset(self):
        """Возвращает queryset с отзывами выбранного произведения."""
        reviewed_title = get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id')
        )
        return reviewed_title.reviews.all()

    def perform_create(self, serializer):
        """Создание автором комментария к выбранному отзыву."""
        reviewed_title = get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=reviewed_title)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminIsModerIsAuthor,
    )

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
