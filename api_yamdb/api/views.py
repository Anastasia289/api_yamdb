from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from .serializers import SignUpSerializer, TokenSerializer, CategorySerializer, GenreSerializer, TitlesGetSerializer, TitlesChangeSerializer
from reviews.models import Category, Genre, Titles
from api.permissions import IsAdminOrSuperUserOrReadOnly



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


class CategoryViewSet(viewsets.ModelViewSet):  # админ или только читать
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet): # админ или только читать
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet): # админ или только читать
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    queryset = Titles.objects.all()
    # serializer_class = TitlesGetSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializer
        return TitlesChangeSerializer

