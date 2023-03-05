from django.urls import path
from .views import TokenCreateView

urlpatterns = [
    # ...
    path('jwt/create/', TokenCreateView.as_view(), name='token_create'),
]
