from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.pagination import ReviewPagination
"""
Ниже инпортированы пермишены из апи и юзерс.
Нужно выбрать, откуда будем ипортировать. Еслии это юзерс,
то нужны пермишены под доки, данные не совсем подходят.
"""
from api.permissions import AuthorAdminModerOrReadOnly
from users.permissions import IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer)
from reviews.models import Category, Genre, Title, Comment, Review


class CategoriesViewSet(viewsets.ModelViewSet):
    """ViewSet для категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = ReviewPagination
    # permissions and filters


class GenresViewSet(viewsets.ModelViewSet):
    """VewSet для жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    # permissions and filters


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
#    permission_classes = [AuthorAdminModerOrReadOnly, ]
#    permission_classes = [AllowAny, ]

    def get_queryset(self):
        """Получение кверисета с произведениями."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        """Функция создания ревью."""
        serializer.save(author=self.request.user,
                        title=Title.objects.get(id=self.kwargs.get('title_id')))


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [AuthorAdminModerOrReadOnly, ]

    def get_queryset(self):
        """Получение кверисета с ревью."""
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        """Создание комментария."""
        serializer.save(author=self.request.user,
                        review=Review.objects.get(id=self.kwargs.get('review_id')))