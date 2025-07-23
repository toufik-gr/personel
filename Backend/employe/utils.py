from .models import Employe
from .filters import EmplFilter, EmplPositFilter
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import timedelta

# --- util function to get filtred employes based on user account
def get_filtered_employe_list(request, user):

    list_rect = 'المديرية'
    list_fac1 = ['الرياضة','كلية الطب','الطبيعة والحياة','الرياضيات وعلوم المادة','معهد التكنولوجيا']
    list_fac2 = ['الإقتصاد','اللغات','العلوم الإنسانية','الحقوق و العلوم السياسية']
    list_fac3 = ['التكنولوجيات الحديثة','العلوم التطبيقية','المحروقات']
    
    if user == "pol1_user":
        employe_list = Employe.objects.filter(faculte__in=list_fac1)
    elif user == 'pol2_user':
        employe_list = Employe.objects.filter(faculte__in=list_fac2)
    elif user == 'pol3_user':
        employe_list = Employe.objects.filter(faculte__in=list_fac3)
    elif user == 'rectorat_user':
        employe_list = Employe.objects.filter(faculte=list_rect)
    
     
    else:
        employe_list = Employe.objects.all()
        # Paginate the queryset, 40 items per page
     # Attach the is_long_leave attribute dynamically


    filter_employe= EmplFilter(request.GET, queryset=employe_list)
    employe_list = filter_employe.qs
    filter_posit= EmplPositFilter(request.GET, queryset=employe_list)
    employe_list = filter_posit.qs 

    query = request.GET.get('query', '')  # Get search input from the user
      
    if query:
        employe_list = employe_list.filter(
            Q(Nom__icontains=query) | 
            Q(Prénom__icontains=query) | 
            Q(faculte__icontains=query)             
            )
    # calculate difference between debutPos and finPosition, to highlight records if is_true
    # Define the conditions in a dictionary
    position_thresholds = {
        "إستيداع قانوني": 5 * 365,
        "إستيداع شخصي": 2 * 365,
        "وضع تحت التصرف": 4 * 365,
        "عطلة مرضية طويلة المدة": 3 * 365,
        "إنتداب محدد": 4 * 365,
        }
   
      
    # Calculate difference and check conditions
    for emp in employe_list:
        # Skip calculation if either date is None
        if emp.fin_position is None or emp.debut_position is None:
            emp.is_long_leave = False
            continue  # Skip to the next employee

        diff = (emp.fin_position - emp.debut_position).days if (emp.fin_position and emp.debut_position) else 0
        emp.is_long_leave = diff > position_thresholds.get(emp.position, float('inf'))  # Default to False if position not in dictionary
        
    
    paginator = Paginator(employe_list, 30)
    page_number = request.GET.get('page')  # Get page number from URL
    page_obj = paginator.get_page(page_number)
      
    count = employe_list.count() 
    
         
    context = {'filter_form': filter_employe, 
                'filter_position':filter_posit,
                'employe_list': employe_list,
                'page_obj':page_obj,'count':count}
    return context