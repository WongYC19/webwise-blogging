from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("", views.LikeViewSet, basename='likes')

urlpatterns = router.urls