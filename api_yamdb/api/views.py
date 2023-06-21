from api import permissions, serializers
from api.mixins import CreateListDestroyViewSet
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter


class SignUpView(APIView):
    """
    Пользователь отправляет POST-запрос на добавление нового пользователя.
    YaMDB отправляет письмо с кодом подтверждения на почтовый адрес.
    """
    queryset = User.objects.all()
    serializer_class = serializers.SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(**serializer.validated_data)
        except IntegrityError:
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = get_random_secret_key()
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
        serializer = serializers.TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Управление пользователями."""
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,
                          permissions.IsAdminOrStuffPermission,)
    serializer_class = serializers.UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        url_path='me',
        permission_classes=(IsAuthenticated,))
    def profile(self, request):
        if request.method == 'PATCH':
            serializer = serializers.UserWithoutRoleSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all().order_by('name')
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.IsAdminOrReadOnly,)
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):

    queryset = Genre.objects.all().order_by('name')
    serializer_class = serializers.GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitlesGetSerializer
        return serializers.TitlesChangeSerializer


class ReviewsViewSet(ModelViewSet):
    serializer_class = serializers.ReviewsSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        permissions.IsSuperUserIsAdminIsModerIsAuthor,
    )

    def get_queryset(self):
        """Возвращает queryset с отзывами выбранного произведения."""
        reviewed_title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return reviewed_title.reviews.all()

    def perform_create(self, serializer):
        """Создание автором комментария к выбранному отзыву."""
        reviewed_title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=reviewed_title)


class CommentsViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = serializers.CommentsSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        permissions.IsSuperUserIsAdminIsModerIsAuthor,
    )

    def get_queryset(self):
        """Возвращает queryset с комментариями выбранного отзыва."""
        commented_review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return commented_review.comments.all()

    def perform_create(self, serializer):
        """Создание автором комментария к выбранному отзыву."""
        commented_review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=commented_review)
