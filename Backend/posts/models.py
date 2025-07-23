from django.db import models
from django.contrib.auth.models import User
# Create your models here.
 



class Emp_contrat(models.Model):
    
    FAC = ( ('المديرية','المديرية'),('الرياضة','الرياضة'), 
           ('كلية الطب','كلية الطب'),('الطبيعة والحياة','الطبيعة والحياة'),
            ('الرياضيات وعلوم المادة','الرياضيات وعلوم المادة'),
            ('معهد التكنولوجيا','معهد التكنولوجيا'),
            ('الإقتصاد','الإقتصاد'),('اللغات','اللغات'),('العلوم الإنسانية','العلوم الإنسانية'),
            ('الحقوق و العلوم السياسية','الحقوق و العلوم السياسية'),
            ('التكنولوجيات الحديثة','التكنولوجيات الحديثة'),
            ('العلوم التطبيقية','العلوم التطبيقية'),('المحروقات','المحروقات'))
    
    GRAD = (
            ('عامل مهني من المستوى الأول','عامل مهني من المستوى الأول'),
            ('عامل مهني من المستوى الأول ت ج','عامل مهني من المستوى الأول ت ج' ),
            ('حارس','حارس'),
            ('عامل مهني من المستوى الثاني','عامل مهني من المستوى الثاني'),
            ('عون وقاية من المستوى الأول','عون وقاية من المستوى الأول'),
            ('سائق سيارة من المستوى الأول','سائق سيارة من المستوى الأول'),
            ('عامل مهني من المستوى الثالث','عامل مهني من المستوى الثالث'),
            ('عون خدمات من المستوى الثالث','عون خدمات من المستوى الثالث')

    )       
    
    POSITION = (
                ('في الخدمة','في الخدمة'),
                ('عطلة مرضية طويلة المدة','عطلة مرضية طويلة المدة'),
                ('عطلة غ مدفوعة الأجر','عطلة غ مدفوعة الأجر'),
                ('إنتداب','إنتداب'))
         
    
    Nom = models.CharField(max_length=200)
    Prénom = models.CharField(max_length=200)
    Type = models.CharField(max_length=50) 	
    NIN = models.CharField(max_length=20, unique=True)
    dat_naiss = models.DateField()	
    Lieu_naiss = models.CharField(max_length=200)
    date_recrut =	models.DateField()
    grade = models.CharField(max_length=200, choices=GRAD)
    Catégorie =	models.CharField(max_length=5)
    position = 	models.CharField(max_length=30, choices=POSITION, default="في الخدمة")
    faculte = models.CharField(max_length=200, choices=FAC)
    matricule = models.CharField(max_length=12, unique=True, null=True)
    debut_position = models.DateField(null=True, blank=True) 
    fin_position = models.DateField(null=True, blank=True) 
     
    def __str__(self):    
        return f"{self.Nom} {self.Prénom}" 


import os
#----function to generate dynamic path to upload_to
def upload_to(instance, filename):
    # Generate dynamic file upload path based on the grade.
    grad = instance.grad  # Assuming 'grade' is a field in the model
    return os.path.join(f'{grad}/', filename) 


class PDFFile(models.Model):
    
    pdf_file = models.FileField(upload_to='contrat/',  verbose_name="الملفات")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='user_pdfs', on_delete=models.CASCADE)
    n_ident = models.ForeignKey(Emp_contrat, related_name='contrat_pdfs', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.n_ident.Nom} {self.user}"  