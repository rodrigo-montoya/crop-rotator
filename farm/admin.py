import math
from django.contrib import admin
from django.db.models import F
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
        "user",
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
        "familia",
        "valor_por_cama",
        "dia_plantacion",
        "tiempo_crecimiento",
        "camas_requeridas",
        "bloque_num",
        "sector",
        "cama",
        "active",
        "chosen"
    )

    # def valor(self, obj):
    #     return obj.cultivo.precio_por_cama * obj.camas_requeridas

    # def valor_tiempo(self, obj):
    #     return math.floor(obj.cultivo.precio_por_cama * obj.camas_requeridas / obj.tiempo_crecimiento)