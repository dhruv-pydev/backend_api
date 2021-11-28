from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework import serializers
from main.models import Question


class QuestionFilter(FilterSet):
    tags = filters.CharFilter(field_name="tags", method="get_tags")

    def get_tags(self, queryset, name, value):
        tags = value.split(",")
        return queryset.filter(tags__title__in=tags)

    class Meta:
        model = Question
        fields = ["user__id", "user__user__username", "tags"]
