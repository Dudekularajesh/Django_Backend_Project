from django.urls import path
from .views import ProductSuggestAPIView

urlpatterns = [
    path("api/search/suggest/", ProductSuggestAPIView.as_view()),
]
