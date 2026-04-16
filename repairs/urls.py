from django.urls import path
from . import views

app_name = 'repairs'

urlpatterns = [
# repairs
    path('jobs/', views.ViewRepairJobList.as_view(), name='job_list'),
    path('jobs/add/', views.ViewRepairJobCreate.as_view(), name='job_create'),
    path('jobs/<int:pk>/', views.ViewRepairJobDetail.as_view(), name='job_detail'),
    path('jobs/<int:pk>/edit/', views.ViewRepairJobUpdate.as_view(), name='job_update'),
    path('jobs/<int:pk>/delete/', views.ViewRepairJobDelete.as_view(), name='job_delete'),
    path('jobs/<int:pk>/update-status/', views.ViewRepairJobStatusUpdate.as_view(), name='job_status_update'),

# parts
    path('jobs/<int:job_id>/parts/add/', views.ViewPartOrderCreate.as_view(), name='part_create'),
    path('parts/<int:pk>/delete/', views.ViewPartOrderDelete.as_view(), name='part_delete'),
    path('parts/<int:pk>/update/', views.ViewPartOrderUpdate.as_view(), name='part_update'),
    path('jobs/<int:job_id>/services/add/', views.ViewRepairServiceCreate.as_view(), name='service_create'),
    path('services/<int:pk>/delete/', views.ViewRepairServiceDelete.as_view(), name='service_delete'),

# service catalog
    path('catalog/', views.ViewServiceCatalogList.as_view(), name='service_catalog_list'),
    path('catalog/add/', views.ViewServiceCatalogCreate.as_view(), name='service_catalog_create'),
    path('catalog/<int:pk>/edit/', views.ViewServiceCatalogUpdate.as_view(), name='service_catalog_update'),
    path('catalog/<int:pk>/delete/', views.ViewServiceCatalogDelete.as_view(), name='service_catalog_delete'),

# archives
    path('archive/', views.ViewRepairArchiveList.as_view(), name='archive_list'),
    path('archive/<int:pk>/invoice/', views.ViewArchivedInvoiceDetail.as_view(), name='archived_invoice'),
]