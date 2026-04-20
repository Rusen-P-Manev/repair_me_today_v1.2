from rest_framework import serializers
from .models import Service, RepairJob


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'price']


class RepairJobStatusSerializer(serializers.ModelSerializer):
    vehicle_make = serializers.CharField(source='vehicle.make', read_only=True)
    vehicle_model = serializers.CharField(source='vehicle.model', read_only=True)
    registration = serializers.CharField(source='vehicle.vehicle_registration_number', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = RepairJob
        fields = [
            'access_token', 'registration', 'vehicle_make',
            'vehicle_model', 'status', 'status_display',
            'total_amount', 'updated_at'
        ]

    def get_total_amount(self, obj):
        if hasattr(obj, 'invoice'):
            return str(obj.invoice.total_amount)
        return "В процес на изчисляване"