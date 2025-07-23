from rest_framework import serializers ; # type: ignore
from .models import Employe , PDF_employe;

class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = '__all__'

class PDFEmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF_employe
        fields = ['id', 'pdf_file', 'uploaded_at', 'grade']