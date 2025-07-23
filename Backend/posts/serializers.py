from rest_framework import serializers ; # type: ignore
from .models import Emp_contrat , PDFFile;

class EmpContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emp_contrat
        fields = '__all__'

class PDFEmpContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFFile
        fields = ['id', 'pdf_file', 'uploaded_at', 'grade']