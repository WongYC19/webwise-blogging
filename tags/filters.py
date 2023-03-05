# from rest_framework.filters import SearchFilter, OrderingFilter, FilterSet
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import filters, FilterSet
from django_filters import ModelChoiceFilter

from .models import TaggedItem

class TaggedItemFilter(FilterSet):
    created_before = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    type = filters.CharFilter(field_name='content_type', method='filter_content_type')

    class Meta:
        model = TaggedItem
        fields = ['type', 'created_before', 'created_after']

    def filter_content_type(self, queryset, name, value):
        return queryset.filter(content_type__model__icontains=value)