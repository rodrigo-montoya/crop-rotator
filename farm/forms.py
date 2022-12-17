from django import forms
from django.forms import BaseModelForm, BaseModelFormSet, formset_factory, inlineformset_factory, modelformset_factory
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponse

from .models import Campo, Sector, FamiliaBotanica, Cultivo, Bloque


class CampoForm(forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['field_name', 'delta']


class BaseSectorFormSet(BaseModelFormSet):
    def clean(self):
        i = 1
        for form in self.forms:
            if 'camas' not in form.cleaned_data:
                msg = f'El sector {i} debe tener al menos una cama'
                form.add_error('camas', msg)
            i += 1


SectorFormSet = modelformset_factory(
    Sector,
    formset=BaseSectorFormSet,
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

class CultivoForm(forms.ModelForm):
    familia_botanica = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la familia botanica'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        familia_botanica = cleaned_data.get('familia_botanica')
        if not FamiliaBotanica.objects.filter(familia_name=familia_botanica).exists():
            the_fam = FamiliaBotanica.objects.create(familia_name=familia_botanica)
        else:
            the_fam = FamiliaBotanica.objects.get(familia_name=familia_botanica)
        cleaned_data['familia_botanica'] = the_fam
        return cleaned_data

    class Meta:
        model = Cultivo
        fields = ['cultivo_name', 'familia_botanica', 'precio_por_cama']
        labels = {
            'cultivo_name': 'Nombre del cultivo',
        }
        widgets = {
            'cultivo_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'nombre del cultivo'
            }),
            'precio_por_cama': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'precio por cama'
            })
        }

class BaseBlockFormSet(BaseModelFormSet):
    def clean(self):
        i = 1
        for form in self.forms:
            if 'dia_plantacion' not in form.cleaned_data:
                form.add_error('dia_plantacion', f'Debe ingresar un dia de plantacion en el bloque {i}')
            if 'tiempo_crecimiento' not in form.cleaned_data:
                form.add_error('tiempo_crecimiento', f'Debe ingresar el tiempo de crecimiento del cultivo en el bloque {i}')
            if 'camas_requeridas' not in form.cleaned_data:
                form.add_error('camas_requeridas', f'Debe ingresar la cantidad de camas requeridas en el bloque {i}')
            i += 1

BloquesFormset = modelformset_factory(
    Bloque,
    formset=BaseBlockFormSet,
    fields=('dia_plantacion', 'tiempo_crecimiento', 'camas_requeridas',),
    extra=1,
    widgets={
        'dia_plantacion': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'ingrese fecha de plantacion',
            'type': 'date',
        }),
        'tiempo_crecimiento': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'tiempo crecimiento del cultivo',
        }),
        'camas_requeridas': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'camas requeridas del bloque',
        }),
    }
)

