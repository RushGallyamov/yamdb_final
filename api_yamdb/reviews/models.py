from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from reviews.validators import year_validator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name="имя", max_length=256)
    slug = models.SlugField(
        verbose_name="символьный код", max_length=50, unique=True
    )

    class Meta:
        verbose_name = "категория"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name="имя", max_length=256)
    slug = models.SlugField(
        verbose_name="символьный код", max_length=50, unique=True
    )

    class Meta:
        verbose_name = "жанр"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name="название", max_length=256)
    year = models.IntegerField(verbose_name="год", validators=[year_validator])
    description = models.CharField(
        verbose_name="описание", max_length=256, blank=True
    )
    genre = models.ManyToManyField(Genre, verbose_name="жанр", blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name="категория",
        related_name="titles",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "произведение"

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, verbose_name="автор", on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        verbose_name="произведение",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField(verbose_name="Отзыв")
    pub_date = models.DateTimeField(
        verbose_name="дата публикации", default=timezone.now, db_index=True
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="оценка",
        validators=[
            MinValueValidator(1, "оценка должна быть в интервале от 1 до 10"),
            MaxValueValidator(10, "оценка должна быть в интервале от 1 до 10"),
        ],
    )

    class Meta:
        verbose_name = "Отзыв"
        ordering = ("-pub_date", "score")
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique review"
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, verbose_name="автор", on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        verbose_name="отзыв",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField(
        verbose_name="Комментарий", help_text="Введите текст комментария"
    )
    pub_date = models.DateTimeField(
        verbose_name="дата публикации", default=timezone.now, db_index=True
    )

    class Meta:
        verbose_name = ("комментарий",)
        ordering = ("-pub_date",)
