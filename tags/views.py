# from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tag, TaggedItem
from .serializers import TagSerializer, TaggedItemSerializer
from .permissions import IsAdminOrReadOnly
from .filters import TaggedItemFilter

# Create your views here.
class TagViewSet(ListCreateAPIView, ViewSet):
    """ Allow user to list and create tags include filtering and search capabilities """
    queryset = Tag.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['label']
    ordering_fields = ['label']
    ordering = ['label']
class TaggedItemViewSet(ListCreateAPIView, DestroyAPIView, RetrieveAPIView, ViewSet):
    """ Allow user to create/read list and details/update and delete the relationship of tag and tagged item """
    # The ordering by "tag" causes duplication in list viewset, for postgres it has to include 'id' to use the distinct method (Source: ChatGPT)
    queryset = TaggedItem.objects.all().distinct('id')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TaggedItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TaggedItemFilter
    ordering_fields = ['id', 'tags', 'modified_date'] # make sure to include the 'id' field in the ordering fields
    ordering = ['id', 'tags', '-modified_date'] # make sure to include the 'id' field in the ordering fields

