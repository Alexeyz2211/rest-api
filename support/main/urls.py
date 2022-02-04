from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('ticket/create/', views.TicketCreateView.as_view()),
    path('ticket/all/', views.TicketListView.as_view()),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view()),
    path('ticket/<int:pk>/message/', views.MessageListView.as_view()),
    path('ticket/<int:pk>/status/', views.TicketStatusView.as_view()),
    path('ticket/<int:pk>/assignee/', views.TicketAssigneeView.as_view()),
]
