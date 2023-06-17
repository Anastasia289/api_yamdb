from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex="^[\\w.@+-]+",
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],)

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Нельзя использовать 'me'.")
        return value

    def create(self, validated_data):
        if self.is_valid():
            user, created = User.objects.get_or_create(**validated_data)
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


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

    def create(self, validated_data):
        existing_username = User.objects.filter(
            username=validated_data.get('username')
        ).first()
        existing_email = User.objects.filter(
            email=validated_data.get('email')
        ).first()
        if any([existing_username, existing_email]):
            if existing_username == existing_email:
                return existing_username
            raise serializers.ValidationError(
                'Данный Email уже существует. Выберите другой.'
            )
        return User.objects.create(**validated_data)

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
            title = get_object_or_404(Title, pk=title_id)
            author = request.user
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Одно произведение - один отзыв от одного автора!!!'
                )
            return data
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comments."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesGetSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlesChangeSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'
