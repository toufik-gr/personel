from django.shortcuts import render, redirect, get_object_or_404
from .models import Enseignant, PDF_enseign
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import FileResponse
from django.contrib import messages
#--------------------------------------
from django.db.models import Count
#---------------------------------------------
from .filters import PdfsEnsFilter
#from django.db.models import Q

#-----------------------------------------------
#from django.views.generic.edit import FormView
from .utils import get_filtered_enseign_list
from urllib.parse import unquote
from django.core.paginator import Paginator
#-------------------------------------------

# --- Api with filter and search
from rest_framework.decorators import api_view, permission_classes # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Enseignant
from .serializers import EnseigSerializer



USER_FACULTY_MAP = {
    "pol1_user": ['الرياضة','كلية الطب','الطبيعة والحياة','الرياضيات وعلوم المادة','معهد التكنولوجيا'],
    "pol2_user": ['الإقتصاد','اللغات','العلوم الإنسانية','الحقوق و العلوم السياسية'],
    "pol3_user" : ['التكنولوجيات الحديثة','العلوم التطبيقية','المحروقات'],
}

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enseignant_list_api(request):
    #queryset = Enseignant.objects.all()
    username = request.user.username
    allowed_faculties = USER_FACULTY_MAP.get(username, [])
    print(allowed_faculties)
    
    queryset= Enseignant.objects.filter(faculte__in=allowed_faculties)
    
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
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = EnseigSerializer(result_page, many=True)
    count = serializer.data.count(queryset)

    return paginator.get_paginated_response({
        'count': queryset.count(),        # Total enseignants matching filters
        'results': serializer.data        # Current page data
    })


@api_view(['POST'])
def create_enseign(request):
    data = request.data
    serializer = EnseigSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET' , 'PUT', 'DELETE'])
