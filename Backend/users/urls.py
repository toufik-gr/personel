from django.urls import path
from . import views
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name="logout"),
 #### api
    #path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('me/', views.get_user, name='get_user'),
    #path('api/logout/', views.logout_view, name ='logout'),
   
    path('profile/', views.user_profile, name="profile"),
]