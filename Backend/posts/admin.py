from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export.formats.base_formats import XLSX
from import_export import resources, fields
from .models import  Emp_contrat, PDFFile # Replace with your actual model

from datetime import datetime
from openpyxl.styles import numbers  # Import Excel formatting
 

class EmpContratResource(resources.ModelResource):
    class Meta:
        model = Emp_contrat
 
# Register Model with Import/Export Support
@admin.register(Emp_contrat)
class Emp_contratAdmin(ImportExportModelAdmin):
    resource_class = EmpContratResource  # Link resource class (optional)
    #list_display = _all_  # Customize list view
    def get_import_formats(self):
        formats = super().get_import_formats()
        if XLSX not in formats:  # Avoid duplicates
            formats.append(XLSX)
        return formats


# Register your models here.
 
admin.site.register(PDFFile)
