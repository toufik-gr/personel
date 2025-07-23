from django import forms 
from .models import *


# --- to upload multi pdf file
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class FileFieldForm(forms.Form):

    grade = forms.ChoiceField(choices=[], label='الرتبة')  # We'll set choices dynamically 
    file_field = MultipleFileField(label="الملفات")
        

    def __init__(self, *args, **kwargs):
        grade_choices = kwargs.pop('grade_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['grade'].choices = grade_choices

class UpdateFormf(forms.ModelForm):
    
    class Meta :
        model = Employe
        fields = "__all__" 
        widgets = {
                'debut_position': forms.DateInput(attrs={
                'placeholder': 'YYYY-MM-DD'},
                
                ),
                 'fin_position': forms.DateInput(attrs={
                'placeholder': 'YYYY-MM-DD'},
               
                ), 

        }
        labels = {
            'Nom':'الإسم',
            'Prénom': 'اللقب',
            'Type': 'النوع',
            'NIN' :'الرقم الوطني',
            'matricule': 'رقم ض أ',
            'dat_naiss':'تاريخ الميلاد',
            'Lieu_naiss':'مكان الميلاد',
            'date_recrut':'تاريخ التوظيف',
            'grade':'الرتبة',
            'Echelon': 'الدرجة',
            'date_grade' : 'تاريخ الرتبة', 
            'Catégorie':'الفئة',
            'division' : 'الشعبة',
            'position':'الوضعية',      
            'debut_position': 'بداية الوضعية',
            'fin_position': 'نهاية الوضعية',      
            'faculte':'الكلية',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make multiple fields readonly
        readonly_fields = ['Type', 'division', 'Catégorie']

        for field_name in readonly_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['readonly'] = True
        
#form to filter employe pdf based on grades of employe division
class GradeFilterForm(forms.Form):
    grade = forms.ChoiceField(
        choices=[],
        required=False,
        label=""
    )
    def __init__(self, *args, **kwargs):
        grade_choices = kwargs.pop('grade_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['grade'].choices = [('', '--- الكل ---')] + grade_choices