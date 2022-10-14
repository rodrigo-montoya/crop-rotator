from django.shortcuts import render
from django.views.generic.edit import CreateView, View, FormView, FormMixin
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
from django import forms
from crop_rotator.views import CreateOrUpdateView
from .models import Campo, Sector
#from .forms import SectorForm


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
    model = Campo
    fields = ['field_name', 'delta']

    def get_success_url(self):
        return reverse('farm:mi_huerta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'mi_huerta'
        context['is_add'] = self.is_add
        return context

# class SectorFormView(LoginRequiredMixin, CreateOrUpdateView):
#     template_name = "farm/sector_form.html"
#     model = Campo
#     fields = ['field_name', 'delta']

#     def get_success_url(self):
#         return reverse('farm:mi_huerta')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['segment'] = 'mi_huerta'
#         context['is_add'] = self.is_add
#         #formset = self.form_class(queryset=Sector.objects.none())
#         #context['formset'] = formset
#         return context

#     def form_valid(self, form):
#         field = Campo.objects.first()
#         counter = 0
#         for f in form:
#             counter += 1
#             obj = f.save(commit=False)
#             obj.field = field
#             obj.sector_num = counter
#             obj.save()
#         return super().form_valid(form)
class SectorFormView(FormView):
    template_name = "farm/sector_form.html"
    success_url = '/'
    form_class = modelformset_factory(
        Sector,
        fields=('camas',),
        extra=1,
        labels = {
            'camas': 'Sector',
        },
        widgets={
            'camas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cantidad de camas'
            })
        }
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(queryset=Sector.objects.none())
        context['form'] = form
        return context

    def form_valid(self, form):
        field = Campo.objects.first()
        counter = 0
        for f in form:
            counter += 1
            obj = f.save(commit=False)
            obj.field = field
            obj.sector_num = counter
            obj.save()
        return super().form_valid(form)


class CronogramaView(LoginRequiredMixin, TemplateView):
    template_name = "farm/cronograma.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'cronograma'
        return context

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