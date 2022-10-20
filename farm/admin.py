from django.contrib import admin
from farm.models import (
    Campo,
    Sector,
    FamiliaBotanica,
    Cultivos,
    Bloques,
)

# Register your models here.

@admin.register(Campo)
class CampoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "field_name",
        "delta"
    )

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'field',
        "sector_num",
        "camas"
    )

@admin.register(FamiliaBotanica)
class FamiliaBotanicaAdmin(admin.ModelAdmin):
    list_display = (
        "familia_name",
    )

@admin.register(Cultivos)
class CultivosAdmin(admin.ModelAdmin):
    list_display = (
        "cultivo_name",
        "familia_botanica"
    )

@admin.register(Bloques)
class BloquesAdmin(admin.ModelAdmin):
    list_display = (
        "cultivo",
        "dia_planatacion",
        "tiempo_crecimiento",
        "camas_requeridas",
        "precio",
        "dia_finalizar",
        "sector",
        "cama"
    )