from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from reviews.models import Category, Genre, Title


class GenresViewSet(viewsets.ModelViewSet):
    """VewSet для жанров"""
    queryset = Genre.objects.all()


class CategoriesViewSet(viewsets.ModelViewSet):
    """ViewSet для категорий"""
    queryset = Category.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.all()
