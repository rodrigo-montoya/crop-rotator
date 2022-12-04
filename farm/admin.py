from django.contrib import admin
from farm.models import (
    Campo,
    Sector,
    FamiliaBotanica,
    Cultivo,
    Bloque,
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
        "camas",
        "active"
    )

@admin.register(FamiliaBotanica)
class FamiliaBotanicaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        "familia_name",
    )

@admin.register(Cultivo)
class CultivosAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "campo",
        "cultivo_name",
        "familia_botanica",
        "precio_por_cama"
    )

@admin.register(Bloque)
class BloqueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cultivo",
        "dia_plantacion",
        "tiempo_crecimiento",
        "camas_requeridas",
        #"precio",
        #"dia_finalizar",
        "sector",
        "cama",
        "bloque_num",
        "active",
    )
