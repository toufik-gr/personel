from .models import Emp_contrat
from .filters import EmplContFilter, EmpPositFilter
from django.db.models import Q
from django.core.paginator import Paginator


# --- util function to get filtred employes based on user account
def get_filtered_emp_list(request, user):

    list_rect = 'المديرية'
    list_fac1 = ['الرياضة','كلية الطب','الطبيعة والحياة','الرياضيات وعلوم المادة','معهد التكنولوجيا']
    list_fac2 = ['الإقتصاد','اللغات','العلوم الإنسانية','الحقوق و العلوم السياسية']
    list_fac3 = ['التكنولوجيات الحديثة','العلوم التطبيقية','المحروقات']

    if user == "pol1_user":
        emp_list = Emp_contrat.objects.filter(faculte__in=list_fac1)
    elif user == 'pol2_user':
        emp_list = Emp_contrat.objects.filter(faculte__in=list_fac2)
    elif user == 'pol3_user':
        emp_list = Emp_contrat.objects.filter(faculte__in=list_fac3)
    elif user == 'rectorat_user':
        emp_list = Emp_contrat.objects.filter(faculte=list_rect)
    
    else:
        emp_list = Emp_contrat.objects.all()
         # Paginate the queryset, 40 items per page
    
    
    filter_cont= EmplContFilter(request.GET, queryset=emp_list)
    emp_list = filter_cont.qs
    filter_posit= EmpPositFilter(request.GET, queryset=emp_list)
    emp_list = filter_posit.qs
    
    query = request.GET.get('query', '')  # Get search input from the user
      
    if query:
        emp_list = emp_list.filter(
            Q(Nom__icontains=query) | 
            Q(Prénom__icontains=query) | 
            Q(faculte__icontains=query)
           # Q(position__icontains=query)
            )
    
    # Define the conditions in a dictionary
    position_thresholds = {
        "إستيداع": 5 * 365,
        "عطلة مرضية طويلة المدة": 3 * 365,
        "إنتداب": 4 * 365,
        }

    # Calculate difference and check conditions
    for emp in emp_list:
        # Skip calculation if either date is None
        if emp.fin_position is None or emp.debut_position is None:
            emp.is_long_leave = False
            continue  # Skip to the next employee

    # Calculate the difference
        diff = (emp.fin_position - emp.debut_position).days if (emp.fin_position and emp.debut_position) else 0
        emp.is_long_leave = diff > position_thresholds.get(emp.position, float('inf'))  # Default to False if position not in dictionary
         
    
    paginator = Paginator(emp_list, 30)
    page_number = request.GET.get('page')  # Get page number from URL
    page_obj = paginator.get_page(page_number)


    count = emp_list.count()        
    context = {'filter_form': filter_cont, 'filter_position':filter_posit,
             'emp_list': emp_list,'page_obj':page_obj,'count':count}     
    return context
