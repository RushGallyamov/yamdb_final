from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title

EMPTY = "-пусто-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    empty_value_display = EMPTY


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    empty_value_display = EMPTY


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "name",
        "year",
        "description",
    )
    empty_value_display = EMPTY


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "author",
        "score",
        "pub_date",
        "title_id",
    )

    empty_value_display = EMPTY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "author", "pub_date", "review")
    fields = ("text", "review", "author", "pub_date")
    empty_value_display = EMPTY
