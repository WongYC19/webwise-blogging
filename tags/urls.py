from rest_framework.routers import DefaultRouter
from .views import TagViewSet, TaggedItemViewSet

routers = DefaultRouter()

routers.register("", TagViewSet, basename="tag")
routers.register("item", TaggedItemViewSet, basename="taggeditem")

urlpatterns = routers.urls