from django.shortcuts import render, redirect, get_object_or_404
from .models import Employe, PDF_employe
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import FileResponse
from django.contrib import messages
#--------------------------------------
from django.db.models import Count
#---------------------------------------------
from .filters import EmplFilter #,PdfsFilter, PdFilter
from django.db.models import Q
#-----------------------------------------------
#from django.views.generic.edit import FormView
from .utils import get_filtered_employe_list
from urllib.parse import unquote
from django.core.paginator import Paginator


# --- Api with filter and search
from rest_framework.decorators import api_view, permission_classes # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Employe
from .serializers import EmployeSerializer



USER_FACULTY_MAP = {
    "rectorat_user" : ["المديرية"],
    "pol1_user": ['الرياضة','كلية الطب','الطبيعة والحياة','الرياضيات وعلوم المادة','معهد التكنولوجيا'],
    "pol2_user": ['الإقتصاد','اللغات','العلوم الإنسانية','الحقوق و العلوم السياسية'],
    "pol3_user" : ['التكنولوجيات الحديثة','العلوم التطبيقية','المحروقات'],
}

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employe_list_api(request):
    username = request.user.username
    allowed_faculties = USER_FACULTY_MAP.get(username, [])
    print(allowed_faculties)
    
    queryset= Employe.objects.filter(faculte__in=allowed_faculties)
    print(queryset)
    # Filtering (exact matches)
    position = request.GET.get('position')
    grade = request.GET.get('grade')
    if position:
        queryset = queryset.filter(position=position)
    if grade:
        queryset = queryset.filter(grade=grade)

    # Searching (partial match)
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(
            Q(Nom__icontains=search_query) | 
            Q(Prénom__icontains=search_query) | 
            Q(faculte__icontains=search_query) 
        )

   # count  = (queryset.count())
  #  print(count)
    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = EmployeSerializer(result_page, many=True)
    count = serializer.data.count(queryset)

    return paginator.get_paginated_response({
        'count': queryset.count(),        # Total enseignants matching filters
        'results': serializer.data        # Current page data
    })
@api_view(['POST'])
def create_employe(request):
    data = request.data
    serializer = EmployeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['GET' , 'PUT', 'DELETE'])
