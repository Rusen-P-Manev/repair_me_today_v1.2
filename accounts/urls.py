from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, RegisterClientView, ClientProfileView, AddDemoDataView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterClientView.as_view(), name='register'),
    path('profile/', ClientProfileView.as_view(), name='client_profile'),
    path('add-demo/', AddDemoDataView.as_view(), name='add_demo_data'),
]