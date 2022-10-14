from django.urls import path, re_path
from . import views

app_name = __name__.split('.')[0]

urlpatterns = [
    path('', views.index, name='home'),
    path('mi_huerta/', views.MiHuertaView.as_view(), name='mi_huerta'),
    path('mi_huerta/create/', views.HuertaCreateUpdateView.as_view(), name='huerta_create'),
    path('mi_huerta/update/<int:pk>/', views.HuertaCreateUpdateView.as_view(), name='huerta_update'),
    path('sector_form/', views.SectorFormView.as_view(), name='sector_form'),
    path('cronograma/', views.CronogramaView.as_view(), name='cronograma'),
    path('mi_usuario/', views.MiUsuarioView.as_view(), name='mi_usuario'),
    #re_path(r'^.*\.*', views.pages, name='pages'),
]
