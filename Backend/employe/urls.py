from django.urls import path
from . import views

app_name = 'employe'

urlpatterns = [
     
     
    # -- View and Update employe
    path('view/<int:id>/', views.view_employe, name='view_empl'),
    path('update/<int:id>/', views.update_employe, name='update_empl'),
    
    #--- PDFs Preview
    path('pdfs/<int:id>/', views.pdf_list, name='pdf_list'),
    path('download/<int:pdf_id>/', views.download_pdf, name='download_pdf'), 
    path('get-pdfs/', views.get_pdfs, name='get_pdfs'),#--from AJAX


    #--- from Api
  
    path('create/', views.create_employe, name='create_employe'),
    path('emp/<int:pk>/', views.emp_detail, name='emp_detail'),
    path('empList/' ,views.employe_list_api , name = 'empList'),
    path('emp/<int:employe_id>/grades/', views.grades_by_division,name="emp_grades"),
    path('upload-folder/', views.upload_pdf_folder, name='upload-folder'),
    path("pdfsList/<int:employe_id>/", views.list_pdfs_for_employe, name="pdfsListEmp"),
]

 