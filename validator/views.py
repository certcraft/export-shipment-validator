from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import AuditRequestForm
from .models import DownloadEvent, DownloadLead, AuditRequest

def home(request):
    return render(request, "validator/home.html")


def download_workbook(request):
    file_path = Path(settings.BASE_DIR) / "downloads" / "Export Shipment Control Workbook FINAL v7.xlsx"

    if not request.session.session_key:
        request.session.save()

    DownloadEvent.objects.create(
        session_key=request.session.session_key or ""
    )

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename="Export Shipment Control Workbook FINAL v7.xlsx"
    )

def download_guide(request):
    file_path = Path(settings.BASE_DIR) / "downloads" / "Export_Shipment_Control_User_Guide.pdf"

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename="Export_Shipment_Control_User_Guide.pdf",
    )


def audit_request(request):
    if request.method == "POST":
        form = AuditRequestForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(
                request,
                "validator/audit_success.html"
            )
    else:
        form = AuditRequestForm()

    return render(
        request,
        "validator/audit_request.html",
        {"form": form}
    )
@login_required
def validation_dashboard(request):
    download_count = DownloadEvent.objects.count()
    lead_count = DownloadLead.objects.count()
    audit_count = AuditRequest.objects.count()

    new_audits = AuditRequest.objects.filter(status="NEW").count()
    processing_audits = AuditRequest.objects.filter(status="PROCESSING").count()
    completed_audits = AuditRequest.objects.filter(status="COMPLETED").count()

    return render(
        request,
        "validator/validation_dashboard.html",
        {
            "download_count": download_count,
            "lead_count": lead_count,
            "audit_count": audit_count,
            "new_audits": new_audits,
            "processing_audits": processing_audits,
            "completed_audits": completed_audits,
        },
    )