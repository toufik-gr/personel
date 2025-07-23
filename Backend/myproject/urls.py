from django.contrib import admin
from django.urls import path, include, re_path
from . import views 
from posts.views import emp_cont_list_global, upload_pdf
from enseignants.views import enseign_list_global, upload_ens_pdf
from employe.views import employe_list_global , upload_empl_pdf
from users.views import CustomLoginView
from django.conf.urls.static import static 
from django.conf import settings    
from django.views.static import serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns =[
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    # path('', CustomLoginView.as_view(), name='login'),
     
    path('', views.homepage, name="home"),
     

    # contractuel list for all operations in all apps
    path('empList/<action>/', emp_cont_list_global, name='empList'), 
    # upload pdfs for all apps
    path('upload/<int:id>/', upload_pdf, name='upload_pdf'),     
  

    # enseignant list for all operations
    path('enseignList/<action>/', enseign_list_global, name='enseignList'), 
    path('upload_ens/<int:id>/', upload_ens_pdf, name='upload_ens_pdf'),     

    # employe list for all operations
    path('employeList/<action>/', employe_list_global, name='employeList'), 
    path('upload_empl/<int:id>/', upload_empl_pdf, name='upload_empl_pdf'),     


    path('posts/', include('posts.urls')),# url of emp_contrat app 
    path('users/', include('users.urls')),
    path('enseign/', include('enseignants.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('employe/', include('employe.urls')),
    
    # --- session
    path('set-category/', views.set_selected_category, name='set_selected_category'), 
    
    #api 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
