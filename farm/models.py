from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class User(AbstractUser):
#     pass

class Campo(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="campos")
    field_name = models.CharField(max_length=64)
    delta = models.IntegerField()

    def __str__(self):
        return self.field_name

class Sector(models.Model):
    field = models.ForeignKey(Campo, on_delete=models.CASCADE, related_name="sectores")
    sector_num = models.IntegerField()
    camas = models.IntegerField()

    def __str__(self):
        return str(self.sector_num)

class FamiliaBotanica(models.Model):
    familia_name = models.CharField(max_length=64)

    def __str__(self):
        return self.familia_name

class Cultivos(models.Model):
    cultivo_name = models.CharField(max_length=64)
    familia_botanica = models.ForeignKey(FamiliaBotanica, on_delete=models.CASCADE, related_name="cultivos")

    def __str__(self):
        return self.cultivo_name

class Bloques(models.Model):
    cultivo = models.ForeignKey(Cultivos, on_delete=models.CASCADE, related_name="bloques")
    dia_planatacion = models.DateField()
    tiempo_crecimiento = models.IntegerField()
    camas_requeridas = models.IntegerField()
    precio = models.IntegerField()
    dia_finalizar = models.DateField()
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="bloques", null=True, blank=True)
    cama = models.IntegerField(default=-1)

    def __str__(self):
        return self.bloque_name