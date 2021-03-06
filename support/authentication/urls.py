from django.urls import path

from authentication.views import UserProfileListCreateView, UserDetailView

urlpatterns = [
    path('profiles/', UserProfileListCreateView.as_view(), name='profiles'),
    path('profiles/<int:pk>/', UserDetailView.as_view(), name='profiles-detail'),
]
