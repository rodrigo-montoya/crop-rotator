from django import forms
from django.forms import formset_factory, modelformset_factory

from .models import Campo, Sector, FamiliaBotanica, Cultivos, Bloques


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
