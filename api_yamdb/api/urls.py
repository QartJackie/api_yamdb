from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoriesViewSet, CommentViewSet, GenresViewSet,
    ReviewViewSet, TitleViewSet
)
from users import urls as users_urls


router_1 = routers.DefaultRouter()

router_1.register(r'titles', TitleViewSet, basename='titles')
router_1.register(r'genres', GenresViewSet, basename='genres')
router_1.register(r'categories', CategoriesViewSet, basename='categories')
router_1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews',
)
router_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments',
)

urlpatterns = [
    path('v1/', include(router_1.urls)),
    path('v1/', include(users_urls)),
]
