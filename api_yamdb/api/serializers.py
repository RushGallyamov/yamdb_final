from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)


class TitleInputSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )
        read_only_fields = ("rating",)


class TitleOutputSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        read_only_fields = ("rating",)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "author", "text", "score", "pub_date")

    def validate(self, data):
        title = get_object_or_404(
            Title.objects.prefetch_related(
                models.Prefetch(
                    "reviews", queryset=Review.objects.select_related("author")
                )
            ),
            id=self.context["view"].kwargs["title_id"],
        )
        author = self.context["request"].user
        if not self.instance and title.reviews.filter(author=author).exists():
            raise serializers.ValidationError(
                f'Ревью на "{title}" от "{author}" уже существует'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_username(value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                f'Имя пользователя "{value}" запрещено!'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f'Пользователь с именем "{value}" уже существует'
            )
        return value

    @staticmethod
    def validate_email(value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует"
            )
        return value

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs["username"]
        request_confirmation_code = attrs["confirmation_code"]
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != request_confirmation_code:
            raise serializers.ValidationError("Неверный confirmation_code!")
        return attrs
