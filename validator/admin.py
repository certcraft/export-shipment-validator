from django.contrib import admin
from .models import DownloadLead, AuditRequest, DownloadEvent


@admin.register(DownloadLead)
class DownloadLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company_or_role", "created_at")
    search_fields = ("name", "email", "company_or_role")
    ordering = ("-created_at",)


@admin.register(AuditRequest)
class AuditRequestAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "shipment_reference",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("email", "shipment_reference")
    ordering = ("-created_at",)

@admin.register(DownloadEvent)
class DownloadEventAdmin(admin.ModelAdmin):
    list_display = ("session_key", "downloaded_at")
    ordering = ("-downloaded_at",)