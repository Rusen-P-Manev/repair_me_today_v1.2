from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Service, RepairJob
from .serializers import ServiceSerializer, RepairJobStatusSerializer


class ServiceListCreateAPI(generics.ListCreateAPIView):
    queryset = Service.objects.all().order_by('name')
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Managers').exists() and not request.user.is_superuser:
            return Response(
                {"detail": "Нямате права да добавяте услуги в ценоразписа."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


class RepairStatusAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, access_token, *args, **kwargs):
        job = get_object_or_404(RepairJob, access_token=access_token)

        reg_num = request.query_params.get('reg_num')
        if reg_num and job.vehicle.vehicle_registration_number.lower() != reg_num.lower():
            return Response(
                {"error": "Несъответствие в регистрационния номер."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RepairJobStatusSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)