from django.db.models import Q
from django_filters.rest_framework import filters, FilterSet

from .models import Post, Comment

class PostFilter(FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    modified_date_after = filters.DateFilter(field_name='modified_date', lookup_expr='gte') # modified_date_after=YYYY-MM-DD&modified_date_before=YYYY-MM-DD
    modified_date_before = filters.DateFilter(field_name='modified_date', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['title', 'modified_date_after', 'modified_date_before']

class CommentFilter(FilterSet):
    created_date_after = filters.DateFilter(field_name='created_date', lookup_expr='gte')  # created_date_after=YYYY-MM-DD&created_date_before=YYYY-MM-DD
    created_date_before = filters.DateFilter(field_name='created_date', lookup_expr='lte')
    name = filters.CharFilter(method='filter_user')
    content = filters.CharFilter(lookup_expr='icontains')

    def filter_user(self, queryset, name, value):
        """
            Filter by user with the following options: first name or last name: ?name=John
        """
        return queryset.filter(Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value))

    class Meta:
        model = Comment
        fields = ['name', 'content', 'created_date_after', 'created_date_before']