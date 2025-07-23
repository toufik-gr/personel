from rest_framework import serializers
from .models import Enseignant, PDF_enseign

class EnseigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = '__all__'

class PDFEnseignSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF_enseign
        fields = ['id', 'pdf_file', 'uploaded_at', 'grade']