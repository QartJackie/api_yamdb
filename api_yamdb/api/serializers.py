from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Comment, User

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    
    class Meta:
        model = Review
        fields = ('id', 'title', 'author', 'pub_date', 'text', 'score', )
        read_only_fields = ('title', 'author', 'pub_date', )
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Вы уже оставили отзыв на данное произведение.'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'review', 'author', 'text', 'pub_date')
        read_only_fields = ('review', 'author', 'pub_date', )
        model = Comment