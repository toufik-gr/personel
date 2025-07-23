from django.db import models
from django.contrib.auth.models import User
  



class Enseignant(models.Model):
    
    FAC = (('الرياضة','الرياضة'),('كلية الطب','كلية الطب'),
           ('الطبيعة والحياة','الطبيعة والحياة'),
            ('الرياضيات وعلوم المادة','الرياضيات وعلوم المادة'),
            ('معهد التكنولوجيا','معهد التكنولوجيا'),
            ('الإقتصاد','الإقتصاد'),('اللغات','اللغات'),('العلوم الإنسانية','العلوم الإنسانية'),
            ('الحقوق و العلوم السياسية','الحقوق و العلوم السياسية'),
            ('التكنولوجيات الحديثة','التكنولوجيات الحديثة'),
            ('العلوم التطبيقية','العلوم التطبيقية'),('المحروقات','المحروقات'))
    
    
    POSITION = (('في الخدمة','في الخدمة'),
                ('وضع تحت التصرف جمعوي','وضع تحت التصرف جمعوي'),
                ('وضع تحت التصرف بيداغوجي','وضع تحت التصرف بيداغوجي'),
                ('عطلة مرضية طويلة المدة','عطلة مرضية طويلة المدة'),
                ('إنتداب محدد','إنتداب محدد'),
                ('إنتداب غ محدد','إنتداب غ محدد'),
                ('إستيداع شخصي','إستيداع شخصي'),
                ('إستيداع قانوني','إستيداع قانوني'))
 
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
           
    Nom = models.CharField(max_length=200)
    Prénom = models.CharField(max_length=200)
    Type = models.CharField(max_length=50) 	
    NIN = models.CharField(max_length=20, unique=True)
    matricule = models.CharField(max_length=12, unique=True, null=True)
    dat_naiss = models.DateField()	
    Lieu_naiss = models.CharField(max_length=100)
    date_recrut =	models.DateField()
    grade = models.CharField(max_length=200, choices=GRAD)
    date_grade = models.DateField(null=True , blank=True) 
    Echelon = models.CharField(max_length=20)
    Catégorie =	models.CharField(max_length=15)
    position = 	models.CharField(max_length=30, choices=POSITION, default="في الخدمة")
    faculte = models.CharField(max_length=200, choices=FAC)
    debut_position = models.DateField(null=True, blank=True) 
    fin_position = models.DateField(null=True, blank=True) 
    
    def __str__(self):    
        return f"{self.Nom} {self.Prénom}" 


import os
#----function to generate dynamic path to upload_to
def upload_to(instance, filename):
    # Generate dynamic file upload path based on the grade.
    grad = instance.grade  # Assuming 'grade' is a field in the model
    return os.path.join(f'enseig/{grad}/', filename) 


class PDF_enseign(models.Model):
    
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

    pdf_file = models.FileField(upload_to=upload_to,  verbose_name="الملفات")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='enseign_pdfs', on_delete=models.CASCADE)
    n_ident = models.ForeignKey(Enseignant, related_name='enseign_pdfs', on_delete=models.CASCADE)
    grade = models.CharField(max_length=60, choices=GRAD, default='Grad')
    def __str__(self):
        return f"{self.n_ident.Nom} {self.user}"   

