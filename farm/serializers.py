from rest_framework import serializers
from farm.models import Campo, Sector, Cultivo, Bloque, FamiliaBotanica

class SectorSerializer(serializers.ModelSerializer):
    def get_delta(self, obj):
        return obj.field.delta

    delta = serializers.SerializerMethodField("get_delta")
    class Meta:
        model = Sector
        fields = ['id', 'sector_num', 'camas', 'delta']
        read_only_fields = ['id', 'sector_num', 'camas', 'delta']

class BloqueSerializer(serializers.ModelSerializer):
    def get_familia(self, obj):
        return obj.cultivo.familia_botanica.pk

    def get_precio(self, obj):
        return obj.cultivo.precio_por_cama

    familia_botanica = serializers.SerializerMethodField("get_familia")
    precio = serializers.SerializerMethodField("get_precio")
    class Meta:
        model = Bloque
        fields = [
            'id',
            'cultivo',
            'dia_plantacion',
            'tiempo_crecimiento',
            'camas_requeridas',
            'familia_botanica',
            'precio',
            'sector',
            'cama',
        ]
        read_only_fields = [
            'id',
            'cultivo',
            'dia_plantacion',
            'tiempo_crecimiento',
            'camas_requeridas',
            'familia_botanica',
            'precio',
        ]
