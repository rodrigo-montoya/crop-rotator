from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import math

# Create your models here.
# class User(AbstractUser):
#     pass

class Campo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="campos")
    field_name = models.CharField(max_length=64)
    delta = models.IntegerField()

    def __str__(self):
        return self.field_name

class Sector(models.Model):
    field = models.ForeignKey(Campo, on_delete=models.CASCADE, related_name="sectores")
    sector_num = models.IntegerField()
    camas = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.field) + ' ' + str(self.sector_num)

    # class meta:
    #     unique_together = ('field', 'sector_num')

class FamiliaBotanica(models.Model):
    familia_name = models.CharField(max_length=64)

    def __str__(self):
        return self.familia_name

class Cultivo(models.Model):
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE, related_name="cultivos")
    cultivo_name = models.CharField(max_length=64)
    familia_botanica = models.ForeignKey(FamiliaBotanica, on_delete=models.CASCADE, related_name="cultivos")
    precio_por_cama = models.IntegerField()

    def __str__(self):
        return self.cultivo_name

class Bloque(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name="bloques")
    dia_plantacion = models.DateField()
    tiempo_crecimiento = models.IntegerField()
    camas_requeridas = models.IntegerField()
    # precio = models.IntegerField()
    # dia_finalizar = models.DateField()
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="bloques", null=True, blank=True)
    cama = models.IntegerField(default=-1)
    active = models.BooleanField(default=True)
    chosen = models.BooleanField(default=False)
    bloque_num = models.IntegerField()

    def __str__(self):
        return self.cultivo.cultivo_name + ' ' + str(self.bloque_num)

    @property
    def valor(self):
        return self.cultivo.precio_por_cama * self.camas_requeridas

    @property
    def valor_tiempo(self):
        return math.floor(self.valor / self.tiempo_crecimiento)

    @property
    def familia(self):
        return self.cultivo.familia_botanica.familia_name

    @property
    def valor_por_cama(self):
        return self.cultivo.precio_por_cama

    class Meta:
        ordering = ['cultivo', 'bloque_num']