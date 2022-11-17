from django import forms
from django.forms import BaseModelForm, BaseModelFormSet, formset_factory, inlineformset_factory, modelformset_factory
from django.forms.models import BaseInlineFormSet

from .models import Campo, Sector, FamiliaBotanica, Cultivo, Bloque


class CampoForm(forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['field_name', 'delta']


SectorFormSet = modelformset_factory(
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


BloquesFormset = modelformset_factory(
    Bloque,
    fields=('dia_plantacion', 'tiempo_crecimiento', 'camas_requeridas',),
    extra=1,
    widgets={
        'dia_plantacion': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'ingrese fecha de plantacion',
            'type': 'date',
        })
    }
)

