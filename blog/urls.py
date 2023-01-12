from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('posts', views.PostViewSet, basename='posts')
router.register('profile', views.UserProfileViewSet)

posts_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register('comments', views.CommentViewSet, basename='post-comments')

urlpatterns = router.urls + posts_router.urls