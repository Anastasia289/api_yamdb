from rest_framework import serializers
from django.shortcuts import get_object_or_404

from users.models import User
from reviews.models import Reviews, Comments, Titles


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Неподходящий логин. "me" использовать запрещено.'
            )
        return value

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
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        """Пользователь не должен оставлять больше одного отзыва."""
        request = self.context['request']
        if request.method == "POST":
            title_id = self.context['view'].kwargs['title_id']
            title = get_object_or_404(Titles, pk=title_id)
            author = request.user
            if Reviews.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Одно произведение - один отзыв от одного автора!!!'
                )
            return data
        return data

    class Meta:
        fields = '__all__'
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comments."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='review'
    )

    class Meta:
        fields = '__all__'
        model = Comments