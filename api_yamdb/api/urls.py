from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import TitleViewSet, GenresViewSet, CategoriesViewSet


router = DefaultRouter()

router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'categories', CategoriesViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router.urls)),
]
