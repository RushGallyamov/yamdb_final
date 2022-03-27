import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .permissions import AdminOrReadOnly, AuthorOrStaffOrReadOnly, UserOrAdmin
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleInputSerializer,
    TitleOutputSerializer,
    UserSerializer,
    UserTokenSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    search_fields = ("name",)
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    search_fields = ("name",)
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.select_related("category")
        .prefetch_related("genre")
        .annotate(rating=models.Avg("reviews__score"))
    )
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TitleInputSerializer
        else:
            return TitleOutputSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrStaffOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            review__title_id=self.kwargs.get("title_id"),
            review_id=self.kwargs.get("review_id"),
        ).select_related("author")

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs["review_id"],
            title__id=self.kwargs["title_id"],
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrStaffOrReadOnly,)

    def get_queryset(self):
        return Review.objects.filter(
            title_id=self.kwargs["title_id"]
        ).select_related("author")

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        serializer.save(author=self.request.user, title=title)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    pagination_class = PageNumberPagination
    permission_classes = (UserOrAdmin,)

    def perform_create(self, serializer):
        return super().perform_create(serializer)

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
        else:
            data = {k: request.data[k] for k in request.data if k != "role"}
            serializer = self.get_serializer(
                request.user, data=data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class TokenClaimViewSet(APIView):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def _get_confirmation_code():
        return str(uuid.uuid4())

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = self._get_confirmation_code()
        user = serializer.save(confirmation_code=confirmation_code)
        send_mail(
            "Confirmation code",
            confirmation_code,
            settings.EMAIL_FROM,
            [user.email],
        )
        return Response(request.data)


class UserTokenViewSet(APIView):
    serializer_class = UserTokenSerializer
    permission_classes = []

    @classmethod
    def get_token(cls, user):
        return AccessToken.for_user(user)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        user = get_object_or_404(User, username=username)
        token = self.get_token(user)
        user.remove_confirmation_code()
        return Response({"token": str(token)})
