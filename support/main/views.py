from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from authentication.models import User
from . import serializers
from . import models
from .permissions import IsOwner
from .tasks import send_email_notice


class TicketCreateView(generics.CreateAPIView):
    serializer_class = serializers.TicketDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketListView(generics.ListAPIView):

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Ticket.objects.all()
        return models.Ticket.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return serializers.TicketSupportListSerializer
        return serializers.TicketUserListSerializer


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TicketDetailSerializer
    queryset = models.Ticket.objects.all()


class TicketStatusView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.TicketStatusSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = models.Ticket.objects.all()


class TicketAssigneeView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.TicketAssigneeSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = models.Ticket.objects.all()

    def perform_update(self, serializer):
        support_id = self.request.data['assignee']
        inform_message = f'{User.objects.get(pk=support_id)} assigned for your Ticket'
        if User.objects.get(pk=support_id).is_staff:
            serializer.save()
            send_email_notice.delay(
                User.objects.get(tickets=serializer.data['id']).id,
                self.request.user.username,
                inform_message
            )
            message = models.Message(
                text=inform_message,
                ticket_id=self.kwargs['pk'],
                user_id=support_id
            )
            message.save()
        else:
            raise ValidationError('The assignee must be an Employee')


class MessageListView(generics.ListCreateAPIView):
    serializer_class = serializers.MessageDetailSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Message.objects.filter(ticket_id=self.kwargs['pk']).order_by('date')
        ticket = get_object_or_404(models.Ticket, pk=self.kwargs['pk'], user=self.request.user)
        self.check_object_permissions(self.request, ticket)
        return models.Message.objects.filter(ticket=ticket).order_by('date')

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            return serializer.save(user=self.request.user, ticket_id=self.kwargs['pk'])
        ticket = get_object_or_404(models.Ticket, pk=self.kwargs['pk'], user=self.request.user)
        self.check_object_permissions(self.request, ticket)
        return serializer.save(user=self.request.user, ticket=ticket)
