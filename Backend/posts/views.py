from django.shortcuts import render, redirect, get_object_or_404
from .models import PDFFile, Emp_contrat
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import FileResponse
from django.contrib import messages
#--------------------------------------
from django.db.models import Count
#---------------------------------------------
from .filters import EmplContFilter
from django.db.models import Q
#-----------------------------------------------
#from django.views.generic.edit import FormView
from .utils import get_filtered_emp_list
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
from .models import Emp_contrat
from .serializers import EmpContratSerializer



USER_FACULTY_MAP = {
    "rectorat_user" : ["المديرية"],
    "pol1_user": ['الرياضة','كلية الطب','الطبيعة والحياة','الرياضيات وعلوم المادة','معهد التكنولوجيا'],
    "pol2_user": ['الإقتصاد','اللغات','العلوم الإنسانية','الحقوق و العلوم السياسية'],
    "pol3_user" : ['التكنولوجيات الحديثة','العلوم التطبيقية','المحروقات'],
}

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def empContrat_list_api(request):
    username = request.user.username
    allowed_faculties = USER_FACULTY_MAP.get(username, [])
    print(allowed_faculties)
    
    queryset= Emp_contrat.objects.filter(faculte__in=allowed_faculties)
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
    serializer = EmpContratSerializer(result_page, many=True)
    count = serializer.data.count(queryset)

    return paginator.get_paginated_response({
        'count': queryset.count(),        # Total enseignants matching filters
        'results': serializer.data        # Current page data
    })
@api_view(['POST'])
def create_empContrat(request):
    data = request.data
    serializer = EmpContratSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['GET' , 'PUT', 'DELETE'])
def empContrat_detail(request, pk):
    try:
        emp = Emp_contrat.objects.get(pk=pk)
    except emp.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmpContratSerializer(emp)
        return Response(serializer.data)
        
    if request.method == 'DELETE':
        emp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        data = request.data
        serializer = EmpContratSerializer(emp, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_pdf_folder(request):
    files = request.FILES.getlist('pdfs')
    #grade = request.POST.get('grade')
    employe_id = request.POST.get('n_ident')
     
    if not files or not employe_id:
        return Response({'error': 'Missing files or metadata'}, status=400)
    try:
        employe = Emp_contrat.objects.get(id=employe_id)
    except Emp_contrat.DoesNotExist:
        return Response({'error': 'Invalid Employe ID'}, status=404)
    # Get grades based on employee's division
    for file in files:
        if file.name.endswith('.pdf'):
            PDFFile.objects.create(
                pdf_file=file,
                #grade=grade,
                user=request.user,
                n_ident=employe
            )

    return Response({'message': 'PDFs uploaded successfully!'})


# --- PDF list api
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pdfs_for_employe(request, employe_id):
    try:
        employe = Emp_contrat.objects.get(id=employe_id)
    except Emp_contrat.DoesNotExist:
        return Response({'error': 'Contrqtcuel not found'}, status=404)
    
    #grade = request.GET.get("grade")
    pdfs = PDFFile.objects.filter(n_ident=employe).order_by('-uploaded_at')
    """if grade:
        pdfs = pdfs.filter(grade=grade)
    """
    data = [
        {
            "id": pdf.id,
            "file": request.build_absolute_uri(pdf.pdf_file.url),
            "uploaded_at": pdf.uploaded_at,
            "user": pdf.user.username,
            "n_ident" : employe.id,
            #"grade": pdf.grade,
        }
        for pdf in pdfs
    ]
    return Response(data)


























# --- show emp_list  to update  
@login_required(login_url="/users/login/")
def emp_cont_list_global(request,action): 
    user = request.user.username
 
    context= get_filtered_emp_list(request, user)
     
    if action == 'update':
        context['action'] = {'action_name': 'تحديث', 'action_title': 'قائمة المتعاقدين والتحديث'}
    
    elif action == 'add_file':
        context ['action']= {'action_name' :'إضافة_ملفات', 'action_title': 'إضافة ملفات المتعاقدين'}
    
    elif action == 'view':     # for view emp : pdfs using AJAX   
         context ['action'] = {'action_name': 'معاينة', 'action_title': 'عرض ملفات المتعاقدين'}
    
    elif action == 'preview':  # for preview emp : pdfs using django
        context['action'] = {'action_name': 'معاينة_ملف', 'action_title': 'معاينة ملفات المتعاقدين'}
    
    return render(request,'emp_list_global.html',context )    


# ------------ GET PDfs of Employee to preview
from django.http import JsonResponse

# View before Update Employe  
@login_required(login_url="/users/login/")
def view_emp(request,id):
    emp = Emp_contrat.objects.get(pk=id)
    form = UpdateFormf(instance=emp)  # Create  form TO GET request
    if request.method == "POST":
        form = UpdateFormf(request.POST, instance=emp)
        if form.is_valid():
             form.save()         
        return redirect("posts:update_emp", emp.id)
    else:
        form = UpdateFormf(instance=emp)
         
    return render(request, 'posts/viewEmp.html', {'form': form})

# Update Employe  
@login_required(login_url="/users/login/")
def update_emp(request,id):
    emp = Emp_contrat.objects.get(pk=id)
     
    if request.method == "POST":
        form = UpdateFormf(request.POST, instance=emp)
        if form.is_valid():
            form = form.save()
            
        messages.success(request,"!تم التحديث بنجاح")
        return redirect("empList" , 'update')  # Redirect after success
         
    else:
        form = UpdateFormf(instance=emp)  # Create an empty form for GET request
         
    return render(request, 'posts/updateEmp.html', {'form': form})



# Upload PDF View  
@login_required(login_url="/users/login/")
def upload_pdf(request,id):
    emp = Emp_contrat.objects.get(pk=id)
    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data["file_field"]  # Extract list of files
          
            for file in files:
                PDFFile.objects.create(pdf_file=file, 
                user = request.user,
           
                n_ident = emp) # Save each file separately
            messages.success(request,"!تم إضافة الملف بنجاح")
            return redirect("posts:pdf_list", emp.id)  # Redirect after success
    else:
        form = FileFieldForm()  # Create an empty form for GET request

    return render(request, 'upload_pdf.html', {'form': form})

   
# List PDFs uploaded
@login_required(login_url="/users/login/")
def pdf_list(request,id):
    emp = Emp_contrat.objects.get(pk=id)  
    pdfs = emp.contrat_pdfs.all().order_by('-uploaded_at')
    # for pdf in pdfs:
    #     print(pdf.pdf_file.url)
    count = pdfs.count()            
    return render(request, 'posts/pdf_list.html', {'emp':emp,'pdfs': pdfs,'count':count})

# ------------ GET PDfs of Employee to preview using  AJAX
def get_pdfs(request):
    emp_id = request.GET.get('emp_id')

    if not emp_id:
        return JsonResponse({"error": "Missing emp_id"}, status=400)

    try:
        pdfs = PDFFile.objects.filter(n_ident_id=emp_id)

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
    pdf = PDFFile.objects.get(id=pdf_id)
    return FileResponse(pdf.pdf_file, as_attachment=True)



 