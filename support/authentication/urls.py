from django.urls import path

from .views import UserProfileListCreateView, UserDetailView

urlpatterns = [
    path("all-profiles/", UserProfileListCreateView.as_view()),
    path("profile/<int:pk>", UserDetailView.as_view()),
]
