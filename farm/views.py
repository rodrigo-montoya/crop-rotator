from django.shortcuts import render
from django.views.generic.edit import CreateView, View, FormView, FormMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.forms import formset_factory, modelformset_factory
from crop_rotator.views import CreateOrUpdateView
from .models import Campo, Sector, Cultivo, Bloque, FamiliaBotanica
from . import forms
from django import forms as django_forms
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import BloqueSerializer, SectorSerializer

import requests
import json


@login_required(login_url="/accounts/login/")
def index(request):
    context = {'segment': 'inicio'}

    html_template = loader.get_template('farm/inicio.html')
    return HttpResponse(html_template.render(context, request))

class MiHuertaView(LoginRequiredMixin, TemplateView):
    template_name = "farm/mi_huerta.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'mi_huerta'
        context['campo_exists'] = False
        campo_exists = Campo.objects.exists()
        if campo_exists:
            context['campo_exists'] = True
            context['campo'] = Campo.objects.first()
        return context

class HuertaCreateUpdateView(LoginRequiredMixin, CreateOrUpdateView):
    template_name = "farm/sector_form.html"
    model = Campo
    fields = ['field_name', 'delta']
    sector_form = forms.SectorFormSet

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['field_name'].widget = django_forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del campo'})
        form.fields['delta'].widget = django_forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'dias requeridos entre cultivos de la misma familia botanica'})
        return form

    def get_success_url(self):
        return reverse('farm:mi_huerta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'mi_huerta'
        context['is_add'] = self.is_add
        # formset = None
        # if self.is_add:
        #     formset = self.sector_form(queryset=Sector.objects.none())
        # else:
        #     formset = self.sector_form(queryset=Sector.objects.filter(field=self.object))
        formset = self.sector_form(queryset=Sector.objects.none())
        context['sector_forms'] = formset
        return context

    def form_valid(self, form):
        formset = self.sector_form(self.request.POST)
        if form.is_valid() and formset.is_valid():
            campo = form.save()
            all_sectors = Sector.objects.filter(field=campo)
            all_sectors.update(active=False)
            total_sectors = all_sectors.count()
            counter = 0
            for sector in formset:
                counter += 1
                if counter > total_sectors:
                    obj = sector.save(commit=False)
                    obj.field = campo
                    obj.sector_num = counter
                else:
                    obj = Sector.objects.filter(field=campo, sector_num=counter).first()
                    obj.camas = sector.cleaned_data.get('camas')
                    obj.active = True
                obj.save()
            return super().form_valid(form)
        else:
            #FIXME: make a prettier version of this
            return HttpResponse(formset.errors)


class MisCultivosView(LoginRequiredMixin, ListView):
    template_name = "farm/mis_cultivos.html"
    model = Cultivo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'mis_cultivos'
        return context


class MisCultivosCreateUpdateView(LoginRequiredMixin, CreateOrUpdateView):
    template_name = "farm/cultivo_form.html"
    model = Cultivo
    form_class = forms.CultivoForm
    bloque_form = forms.BloquesFormset

    def get_success_url(self):
        return reverse('farm:mis_cultivos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'mis_cultivos'
        context['is_add'] = self.is_add
        formset = None
        # if self.is_add:
        #     formset = self.sector_form(queryset=Sector.objects.none())
        # else:
        #     formset = self.sector_form(queryset=Sector.objects.filter(field=self.object))
        formset = self.bloque_form(queryset=Bloque.objects.none())
        context['bloque_forms'] = formset
        return context

    def form_valid(self, form):
        formset = self.bloque_form(self.request.POST)
        if form.is_valid() and formset.is_valid():
            cultivo = form.save(commit=False)
            cultivo.campo = Campo.objects.first()
            cultivo.save()
            all_bloques = Bloque.objects.filter(cultivo=cultivo)
            all_bloques.update(active=False)
            total_bloques = all_bloques.count()
            counter = 0
            for bloque in formset:
                counter += 1
                if counter > total_bloques:
                    obj = bloque.save(commit=False)
                    obj.cultivo = cultivo
                    obj.bloque_num = counter
                else:
                    obj = Bloque.objects.filter(cultivo=cultivo, bloque_num=counter).first()
                    obj.dia_plantacion = bloque.cleaned_data.get('dia_plantacion')
                    obj.tiempo_crecimiento = bloque.cleaned_data.get('tiempo_crecimiento')
                    obj.camas_requeridas = bloque.cleaned_data.get('camas_requeridas')
                    obj.active = True
                    obj.bloque_num = counter
                obj.save()
            return super().form_valid(form)
        else:
            #FIXME: make a prettier version of this
            return HttpResponse(formset.errors)


class CronogramaView(LoginRequiredMixin, ListView):
    model = Sector
    paginate_by = 1
    template_name = "farm/cronograma.html"

    def get_queryset(self):
        return Sector.objects.filter(field=Campo.objects.first(), active=True).order_by('sector_num')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'cronograma'
        campo = Campo.objects.first()
        context['campo'] = campo
        cultivos = Cultivo.objects.filter(campo=campo)
        context['cultivos'] = {}
        i = 0
        for cultivo in cultivos:
            context['cultivos'][cultivo.cultivo_name] = i
            i += 1
        return context


class PostTestView(LoginRequiredMixin, TemplateView):
    template_name = "farm/post_test.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     campo = Campo.objects.first()
    #     bloques_json = BloqueSerializer(Bloque.objects.filter(cultivo__campo=campo), many=True).data
    #     sectores_json = SectorSerializer(Sector.objects.filter(field=campo), many=True).data
    #     other_page_response = requests.post(
    #         'http://optimizer:5000/', json = {'sectores': sectores_json, 'bloques': bloques_json}
    #     )
    #     context['other_page_response'] = other_page_response.json()
    #     return context

    def post(self, request, *args, **kwargs):
        campo = Campo.objects.first()
        bloques_json = BloqueSerializer(Bloque.objects.filter(cultivo__campo=campo), many=True).data
        sectores_json = SectorSerializer(Sector.objects.filter(field=campo), many=True).data
        other_page_response = requests.post(
            'http://optimizer:5000/', json = {'sectores': sectores_json, 'bloques': bloques_json}
        )
        bloque_instances = []
        for bloque in json.loads(other_page_response.json()):
            bloque_instance = Bloque.objects.get(id=bloque['id'])
            bloque_instance.sector = Sector.objects.get(id=bloque['sector'])
            bloque_instance.cama = bloque['cama']
            bloque_instance.save()
            bloque_instances.append(bloque_instance)
        serializer = BloqueSerializer(bloque_instances, many=True)

        messages.success(request, serializer.data)
        # messages.success(request, bloque_instances)

        return HttpResponseRedirect(reverse('farm:post_test'))


class BloqueApiView(viewsets.ModelViewSet):
    queryset = Bloque.objects.all()
    serializer_class = BloqueSerializer

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

class SectorApiView(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class MiUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = "farm/pagina_usuario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'mi_usuario'
        return context


# @login_required(login_url="accounts/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('farm/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))