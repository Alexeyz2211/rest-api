from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('ticket/create/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/all/', views.TicketListView.as_view(), name='ticket-all'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('ticket/<int:pk>/message/', views.MessageListView.as_view(), name='ticket-message'),
    path('ticket/<int:pk>/status/', views.TicketStatusView.as_view(), name='ticket-status'),
    path('ticket/<int:pk>/assignee/', views.TicketAssigneeView.as_view(), name='ticket-assignee'),
]
