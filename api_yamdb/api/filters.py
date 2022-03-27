import django_filters as filters
from django.db import models

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name="genre__slug")
    category = filters.CharFilter(field_name="category__slug")

    class Meta:
        model = Title
        fields = ("name", "year")
        filter_overrides = {
            models.CharField: {
                "filter_class": filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }
