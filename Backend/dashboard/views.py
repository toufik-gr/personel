from django.shortcuts import render
from django.contrib.auth.models import User
from posts.models import Emp_contrat
from enseignants.models import Enseignant
from employe.models import Employe
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required(login_url="/users/login/")
def dashboard(request):
    faculties = {
        "rectorat": ['المديرية'],
        "pol1": ['الرياضة', 'كلية الطب', 'الطبيعة والحياة', 'الرياضيات وعلوم المادة', 'معهد التكنولوجيا'],
        "pol2": ['الإقتصاد', 'اللغات', 'العلوم الإنسانية', 'الحقوق و العلوم السياسية'],
        "pol3": ['التكنولوجيات الحديثة', 'العلوم التطبيقية', 'المحروقات']
    }

    data_emp = {}
    count_emp = 0
    for key, faculty_list in faculties.items():
        emps = Emp_contrat.objects.filter(faculte__in=faculty_list)
        total_emps = emps.count()
        existing = emps.filter(contrat_pdfs__isnull=False).distinct().count()
        rest_count = total_emps - existing
        percentage = round((existing * 100) / total_emps, 2) if total_emps > 0 else 0
        
        data_emp[key] = {
            "emps": total_emps,
            "existing": existing,
            "rest": rest_count,
            "percentage": percentage
        }

        count_emp +=total_emps
 
    #--------------data employe 
    data_employe = {}
    count_employe = 0
    for key, faculty_list in faculties.items():
        emps = Employe.objects.filter(faculte__in=faculty_list)
        total_empls = emps.count()
        existing = emps.filter(employe_pdfs__isnull=False).distinct().count()
        rest_count = total_empls - existing
        percentage = round((existing * 100) / total_empls, 2) if total_empls > 0 else 0
        
        data_employe[key] = {
            "emps": total_empls,
            "existing": existing,
            "rest": rest_count,
            "percentage": percentage
        }
 
        count_employe +=total_empls
 
 
    # Removes 'rectorat' if it exists
    rectorat = faculties.pop("rectorat")
    data_ens = {}
    count_ens = 0
    for key, faculty_list in faculties.items():
        ens = Enseignant.objects.filter(faculte__in=faculty_list)
       
        total_ens = ens.count()
        existing = ens.filter(enseign_pdfs__isnull=False).distinct().count()
        rest_count = total_ens - existing
        percentage = round((existing * 100) / total_ens, 2) if total_ens > 0 else 0

        data_ens[key] = {
            "ens": total_ens,
            "existing": existing,
            "rest": rest_count,
            "percentage": percentage
        }
        count_ens += total_ens
    context = {"data_emp": data_emp , "data_ens" : data_ens, "data_employe":data_employe,
               "count_emp":count_emp , "count_ens":count_ens , "count_employe":count_employe}
    return render(request, "dashboard/dashboard.html", context )

