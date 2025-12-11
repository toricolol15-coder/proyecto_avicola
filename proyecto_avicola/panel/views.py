from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import RegistroRacion, RegistroUsuario
from .models import Insumo  # Asegúrate de ponerlo arriba con tus otros imports
import json



# ================== LOGIN ==================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "panel/login.html", {"error": "Usuario o contraseña incorrecta"})

    return render(request, "panel/login.html")


# ================== REGISTRO ==================
def register_view(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre_completo")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "panel/register.html", {"error": "Las contraseñas no coinciden"})

        if User.objects.filter(username=username).exists():
            return render(request, "panel/register.html", {"error": "Usuario ya registrado"})

        User.objects.create_user(
            username=username,
            password=password1,
            first_name=nombre
        )
        return redirect("login")

    return render(request, "panel/register.html")


# ================== LOGOUT ==================
def logout_view(request):
    logout(request)
    return redirect("login")


# ================== PÁGINAS PROTEGIDAS ==================
@login_required
def dashboard(request):
    return render(request, "panel/dashboard.html")

@login_required
def raciones(request):
    dias = [
        ("Lunes", "L"), ("Martes", "M"), ("Miércoles", "X"),
        ("Jueves", "J"), ("Viernes", "V"), ("Sábado", "S"), ("Domingo", "D")
    ]
    return render(request, "panel/raciones.html", {"dias": dias})

@login_required
def proyecciones(request):
    # Obtener todas las raciones guardadas
    raciones = RegistroRacion.objects.all().order_by('-creado_en')

    # Crear opciones solo con tipo de animal y peso
    opciones = []
    raciones_data = {}
    for r in raciones:
        opciones.append({
            "id": r.id,
            "descripcion": f"{r.tipo_animal} - {r.peso} kg"
        })
        # incluir datos relevantes por ración para uso en JS
        raciones_data[r.id] = {
            "granos": float(r.granos) if r.granos is not None else 0,
            "algas": float(r.algas) if r.algas is not None else 0,
            "peso": float(r.peso) if r.peso is not None else 0,
            "dias": r.dias,
        }

    return render(request, "panel/proyecciones.html", {
        "raciones": opciones,
        "raciones_data_json": json.dumps(raciones_data)
    })

@login_required
def registros(request):
    registros = RegistroRacion.objects.all()
    return render(request, "panel/registros.html", {"registros": registros})

@login_required
def configuraciones(request):
    return render(request, "panel/configuraciones.html")

@login_required
def perfil_usuario(request):
    return render(request, "panel/perfil_usuario.html")


# ================== REGISTROS ==================
@login_required
def registro_eliminar(request, id):
    registro = get_object_or_404(RegistroRacion, id=id)
    registro.delete()
    return redirect("registros")

@login_required
def registro_editar(request, id):
    registro = get_object_or_404(RegistroRacion, id=id)

    if request.method == "POST":
        registro.tipo_animal = request.POST.get("tipo_animal")
        registro.peso = request.POST.get("peso")
        registro.granos = request.POST.get("granos")
        registro.algas = request.POST.get("algas")
        registro.dias = request.POST.get("dias")
        registro.save()
        return redirect("registros")

    dias = [
        ("Lunes", "L"), ("Martes", "M"), ("Miércoles", "X"),
        ("Jueves", "J"), ("Viernes", "V"), ("Sábado", "S"), ("Domingo", "D")
    ]
    return render(request, "panel/editar_registro.html", {"registro": registro, "dias": dias})


# ================== GUARDAR RACIONES ==================
@login_required
def guardar_racion(request):
    if request.method == "POST":
        tipo = request.POST.get("tipo_animal")
        peso = request.POST.get("peso")
        granos = request.POST.get("granos")
        algas = request.POST.get("algas")
        dias_list = request.POST.getlist("dias")  # lista de días seleccionados
        dias = " - ".join(dias_list)  # convertir a string tipo "Lunes - Martes"

        registro = RegistroRacion.objects.create(
            tipo_animal=tipo,
            peso=peso,
            granos=granos,
            algas=algas,
            dias=dias
        )

        # Si es petición AJAX, devuelve JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"ok": True, "id": registro.id})

        return redirect("registros")

    return redirect("raciones")


@login_required
def stock(request):
    insumos = Insumo.objects.all()
    alertas_stock = []

    for insumo in insumos:
        if insumo.stock_actual <= insumo.stock_minimo:
            nivel = 'Crítico'
        elif insumo.stock_actual <= insumo.stock_minimo * 2:
            nivel = 'Bajo'
        else:
            nivel = 'Normal'
        alertas_stock.append({
            'nombre': insumo.nombre,
            'stock_actual': insumo.stock_actual,
            'nivel': nivel
        })

    return render(request, "panel/stock.html", {
        'insumos': insumos,
        'alertas_stock': alertas_stock
    })

@login_required
def stock_agregar(request, id):
    insumo = get_object_or_404(Insumo, id=id)
    if request.method == "POST":
        try:
            cantidad = float(request.POST.get("cantidad", 0))
            if cantidad < 0:
                return render(request, "panel/stock_agregar.html", {
                    "insumo": insumo,
                    "error": "La cantidad no puede ser negativa"
                })
            insumo.stock_actual += cantidad
            insumo.save()
            return redirect("stock")
        except ValueError:
            return render(request, "panel/stock_agregar.html", {
                "insumo": insumo,
                "error": "Ingresa un número válido"
            })
    return render(request, "panel/stock_agregar.html", {"insumo": insumo})


@login_required
def stock_crear(request):
    """Crear un nuevo insumo"""
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        unidad = request.POST.get("unidad", "kg").strip()
        stock_actual = float(request.POST.get("stock_actual", 0))
        stock_minimo = float(request.POST.get("stock_minimo", 0))
        porcentaje_bodega = float(request.POST.get("porcentaje_bodega", 0))

        if not nombre:
            return render(request, "panel/stock_crear.html", {
                "error": "El nombre del insumo es requerido"
            })

        if Insumo.objects.filter(nombre=nombre).exists():
            return render(request, "panel/stock_crear.html", {
                "error": f"El insumo '{nombre}' ya existe"
            })

        Insumo.objects.create(
            nombre=nombre,
            unidad=unidad,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo,
            porcentaje_ocupado_bodega=porcentaje_bodega
        )
        return redirect("stock")

    return render(request, "panel/stock_crear.html")


@login_required
def stock_editar(request, id):
    insumo = get_object_or_404(Insumo, id=id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        try:
            stock_actual = float(request.POST.get('stock_actual', insumo.stock_actual))
            stock_minimo = float(request.POST.get('stock_minimo', insumo.stock_minimo))
        except ValueError:
            return render(request, 'panel/editar_stock.html', {
                'insumo': insumo,
                'error': 'Valores numéricos inválidos'
            })

        if nombre:
            insumo.nombre = nombre
        insumo.stock_actual = stock_actual
        insumo.stock_minimo = stock_minimo
        insumo.save()
        return redirect('stock')

    return render(request, 'panel/editar_stock.html', {'insumo': insumo})