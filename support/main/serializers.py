from rest_framework import serializers

from . import models
from .models import Ticket


class TicketDetailSerializer(serializers.ModelSerializer):
    message_set = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Ticket
        fields = ('id', 'name', 'description', 'message_set')


class TicketUserListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    message_set = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Ticket
        fields = ('id', 'name', 'description', 'date_create', 'user', 'message_set')


class TicketSupportListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    message_set = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Ticket
        fields = ('id', 'name', 'description', 'date_create', 'user', 'status', 'message_set')


class TicketStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ticket
        fields = ('id', 'name', 'description', 'status')
        read_only_fields = ('id', 'name', 'description')


class MessageDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Message
        exclude = ('id', 'date', 'ticket')
