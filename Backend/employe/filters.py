import django_filters
from django import forms
from .models import Employe, PDF_employe

class EmplFilter(django_filters.FilterSet):
    grade = django_filters.ChoiceFilter(
        field_name='grade',
        label='',
        choices=[],
        widget=forms.Select
    )
    class Meta:
        model = Employe
        fields = ['grade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        grade = Employe.objects.values_list('grade', flat=True).distinct()
        grad_choices = [(g, g) for g in grade if g]  # Remove empty/null grade
        self.filters['grade'].extra['choices'] = grad_choices


class EmplPositFilter(django_filters.FilterSet):
    position = django_filters.ChoiceFilter(
        field_name='position',
        label='',
        choices=[],
        widget=forms.Select
    )
    class Meta:
        model = Employe
        fields = ['position']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        position = Employe.objects.values_list('position', flat=True).distinct()
        posit_choices = [(g, g) for g in position if g]  # Remove empty/null position
        self.filters['position'].extra['choices'] = posit_choices



"""
# Filter pdfs 
class PdfsFilter(django_filters.FilterSet):
    grade = django_filters.ChoiceFilter(
        field_name='grade',
        label='',
        choices=[(g, g) for g in Employe.objects.values_list('grade', flat=True).distinct()],
        widget=forms.Select
    )
    class EMeta:
        model = PDF_employe
        fields = ['n_ident__grade']
"""

"""
# -------------------------
class PdFilter(django_filters.FilterSet):
    # First filter: by Catégorie
        division = django_filters.ChoiceFilter(
        field_name='n_ident__division',
        label='الشعبة',
        choices=[(c, c) for c in Employe.objects.values_list('division', flat=True).distinct()],
        widget=forms.Select
    )

    # Second filter: by grade
        grade = django_filters.ChoiceFilter(
        field_name='grade',
        label='الرتبة',
        choices=[(g, g) for g in PDF_employe.objects.values_list('grade', flat=True).distinct()],
        widget=forms.Select
    )

        class Meta:
            model = PDF_employe
            fields = ['n_ident__grade']
"""