from rest_framework import serializers

from users.models import User
from reviews import models


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Titles
        fields = '__all__'
