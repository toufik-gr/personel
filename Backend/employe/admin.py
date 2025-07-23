from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export.formats.base_formats import XLSX
from import_export import resources, fields
from .models import  Employe, PDF_employe # Replace with your actual model

from datetime import datetime
from openpyxl.styles import numbers  # Import Excel formatting
 

class EmployeResource(resources.ModelResource):
    class Meta:
        model = Employe
 
# Register Model with Import/Export Support
@admin.register(Employe)
class Emp_contratAdmin(ImportExportModelAdmin):
    resource_class = EmployeResource  # Link resource class (optional)
    #list_display = _all_  # Customize list view
    def get_import_formats(self):
        formats = super().get_import_formats()
        if XLSX not in formats:  # Avoid duplicates
            formats.append(XLSX)
        return formats


# Register your models here.
 
admin.site.register(PDF_employe)
