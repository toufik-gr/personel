import django_filters
from django import forms
from .models import Emp_contrat, PDFFile

class EmplContFilter(django_filters.FilterSet):
    grade = django_filters.ChoiceFilter(
        field_name='grade',
        label='',
        choices=[],
        widget=forms.Select
    )
    class Meta:
        model = Emp_contrat
        fields = ['grade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        grade = Emp_contrat.objects.values_list('grade', flat=True).distinct()
        grad_choices = [(g, g) for g in grade if g]  # Remove empty/null grade
        self.filters['grade'].extra['choices'] = grad_choices
 

class EmpPositFilter(django_filters.FilterSet):
    position = django_filters.ChoiceFilter(
        field_name='position',
        label='',
        choices=[],
        widget=forms.Select
    )
    class Meta:
        model = Emp_contrat
        fields = ['position']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        position = Emp_contrat.objects.values_list('position', flat=True).distinct()
        posit_choices = [(g, g) for g in position if g]  # Remove empty/null position
        self.filters['position'].extra['choices'] = posit_choices
    


# Filter pdfs 
class PdfsFilter(django_filters.FilterSet):
    grade = django_filters.ChoiceFilter(
        field_name='grade',
        label='',
        choices=[(g, g) for g in Emp_contrat.objects.values_list('grade', flat=True).distinct()],
        widget=forms.Select
    )
    class Meta:
        model = PDFFile
        fields = ['n_ident__grade']
