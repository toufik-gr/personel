from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [ 
    # -- View and Update emp
    path('view/<int:id>/', views.view_emp, name='view_emp'),
    path('update/<int:id>/', views.update_emp, name='update_emp'),
    
    #--- PDFs Preview
    path('pdfs/<int:id>/', views.pdf_list, name='pdf_list'),
    path('download/<int:pdf_id>/', views.download_pdf, name='download_pdf'),    
    # path('pdfs-preview/', views.pdfs_preview, name="pdfs_preview"),#BUT Not used in app
    path('get-pdfs/', views.get_pdfs, name='get_pdfs'),#--from AJAX



    #--- from Api
  
    path('create/', views.create_empContrat, name='create_employe'),
    path('emp/<int:pk>/', views.empContrat_detail, name='emp_detail'),
    path('empContList/' ,views.empContrat_list_api , name = 'empCList'),   
    path('upload-folder/', views.upload_pdf_folder, name='upload-folder'),
    path('pdfsList/<int:employe_id>/', views.list_pdfs_for_employe, name="pdfsListEmp"),

]
