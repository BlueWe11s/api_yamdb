from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели отзыва
    """
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
    """
    Сериализатор для модели комментария
    """
    author = serializers.SlugRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(),
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date', 'review')
        read_only_fields = ('author', 'review', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели категории
    """
    class Meta:
        model = Category
        fields = (
            'name',
            'slug'
        )


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели жанра
    """
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug'
        )


class ListDetailedTitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели подсчета среднего рейтинга
    """
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

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
    """
    Сериализатор для модели произведения
    """
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
