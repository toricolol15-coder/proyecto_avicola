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

    # Guardar proyecciones desde el formulario
    path('guardar-proyeccion/', views.guardar_proyeccion, name="guardar_proyeccion"),

    # Exportar proyecciones
    path('exportar-proyecciones-excel/', views.exportar_proyecciones_excel, name="exportar_proyecciones_excel"),

    # API para detalle de proyección
    path('api/proyeccion/<int:id>/', views.api_proyeccion_detalle, name="api_proyeccion_detalle"),

# Stock
    path('stock/', views.stock, name="stock"),
    path('stock/agregar/<int:id>/', views.stock_agregar, name="stock_agregar"),
    path('stock/crear/', views.stock_crear, name="stock_crear"),
    path('stock/editar/<int:id>/', views.stock_editar, name="stock_editar"),

    # Producción de huevos
    path('produccion-huevos/', views.produccion_huevos, name="produccion_huevos"),
    path('produccion-huevos/editar/<int:id>/', views.produccion_huevos_editar, name="produccion_huevos_editar"),
    path('produccion-huevos/eliminar/<int:id>/', views.produccion_huevos_eliminar, name="produccion_huevos_eliminar"),

]
