from django.db import models


class DownloadLead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    company_or_role = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class AuditRequest(models.Model):
    STATUS_CHOICES = [
        ("NEW", "New"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
    ]

    email = models.EmailField()
    shipment_reference = models.CharField(max_length=100, blank=True)

    invoice_file = models.FileField(upload_to="audit_requests/invoices/")
    packing_list_file = models.FileField(upload_to="audit_requests/packing_lists/")
    bl_file = models.FileField(upload_to="audit_requests/bills_of_lading/")

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="NEW",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.shipment_reference}"

class DownloadEvent(models.Model):
    session_key = models.CharField(max_length=100, blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Workbook download - {self.downloaded_at}"