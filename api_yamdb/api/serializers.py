from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews import models
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    username = serializers.RegexField(
        regex="^[\\w.@+-]+",
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserWithoutRoleSerializer(UserSerializer):
    role = serializers.StringRelatedField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=150,
        validators=[
            UnicodeUsernameValidator(),
            RegexValidator(
                regex=r'^(?!me$).*$',
                message='Неподходящий логин. "me" использовать запрещено.',
            ),
        ],
    )
    email = serializers.EmailField(max_length=254)

    def validate(self, validated_data):
        if (
                User.objects.filter(email=validated_data['email']).exists()
                and User.objects.get(email=validated_data['email']).username
                != validated_data['username']
        ):
            raise serializers.ValidationError(
                'Данный username уже существует. Выберите другой.')
        if (
                User.objects.filter(
                    username=validated_data['username']).exists()
                and User.objects.get(username=validated_data['username']).email
                != validated_data['email']
        ):
            raise serializers.ValidationError(
                'Данный Email уже существует. Выберите другой.',)
        return validated_data

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        """Пользователь не должен оставлять больше одного отзыва."""
        request = self.context['request']
        if request.method == "POST":
            title_id = self.context['view'].kwargs['title_id']
            title = get_object_or_404(models.Title, pk=title_id)
            author = request.user
            if models.Review.objects.filter(title=title,
                                            author=author).exists():
                raise serializers.ValidationError(
                    'Одно произведение - один отзыв от одного автора!!!'
                )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = models.Review


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comments."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = models.Comments


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('name', 'slug')


class TitlesGetSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Title
        fields = '__all__'


class TitlesChangeSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Category.objects.all()
    )

    class Meta:
        model = models.Title
        fields = '__all__'
