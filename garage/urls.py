from django.urls import path
from . import views

app_name = 'garage'

urlpatterns = [

# clients
    path('clients/', views.ViewClientList.as_view(), name='client_list'),
    path('clients/add/', views.ViewClientCreate.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', views.ViewClientUpdate.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ViewClientDelete.as_view(), name='client_delete'),

# vehicles
    path('vehicles/', views.ViewVehicleList.as_view(), name='vehicle_list'),
    path('vehicles/add/', views.ViewVehicleCreate.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.ViewVehicleUpdate.as_view(), name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.ViewVehicleDelete.as_view(), name='vehicle_delete'),
]