def enseign_detail(request, pk):
    try:
        ens = Enseignant.objects.get(pk=pk)
    except ens.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EnseigSerializer(ens)
        return Response(serializer.data)
        
    if request.method == 'DELETE':
        ens.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        data = request.data
        serializer = EnseigSerializer(ens, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#----Api Upload pdf Files ------------
from .models import PDF_enseign, Enseignant

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_pdf_folder(request):
    files = request.FILES.getlist('pdfs')
    grade = request.POST.get('grade')
    enseignant_id = request.POST.get('n_ident')
    # user = request.user

    if not files or not grade or not enseignant_id:
        return Response({'error': 'Missing files or metadata'}, status=400)

    try:
        enseignant = Enseignant.objects.get(id=enseignant_id)
    except Enseignant.DoesNotExist:
        return Response({'error': 'Invalid Enseignant ID'}, status=404)

    for file in files:
        if file.name.endswith('.pdf'):
            PDF_enseign.objects.create(
                pdf_file=file,
                grade=grade,
                user=request.user,
                n_ident=enseignant
            )

    return Response({'message': 'PDFs uploaded successfully!'})

# --- PDF list api
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pdfs_for_enseignant(request, enseignant_id):
    try:
        enseignant = Enseignant.objects.get(id=enseignant_id)
    except Enseignant.DoesNotExist:
        return Response({'error': 'Enseignant not found'}, status=404)
    
    grade = request.GET.get("grade")
    pdfs = PDF_enseign.objects.filter(n_ident=enseignant).order_by('-uploaded_at')
    if grade:
        pdfs = pdfs.filter(grade=grade)

    data = [
        {
            "id": pdf.id,
            "file": request.build_absolute_uri(pdf.pdf_file.url),
            "uploaded_at": pdf.uploaded_at,
            "user": pdf.user.username,
            "n_ident" : enseignant.id,
            "grade": pdf.grade,
        }
        for pdf in pdfs
    ]
    return Response(data)

#---api ---
"""
from django.shortcuts import get_object_or_404
from .models import Enseignant, PDF_enseign
from .serializers import PDFEnseignSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pdf_list_api(request, id):
    enseignant = get_object_or_404(Enseignant, pk=id)
    pdfs = enseignant.enseign_pdfs.all().order_by('-uploaded_at')

    # Optional: filter using GET parameters (manual filtering or custom filter class)
    grade = request.GET.get('grade')
    if grade:
        pdfs = pdfs.filter(grade=grade)

    serializer = PDFEnseignSerializer(pdfs, many=True)
    return Response({
        'count': pdfs.count(),
        'enseignant': {
            'id': enseignant.id,
            'Nom': enseignant.Nom,
            'Prenom': enseignant.Prenom,
        },
        'pdfs': serializer.data
    })
"""
# --- ens api -----

# ---- end Api ----------









# --- show emp_list  to update  
@login_required(login_url="/users/login/")
def enseign_list_global(request,action): 
    user = request.user.username
    context= get_filtered_enseign_list(request, user)
     
    if action == 'update':
        context['action'] = {'action_name': 'تحديث', 'action_title': 'قائمة الأساتذة والتحديث'}
    
    elif action == 'add_file':
        context ['action']= {'action_name' :'إضافة_ملفات', 'action_title': 'إضافة ملفات الأساتذة'}
    
    elif action == 'view':     # for view emp : pdfs using AJAX   
         context ['action'] = {'action_name': 'معاينة', 'action_title': 'عرض ملفات الأساتذة'}
    
    elif action == 'preview':  # for preview emp : pdfs using django
        context['action'] = {'action_name': 'معاينة_ملف', 'action_title': 'معاينة ملفات الأساتذة'}
     
     
    return render(request,'emp_list_global.html',context )    


# ------------ GET PDfs of Employee to preview
from django.http import JsonResponse

# View before Update Employe  
@login_required(login_url="/users/login/")
def view_enseign(request,id):
    ens = Enseignant.objects.get(pk=id)
    form = UpdateFormf(instance=ens)  # Create  form TO GET request
    if request.method == "POST":
        form = UpdateFormf(request.POST, instance=ens)
        if form.is_valid():
            form.save()         
           
        return redirect("enseignants:update_ens", ens.id)
    else:
        form = UpdateFormf(instance=ens)
         
    return render(request, 'enseignants/viewEns.html', {'form': form})

# Update Employe  
@login_required(login_url="/users/login/")
def update_enseign(request,id):
    ens = Enseignant.objects.get(pk=id)
     
    if request.method == "POST":
        form = UpdateFormf(request.POST, instance=ens)
        if form.is_valid():
            form = form.save()
          
        messages.success(request,"!تم التحديث بنجاح")
        return redirect('enseignList', 'update')  # Redirect after success
         
    else:
        form = UpdateFormf(instance=ens)  # Create an empty form for GET request
         
    return render(request, 'enseignants/updateEns.html', {'form': form})

# Upload PDF View  
@login_required(login_url="/users/login/")
def upload_ens_pdf(request,id):
    ens = Enseignant.objects.get(pk=id)
    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data["file_field"]  # Extract list of files
            grade = form.cleaned_data["grade"]
            for file in files:
                PDF_enseign.objects.create(pdf_file=file, 
                user = request.user,
                grade = grade,        
                n_ident = ens) # Save each file separately
            messages.success(request,"!تم إضافة الملف بنجاح")
            return redirect("enseignants:pdf_list", ens.id)  # Redirect after success
    else:
        form = FileFieldForm()  # Create an empty form for GET request

    return render(request, 'upload_pdf.html', {'form': form})

   
# List PDFs uploaded
@login_required(login_url="/users/login/")
def pdf_list(request,id):
    ens = Enseignant.objects.get(pk=id)  
    pdfs = ens.enseign_pdfs.all().order_by('-uploaded_at')
    filtePDFEns = PdfsEnsFilter(request.GET, queryset=pdfs)
    pdfs = filtePDFEns.qs 
    count = pdfs.count() 
    context = {'filter_pdf': filtePDFEns, 'ens':ens,'pdfs': pdfs,'count':count}

    return render(request, 'enseignants/pdf_list.html',context)

# ------------ GET PDfs of Employee to preview using  AJAX

def get_pdfs(request):
    emp_id = request.GET.get('emp_id')

    if not emp_id:
        return JsonResponse({"error": "Missing emp_id"}, status=400)

    try:
        pdfs = PDF_enseign.objects.filter(n_ident_id=emp_id)

        if not pdfs.exists():
            return JsonResponse([], safe=False)  # Return empty list if no PDFs found

        pdf_list = [
            {
                'id': pdf.id,
                'pdf_url': pdf.pdf_file.url,
                'grade' : pdf.grade,
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
    pdf = PDF_enseign.objects.get(id=pdf_id)
    return FileResponse(pdf.pdf_file, as_attachment=True)