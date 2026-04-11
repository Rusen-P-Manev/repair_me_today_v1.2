from django.urls import path
from . import views

app_name = 'invoicing'

urlpatterns = [
    path('list/', views.ViewInvoiceList.as_view(), name='invoice_list'),
    path('create/<int:job_id>/', views.ViewInvoiceCreate.as_view(), name='invoice_create'),
    path('<int:pk>/', views.ViewInvoiceDetail.as_view(), name='invoice_detail'),
    path('<int:pk>/pay/', views.ViewInvoiceMarkPaid.as_view(), name='invoice_mark_paid'),
]