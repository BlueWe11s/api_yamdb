from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import Users
from users.validators import validate_username

User = Users


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True, max_length=150,
        validators=(validate_username, UnicodeUsernameValidator())
    )

    def validate(self, data):
        try:
            User.objects.get_or_create(
                username=data.get('username'),
                email=data.get('email')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Одно из полей username или email уже занято'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(),
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'pub_date', 'title', 'score')
        read_only_fields = ('author', 'title', 'pub_date')

    def validate(self, data):
        title_id = self.context.get('title_id')
        if self.context['request'].method == 'POST' and Review.objects.filter(
            title=title_id, author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.')
        return data

    def create(self, validated_data):
        return Review.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(),
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date', 'review')
        read_only_fields = ('author', 'review', 'pub_date')

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug'
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug'
        )


class ListDetailedTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = Review.objects.filter(title=obj).aggregate(
            Avg('score'))['score__avg']
        if rating:
            return int(rating)
        return None

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'genre',
            'category',
            'description',
            'rating'
        )


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'category',
            'genre',
            'name',
            'year',
            'description'
        )
