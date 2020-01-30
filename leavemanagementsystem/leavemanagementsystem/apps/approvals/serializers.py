from rest_framework import serializers
from .models import AcceptedNotifications, ApproveNotifications


class AcceptedNotificationsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)

    class Meta:
        model = AcceptedNotifications
        fields = '__all__'


class ApproveNotificationsNotificationsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)

    class Meta:
        model = ApproveNotifications
        fields = '__all__'
