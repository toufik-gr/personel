from django.urls import path
from . import views

app_name = 'enseignants'
urlpatterns = [     
     
    # -- View and Update ens
    path('view/<int:id>/', views.view_enseign, name='view_ens'),
    path('update/<int:id>/', views.update_enseign, name='update_ens'),
    
    #--- PDFs Preview
    path('pdfs/<int:id>/', views.pdf_list, name='pdf_list'),
    path('download/<int:pdf_id>/', views.download_pdf, name='download_pdf'), 
    path('get-pdfs/', views.get_pdfs, name='get_pdfs'),#--from AJAX
    
    #--- from Api
    #path('ens/', views.get_ensigns, name='get_ensigns'),
    path('create/', views.create_enseign, name='create_enseign'),
    path('ens/<int:pk>/', views.enseign_detail, name='enseign_detail'),
    path('ensList/' ,views.enseignant_list_api , name = 'ensList'),
   # path('api/<int:id>/pdfs/', views.pdf_list_api, name='pdf_list_api'),
    path('upload-folder/', views.upload_pdf_folder, name='upload-folder'),
    path("pdfsList/<int:enseignant_id>/", views.list_pdfs_for_enseignant, name="pdfsList"),
]
