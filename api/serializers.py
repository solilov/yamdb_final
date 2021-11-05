from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserCreateCustomSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации пользователя. """

    default_error_messages = {
        "cannot_create_user": "cannot_create_user"
    }

    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        try:
            return self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

    def perform_create(self, validated_data):
        with transaction.atomic():
            if validated_data['username'] == 'me':
                raise serializers.ValidationError(
                    'Использование данного имени запрещено'
                )
            user = User.objects.create_user(**validated_data)
            user.is_active = False
            user.save(update_fields=["is_active"])
            token = default_token_generator.make_token(user)
            send_mail('Тема письма',
                      f'Confirmation code {token}',
                      settings.MAIL,
                      [user.email],)
        return user


class UserSerializers(serializers.ModelSerializer):
    """ Сериализатор для вывода пользователей. """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')


class CustomUsernamedAndTokenSerializer(serializers.Serializer):
    """ Сериализатор для проверки кода
        и выписки токена для пользователя. """
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = self.initial_data.get("username", "")
        self.user = get_object_or_404(User, username=username)
        is_token_valid = self.context["view"].token_generator.check_token(
            self.user, self.initial_data.get("confirmation_code", "")
        )
        if is_token_valid:
            return super().validate(attrs)
        else:
            raise ValidationError(
                "invalid_confirmation_code"
            )


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор для категорий. """

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """ Сериализатор для жанров. """

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    """ Сериализатор для тайтлов. """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'category', 'genre', 'rating'
        )

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class TitleOtherSerializer(serializers.ModelSerializer):
    """ Сериализатор для тайтлов. """
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализатор для отзывов. """
    author = SlugRelatedField(queryset=User.objects.all(),
                              slug_field='username', required=False)

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'pub_date', 'author')
        read_only_fields = ('title', 'author')

    def create(self, validated_data):
        title = validated_data['title']
        author = validated_data['author']
        unique_object = Review.objects.filter(
            title=title,
            author=author
        )
        if unique_object:
            raise ValidationError(
                'Невозможно заново написать отзыв'
            )
        return Review.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """ Сериализатор для комментариев. """
    author = SlugRelatedField(queryset=User.objects.all(),
                              slug_field='username', required=False)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review', 'author')
