
from rest_framework import viewsets, mixins


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Кастомный ViewSet с разрешениями:
    Получения списка объектов,
    Создание нового объекта,
    Удаление объекта.
    """
    pass
