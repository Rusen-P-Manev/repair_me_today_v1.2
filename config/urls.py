from django.contrib import admin
from django.urls import path, include
from repairs.views import ViewClientInfo
from common.views import ViewDashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # dashboard
    path('', ViewDashboard.as_view(), name='dashboard'),

    # garage paths
    path('garage/', include('garage.urls', namespace='garage')),
    path('repairs/', include('repairs.urls', namespace='repairs')),
    path('invoicing/', include('invoicing.urls', namespace='invoicing')),

    # clients info path
    path('clientinfo/', ViewClientInfo.as_view(), name='public_client_info'),

    # accounts
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    