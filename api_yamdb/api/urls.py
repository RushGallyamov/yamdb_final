from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    TokenClaimViewSet,
    UserTokenViewSet,
    UserViewSet,
)

app_name = "api"

router = routers.DefaultRouter()
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)
router.register("users", UserViewSet)


urlpatterns = [
    path("v1/auth/signup/", TokenClaimViewSet.as_view()),
    path("v1/auth/token/", UserTokenViewSet.as_view()),
    path("v1/", include(router.urls)),
]
