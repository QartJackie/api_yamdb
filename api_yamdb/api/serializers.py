import datetime as dt
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title


class CustomSlugRelatedField(serializers.SlugRelatedField):
    """Кастомный сериализатор с репрезентацией."""
    def to_representation(self, obj):
        return {
            "name": obj.name,
            "slug": obj.slug
        }


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        """Настройка сериализатора."""
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        """Настройка сериализатора."""
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""
    category = CustomSlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), many=False
    )
    genre = CustomSlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        """Настройка сериализатора."""
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        """Валидация года выпуска произведения."""

        current_year = dt.date.today().year

        if not 0 < value <= current_year:
            raise serializers.ValidationError(
                'Размещение не вышедшего материала не возможно.'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'author', 'pub_date', 'text', 'score', )
        read_only_fields = ('title', 'author', 'pub_date', )

    def validate(self, data):
        request = self.context['request']
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if (request.method == 'POST'
            and Review.objects.filter(
                title=title, author=request.user).exists()):
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'review', 'author', 'text', 'pub_date')
        read_only_fields = ('review', 'author', 'pub_date', )
        model = Comment
