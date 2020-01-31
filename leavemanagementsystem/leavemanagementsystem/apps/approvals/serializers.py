from rest_framework import serializers
from .models import AcceptedNotifications


class AcceptedNotificationsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)

    class Meta:
        model = AcceptedNotifications
        fields = '__all__'
