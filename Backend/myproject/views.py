from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="/users/login/")
def homepage(request):
#    context = {'أساتذة':'أساتذة','متعاقدين':'متعاقدين'}
    
    return render(request, 'home.html')


def about(request):
     
    return render(request, 'about.html')


from django.shortcuts import redirect

def set_selected_category(request):
    category = request.GET.get('category', 'متعاقدين')  # Default is 'employees'
    request.session['selected_category'] = category
    print(request.session)
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the same page
    