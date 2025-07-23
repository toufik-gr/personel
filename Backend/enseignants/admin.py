from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export.formats.base_formats import XLSX
from import_export import resources, fields
from .models import  Enseignant, PDF_enseign # Replace with your actual model

from datetime import datetime
from openpyxl.styles import numbers  # Import Excel formatting
 

class EnseignResource(resources.ModelResource):
    class Meta:
        model = Enseignant
 
# Register Model with Import/Export Support
@admin.register(Enseignant)
class EnseingAdmin(ImportExportModelAdmin):
    resource_class = EnseignResource  # Link resource class (optional)
    #list_display = _all_  # Customize list view
    def get_import_formats(self):
        formats = super().get_import_formats()
        if XLSX not in formats:  # Avoid duplicates
            formats.append(XLSX)
        return formats


# Register your models here.
 
admin.site.register(PDF_enseign) 