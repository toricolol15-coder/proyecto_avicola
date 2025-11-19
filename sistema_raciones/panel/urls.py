from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('raciones/', views.raciones, name='raciones'),
    path('proyecciones/', views.proyecciones, name='proyecciones'),
    path('registros/', views.registros, name='registros'),
    path('configuraciones/', views.configuraciones, name='configuraciones'),
]
