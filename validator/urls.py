from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("download-workbook/", views.download_workbook, name="download_workbook"),
    path("download-guide/", views.download_guide, name="download_guide"),
    path("audit-request/", views.audit_request, name="audit_request"),
    path("validation-dashboard/", views.validation_dashboard, name="validation_dashboard"),
]