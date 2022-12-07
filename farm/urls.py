from django.urls import path, re_path
from . import views

app_name = __name__.split('.')[0]

urlpatterns = [
    path('', views.index, name='home'),
    path('mi_huerta/', views.MiHuertaView.as_view(), name='mi_huerta'),
    path('mi_huerta/create/', views.HuertaCreateUpdateView.as_view(), name='huerta_create'),
    path('mi_huerta/update/<int:pk>/', views.HuertaCreateUpdateView.as_view(), name='huerta_update'),
    path('mis_cultivos/', views.MisCultivosView.as_view(), name='mis_cultivos'),
    path('mis_cultivos/create', views.MisCultivosCreateUpdateView.as_view(), name='mis_cultivos_create'),
    path('mis_cultivos/update/<int:pk>/', views.MisCultivosCreateUpdateView.as_view(), name='mis_cultivos_update'),
    # path('sector_form/create/', views.SectorFormView.as_view(), name='sector_form'),
    # path('sector_form/update/<int:pk>', views.SectorFormView.as_view(), name='sector_form'),
    path('calendario/', views.CalendarioView.as_view(), name='calendario'),
    #path('post_test/', views.PostTestView.as_view(), name='post_test'),
    path('mi_usuario/', views.MiUsuarioView.as_view(), name='mi_usuario'),
    #re_path(r'^.*\.*', views.pages, name='pages'),
]