def emp_detail(request, pk):
    try:
        emp = Employe.objects.get(pk=pk)
    except emp.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeSerializer(emp)
        return Response(serializer.data)
        
    if request.method == 'DELETE':
        emp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        data = request.data
        serializer = EmployeSerializer(emp, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def grades_by_division(request, employe_id):
    try:
        employe = Employe.objects.get(id=employe_id)
    except Employe.DoesNotExist:
        return Response({'error': 'Employe not found'}, status=404)

    grades = Employe.objects \
        .filter(division=employe.division) \
        .values_list('grade', flat=True) \
        .distinct()

    return Response({'grades': list(grades)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_pdf_folder(request):
    files = request.FILES.getlist('pdfs')
    grade = request.POST.get('grade')
    employe_id = request.POST.get('n_ident')
     
    if not files or not grade or not employe_id:
        return Response({'error': 'Missing files or metadata'}, status=400)
    try:
        employe = Employe.objects.get(id=employe_id)
    except Employe.DoesNotExist:
        return Response({'error': 'Invalid Employe ID'}, status=404)
    # Get grades based on employee's division
    """ 
    grades = [(g, g) for g in Employe.objects
                                .filter(division=employe.division)
                                .values_list('grade', flat=True)
                                .distinct()]
     """
    for file in files:
        if file.name.endswith('.pdf'):
            PDF_employe.objects.create(
                pdf_file=file,
                grade=grade,
                user=request.user,
                n_ident=employe
            )

    return Response({'message': 'PDFs uploaded successfully!'})


# --- PDF list api
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pdfs_for_employe(request, employe_id):
    try:
        employe = Employe.objects.get(id=employe_id)
    except Employe.DoesNotExist:
        return Response({'error': 'Employe not found'}, status=404)
    
    grade = request.GET.get("grade")
    pdfs = PDF_employe.objects.filter(n_ident=employe).order_by('-uploaded_at')
    if grade:
        pdfs = pdfs.filter(grade=grade)

    data = [
        {
            "id": pdf.id,
            "file": request.build_absolute_uri(pdf.pdf_file.url),
            "uploaded_at": pdf.uploaded_at,
            "user": pdf.user.username,
            "n_ident" : employe.id,
            "grade": pdf.grade,
        }
        for pdf in pdfs
    ]
    return Response(data)


















#----------END API ---------------------------#
# --- show emp_list  to update  
@login_required(login_url="/users/login/")
def employe_list_global(request,action): 
    user = request.user.username
    context= get_filtered_employe_list(request, user)
     
    if action == 'update':
        context['action'] = {'action_name': 'تحديث', 'action_title': 'قائمة الموظفين والتحديث'}
    
    elif action == 'add_file':
        context ['action']= {'action_name' :'إضافة_ملفات', 'action_title': 'إضافة ملفات الموظفين'}
    
    elif action == 'view':     # for view emp : pdfs using AJAX   
         context ['action'] = {'action_name': 'معاينة', 'action_title': 'عرض ملفات الموظفين'}
    
    elif action == 'preview':  # for preview emp : pdfs using django
        context['action'] = {'action_name': 'معاينة_ملف', 'action_title': 'معاينة ملفات الموظفين'}
     
    return render(request,'emp_list_global.html',context )    


# ------------ GET PDfs of Employee to preview
from django.http import JsonResponse

# View before Update Employe  
@login_required(login_url="/users/login/")
def view_employe(request,id):
     
    empl = Employe.objects.get(pk=id)
    form = UpdateFormf(instance=empl)  # Create  form TO GET request
    if request.method == "POST":
        form = UpdateFormf(request.POST, instance=empl)
        if form.is_valid():
            form.save()         
           
        return redirect("employe:update_empl", empl.id)
    else:
        form = UpdateFormf(instance=empl)
         
    return render(request, 'employe/viewEmpl.html', {'form': form})

# Update Employe  
@login_required(login_url="/users/login/")
def update_employe(request,id):
     
    empl = Employe.objects.get(pk=id)
     
    if request.method == "POST":
        form = UpdateFormf(request.POST, instance=empl)
        if form.is_valid():
            form = form.save()
          
        messages.success(request,"!تم التحديث بنجاح")
        return redirect('employeList', 'update')  # Redirect after success
         
    else:
        form = UpdateFormf(instance=empl)  # Create an empty form for GET request
         
    return render(request, 'employe/updateEmpl.html', {'form': form})



# Upload PDF View  
@login_required(login_url="/users/login/")
def upload_empl_pdf(request,id):
    empl = Employe.objects.get(pk=id)     

    # Get grades based on employee's division
    grades = [(g, g) for g in Employe.objects
                                .filter(division=empl.division)
                                .values_list('grade', flat=True)
                                .distinct()]
     
    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES, grade_choices=grades)
        if form.is_valid():
            selected_grade = form.cleaned_data["grade"]
            files = form.cleaned_data["file_field"]  # Extract list of files
            
            for file in files:
                PDF_employe.objects.create(pdf_file=file, 
                user = request.user,
                n_ident = empl,
                grade=selected_grade,  # Save grade if your model includes it
                 ) # Save each file separately
            messages.success(request,"!تم إضافة الملف بنجاح")
            return redirect("employe:pdf_list", empl.id)  # Redirect after success
    else:
        form = FileFieldForm(grade_choices=grades)  # Create an empty form for GET request

    return render(request, 'upload_pdf.html', {'form': form})

   
# List PDFs uploaded
@login_required(login_url="/users/login/")
def pdf_list(request,id):
    empl = Employe.objects.get(pk=id)       
   
    # Get grades based on employee's division
    grades = [(g, g) for g in Employe.objects
                                .filter(division=empl.division)
                                .values_list('grade', flat=True)
                                .distinct()]
    
    pdfs = empl.employe_pdfs.all().order_by('-uploaded_at')
   
    #apply filter form
    form = GradeFilterForm(request.GET, grade_choices=grades)
    if form.is_valid():
        selected_grade = form.cleaned_data.get('grade')
        if selected_grade:
            pdfs = pdfs.filter(grade=selected_grade)

    count = pdfs.count()

    return render(request, 'employe/pdf_list.html', {
        'empl': empl,
        'pdfs': pdfs,
        'count': count,
        'form': form,
    })



# ------------ GET PDfs of Employee to preview using  AJAX

def get_pdfs(request):
    emp_id = request.GET.get('emp_id')

    if not emp_id:
        return JsonResponse({"error": "Missing emp_id"}, status=400)

    try:
        pdfs = PDF_employe.objects.filter(n_ident_id=emp_id)

        if not pdfs.exists():
            return JsonResponse([], safe=False)  # Return empty list if no PDFs found

        pdf_list = [
            {
                'id': pdf.id,
                'pdf_url': pdf.pdf_file.url,
                'uploaded_at': pdf.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format date
                'user': pdf.user.username  # Get username
            }
            for pdf in pdfs
        ]

        return JsonResponse(pdf_list, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Download PDF
def download_pdf(request, pdf_id):
    pdf = PDF_employe.objects.get(id=pdf_id)
    return FileResponse(pdf.pdf_file, as_attachment=True)



 