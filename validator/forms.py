from django import forms
from .models import AuditRequest


class AuditRequestForm(forms.ModelForm):
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".xlsx",
        ".xls",
        ".docx",
        ".jpg",
        ".jpeg",
        ".png",
    }

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

    def _validate_document(self, uploaded_file, label):
        if not uploaded_file:
            return uploaded_file

        if uploaded_file.size > self.MAX_FILE_SIZE:
            raise forms.ValidationError(
                f"{label} must be 10 MB or smaller."
            )

        filename = uploaded_file.name.lower()

        if "." not in filename:
            raise forms.ValidationError(
                f"{label} must have a valid file extension."
            )

        extension = "." + filename.rsplit(".", 1)[1]

        if extension not in self.ALLOWED_EXTENSIONS:
            raise forms.ValidationError(
                f"{label}: unsupported file type. "
                "Use PDF, Excel, Word, JPG, JPEG, or PNG."
            )

        return uploaded_file

    def clean_invoice_file(self):
        return self._validate_document(
            self.cleaned_data.get("invoice_file"),
            "Commercial Invoice",
        )

    def clean_packing_list_file(self):
        return self._validate_document(
            self.cleaned_data.get("packing_list_file"),
            "Packing List",
        )

    def clean_bl_file(self):
        return self._validate_document(
            self.cleaned_data.get("bl_file"),
            "Draft Bill of Lading",
        )