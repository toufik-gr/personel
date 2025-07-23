##### serializer #####
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


####### API ##########


#---- django ------------------------
from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout
from django.contrib import messages
 
# Create your views here.
def register_view(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            login(request, form.save())
            return redirect("posts:list")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", { "form": form })

 
from django.contrib.auth.views import LoginView
from .forms import ArabicAuthentForm

class CustomLoginView(LoginView):
    form_class = ArabicAuthentForm
    template_name = 'users/login.html'  # Ensure this template exists


def logout_view(request):
     
        logout(request) 
        return redirect('/')

"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
    })
"""