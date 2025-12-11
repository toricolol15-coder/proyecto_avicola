from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name="logout"),

    # Panel interno
    path('dashboard/', views.dashboard, name="dashboard"),
    path('raciones/', views.raciones, name="raciones"),
    path('proyecciones/', views.proyecciones, name="proyecciones"),
    path('registros/', views.registros, name="registros"),
    path('configuraciones/', views.configuraciones, name="configuraciones"),
    path('perfil/', views.perfil_usuario, name="perfil_usuario"),

    # Acciones sobre registros
    path('registros/editar/<int:id>/', views.registro_editar, name="registro_editar"),
    path('registros/eliminar/<int:id>/', views.registro_eliminar, name="registro_eliminar"),

    # Guardar raciones desde el formulario
    path('guardar-racion/', views.guardar_racion, name="guardar_racion"),

# Stock
    path('stock/', views.stock, name="stock"),
    path('stock/agregar/<int:id>/', views.stock_agregar, name="stock_agregar"),
    path('stock/crear/', views.stock_crear, name="stock_crear"),
    path('stock/editar/<int:id>/', views.stock_editar, name="stock_editar"),

]
