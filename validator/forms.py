from django import forms
from .models import AuditRequest


class AuditRequestForm(forms.ModelForm):
    class Meta:
        model = AuditRequest
        fields = [
            "email",
            "shipment_reference",
            "invoice_file",
            "packing_list_file",
            "bl_file",
            "notes",
        ]

        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": "you@company.com"
            }),
            "shipment_reference": forms.TextInput(attrs={
                "placeholder": "e.g. EXP-2026-001"
            }),
            "notes": forms.Textarea(attrs={
                "placeholder": "Tell us anything important about this shipment...",
                "rows": 4
            }),
        }