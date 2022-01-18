from rest_framework import generics
from rest_framework import permissions

from .permissions import IsOwner
from . import serializers
from . import models


class TicketCreateView(generics.CreateAPIView):
    serializer_class = serializers.TicketDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketListView(generics.ListAPIView):
    serializer_class = serializers.TicketListSerializer
    queryset = models.Ticket.objects.all()


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TicketDetailSerializer
    queryset = models.Ticket.objects.all()


class MessageDetailView(generics.ListCreateAPIView):
    serializer_class = serializers.MessageDetailSerializer
    permission_classes = [IsOwner | permissions.IsAdminUser]

    def get_queryset(self):
        return models.Message.objects.filter(ticket__id=self.kwargs['pk']).order_by('date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, ticket_id=self.kwargs['pk'])
