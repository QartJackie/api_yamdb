from django.urls import include, path
from rest_framework import routers

from api.views import TitleViewSet, GenresViewSet, CategoriesViewSet
from api.views import ReviewViewSet, CommentViewSet


router = routers.DefaultRouter()

router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='reviews',
                )
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)


urlpatterns = [
    path('v1/', include(router.urls)),
]
