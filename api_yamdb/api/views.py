from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Comment, Review
from .serializers import ReviewSerializer, CommentSerializer
from .pagination import ReviewPagination
from .permissions import AuthorAdminModerOrReadOnly


class GenresViewSet(viewsets.ModelViewSet):
    """VewSet для жанров"""
    queryset = Genre.objects.all()


class CategoriesViewSet(viewsets.ModelViewSet):
    """ViewSet для категорий"""
    queryset = Category.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
#    permission_classes = [AuthorAdminModerOrReadOnly, ]
#    permission_classes = [AllowAny, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=Title.objects.get(id=self.kwargs.get('title_id')))


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [AuthorAdminModerOrReadOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=Review.objects.get(id=self.kwargs.get('review_id')))