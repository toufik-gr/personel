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
    GRAD = (
            ('أستاذ محاضر قسم أ','أستاذ محاضر قسم أ'),
            ('أستاذ محاضر قسم ب','أستاذ محاضر قسم ب'),
            ('أستاذ مساعد قسم أ','أستاذ مساعد قسم أ'),
            ('أستاذ مساعد قسم ب','أستاذ مساعد قسم ب'),
            ('أستاذ مساعد','أستاذ مساعد') ,
            ('أستاذ مساعد إستشفائي جامعي','أستاذ مساعد إستشفائي جامعي'),
            ('أستاذ إستشفائي جامعي','أستاذ إستشفائي جامعي'),
            ('أستاذ محاضر إستشفائي جامعي أ','أستاذ محاضر إستشفائي جامعي أ'),
            ('أستاذ محاضر إستشفائي جامعي ب','أستاذ محاضر إستشفائي جامعي ب'),
            ('أستاذ','أستاذ'),
            ('أستاذ متميز','أستاذ متميز') ,
            ('معيد','معيد') ,
    )

    grade = forms.ChoiceField(label='الرتبة', choices=GRAD) 
    file_field = MultipleFileField()

class UpdateFormf(forms.ModelForm):
    
    class Meta :
        model = Enseignant
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
            'date_grade': 'تاريخ الرتبة',
            'Echelon': 'الدرجة', 
            'Catégorie':'الصنف',
            'position':'الوضعية',      
            'debut_position': 'بداية الوضعية',
            'fin_position': 'نهاية الوضعية',      
            'faculte':'الكلية',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Type'].widget.attrs['readonly'] = True
        