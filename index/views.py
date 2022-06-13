from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .forms import *
import re
from .models import Post
from django.views.generic import ListView, CreateView # новый
from django.urls import reverse_lazy # новый 
from .forms import PostForm # новый
#from tensorflow import keras
from .semantic import *
import numpy as np
from .antifakesearcher import predict_proba
import os
#import cv2

class HomePageView(ListView):
    model = Post
    template_name = 'home.html'#home

class CreatePostView(CreateView): # новый
    model = Post
    form_class = PostForm
    template_name = 'post.html'
    success_url = reverse_lazy('index')

def index(request):

    regiondata = []
 

    for region in Region_data:
        regiondata.append(region[0])
    context = {
        'фото': 'foto1',
        'информация': 'info1',
        'regions': 'data1'
    }
    return render(request, 'index/index.html', context=context)


def list(request):
    global query_result
    fotos=[]
    infos=[]
    query_result =  {
        'Names': fotos,
        'Infos': 0,
        'Itogs': 0
    }
    model = Post
    text=" "
    BASE_DIR2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT2 = os.path.join(BASE_DIR2, 'media//images')
    MOD = os.path.join(BASE_DIR2, 'media/antifake.model')
    for c in os.listdir(MEDIA_ROOT2):
        full_path = os.path.join(MEDIA_ROOT2, c)
        if os.path.isfile(full_path):
            fotos.append(c)
            with open(full_path, "r", encoding='utf-8') as file:
                for item in file:
                    text=text+" "+str(item)


            r = predict_proba(str(text))
            #print(""+text)
            infos.append(f'Вероятность содержания фейковой информации:{round(r[1] * 100, 2)}%')
            query_result =  {
                'Names': fotos,
                'Infos': infos,
                'Itogs': 3
            }
        else:
            query_result =  {
                'Names': 'Отсутствует файл с новостью для анализа!',
                'Infos': 0,
                'Itogs': 0
            }
    for c in os.listdir(MEDIA_ROOT2):
       full_path = os.path.join(MEDIA_ROOT2, c)
       if os.path.isfile(full_path):
           os.remove(full_path)        
    return render(request, 'index/list.html', context=query_result)


def search(request):
   
    query_result =  {
        'Name': 4,
        'Info': 5,
        'Itog': 6
    }
    photo ='hghghg'
    return render(request, 'index/list.html', context=photo)
    # else:
    # return redirect('index')

def posto(request):
    orgInfo = request.POST["orgInfo"]
    p = re.compile('\W')   # Check if the input has any non alphanumeric charaters
    specialChars = p.findall(orgInfo)
    for chars in specialChars:
        if chars != ' ':
            return redirect('index') # Redirect to index if undesirable input
    form = SearchForm({'search': orgInfo})
    if form.is_valid():
        orgs = OrgBaseInfo.objects.filter(
            Name__icontains=orgInfo).order_by('Region')
        return render(request, 'index/post.html', context={'query_result': orgs})
    else:
        return redirect('index')
# Org_Base_Info

class OrgbaseInfoCreate(LoginRequiredMixin, CreateView):
    model = OrgBaseInfo
    form_class = OrgBaseInfoForm

class OrgBaseInfoUpdate(LoginRequiredMixin, UpdateView):
    model = OrgBaseInfo
    form_class = OrgBaseInfoForm
    context_object_name = 'org'
    template_name = 'index/orgbaseinfo_form.html'

    def get_success_url(self):
        id = self.kwargs['pk']
        return reverse_lazy('details', kwargs={'id': id})


class OrgDelete(LoginRequiredMixin, DeleteView):
    model = OrgBaseInfo
    success_url = reverse_lazy('index')


@login_required
def OrgDelete(request, pk):
    org = OrgBaseInfo.objects.get(id=pk)
    org.delete()
    return redirect('index')


# Industry Options ------------>
@login_required
def EditIndustryOptions(request):
    industries = Industry.objects.all()
    context = {
        "objects":industries,
        "title": "Industry"
    }
    return render(request, 'index/industry_options.html', context=context)

class AddIndustry(LoginRequiredMixin, CreateView):
    model = Industry
    form_class = IndustryForm
    template = "index/industry_form.html"
    def form_valid(self, form):
        form.save()
        return redirect('options_industry')

class UpdateIndustry(LoginRequiredMixin, UpdateView):
    model = Industry
    form_class = IndustryForm
    context_object_name = 'industry'
    
    def form_valid(self, form):
        form.save()
        return redirect('options_industry')

@login_required
def DeleteIndustry(request, pk):
    industry = Industry.objects.get(id=pk)
    industry.delete()
    return redirect('options_industry')

# Service Options
@login_required
def EditServiceCategoryOptions(request):
    services = ServiceCategory.objects.all()
    context = {
        "objects":services,
        "title": "Service"
    }
    return render(request, 'index/serviceCategory_options.html', context=context)

class AddServiceCategory(LoginRequiredMixin, CreateView):
    model = ServiceCategory
    form_class = addServiceCategoryForm
    template_name = "index/servicecategory_form.html"
    success_url = reverse_lazy('options_serviceCategory')
   
    def form_valid(self, form):
        form.save()
        return redirect('options_serviceCategory')

class UpdateServiceCategory(LoginRequiredMixin, UpdateView):
    model = ServiceCategory
    form_class = addServiceCategoryForm
    context_object_name = 'serviceCategory'
    def form_valid(self, form):
        form.save()
        return redirect('options_serviceCategory')

@login_required
def DeleteServiceCategory(request, pk):
    service = ServiceCategory.objects.get(id=pk)
    service.delete()
    return redirect('options_serviceCategory')


# Service
@method_decorator(login_required, name='dispatch')
class ServiceCreate(CreateView):
    model = Service
    form_class = ServiceForm
    context_object_name = 'org'

    def form_valid(self, form):
        service = form.save(commit=False)
        service.OrgName = OrgBaseInfo.objects.get(id=self.kwargs["pk"])
        service.save()
        form.save_m2m()
        return redirect('details', id=self.kwargs["pk"])


class ServiceUpdate(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    context_object_name = 'service'


@login_required
def ServiceDelete(request, pk):
    service = Service.objects.get(id=pk)
    orgid = service.OrgName.id
    service.delete()
    return redirect('details', id=int(orgid))


# Experience
class ExperienceCreate(LoginRequiredMixin, CreateView):
    model = Experience
    form_class = ExperienceForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.OrgName = OrgBaseInfo.objects.get(id=self.kwargs["pk"])
        instance.save()
        return redirect('details', id=self.kwargs["pk"])


class ExperienceUpdate(LoginRequiredMixin, UpdateView):
    model = Experience
    form_class = ExperienceForm


class ExperienceDelete(LoginRequiredMixin, DeleteView):
    model = Experience
    success_url = reverse_lazy('index')


# Case
class CaseCreate(LoginRequiredMixin, CreateView):
    model = Case
    form_class = CaseForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.OrgName = OrgBaseInfo.objects.get(id=self.kwargs["pk"])
        instance.save()
        form.save_m2m()
        return redirect('details', id=self.kwargs["pk"])


class CaseUpdate(LoginRequiredMixin, UpdateView):
    model = Case
    form_class = CaseForm
    context_object_name = 'case'


@login_required
def CaseDelete(request, pk):
    case = Case.objects.get(id=pk)
    orgid = case.OrgName.id
    case.delete()
    return redirect('details', id=int(orgid))


class Peoples(models.Model):
    peopless = range(10)

