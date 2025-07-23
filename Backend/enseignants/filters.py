import django_filters
from django import forms
from .models import Enseignant, PDF_enseign

class EnseignFilter(django_filters.FilterSet):
    grade = django_filters.ChoiceFilter(
        field_name='grade',
        label='',
        choices=[],
        widget=forms.Select
    )
    class Meta:
        model = Enseignant
        fields = ['grade']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        grade = Enseignant.objects.values_list('grade', flat=True).distinct()
        grad_choices = [(g, g) for g in grade if g]  # Remove empty/null position
        self.filters['grade'].extra['choices'] = grad_choices


class EnsPositFilter(django_filters.FilterSet):
    position = django_filters.ChoiceFilter(
        field_name='position',
        label='',
        choices=[],  # Will be set dynamically in __init__
        widget=forms.Select
    )

    class Meta:
        model = Enseignant
        fields = ['position']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        positions = Enseignant.objects.values_list('position', flat=True).distinct()
        posi_choices = [(g, g) for g in positions if g]  # Remove empty/null position
        self.filters['position'].extra['choices'] = posi_choices

#Filter grade in pdf_ens model
""" 
class PdfsEnsFilter(django_filters.FilterSet):
    grade = django_filters.ChoiceFilter(
        field_name='grade',
        label='',
        choices=[(g, g) for g in PDF_enseign.objects.values_list('grade', flat=True).distinct()],
        widget=forms.Select
    )
    
    class Meta:
        model = PDF_enseign
        fields = ['grade']
 """
class PdfsEnsFilter(django_filters.FilterSet):
    grade = django_filters.ChoiceFilter(
        field_name='grade',
        label='',
        # Will be set dynamically in __init__
        choices=[(g, g) for g in PDF_enseign.objects.values_list('grade', flat=True).distinct()],
        widget=forms.Select
    )

    class Meta:
        model = PDF_enseign
        fields = ['grade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        grades = PDF_enseign.objects.values_list('grade', flat=True).distinct()
        grade_choices = [(g, g) for g in grades if g]  # Remove empty/null grades
        self.filters['grade'].extra['choices'] = grade_choices
       
# Filter pdfs 
class PdfsFilter(django_filters.FilterSet):
    grade = django_filters.ChoiceFilter(
        field_name='grade',
        label='',
        choices=[(g, g) for g in Enseignant.objects.values_list('grade', flat=True).distinct()],
        widget=forms.Select
    )
    class Meta:
        model = PDF_enseign
        fields = ['n_ident__grade']
