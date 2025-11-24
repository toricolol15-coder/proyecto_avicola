from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "panel/login.html", {
                "error": "Usuario o contraseña incorrecta"
            })

    return render(request, "panel/login.html")

def register_view(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre_completo")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        rol = request.POST.get("rol")  # OPCIONAL, por si luego usas roles

        # VALIDAR CONTRASEÑAS
        if password1 != password2:
            return render(request, "panel/register.html", {
                "error": "Las contraseñas no coinciden"
            })

        # VALIDAR QUE EL USUARIO NO EXISTA
        if User.objects.filter(username=username).exists():
            return render(request, "panel/register.html", {
                "error": "El nombre de usuario ya está registrado"
            })

        # CREAR USUARIO
        user = User.objects.create_user(
            username=username,
            password=password1,
            first_name=nombre
        )

        # OPCIONAL: imprimir el rol seleccionado (futuro perfil)
        print("Rol del nuevo usuario:", rol)

        return redirect("login")

    return render(request, "panel/register.html")


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")



# PÁGINAS PROTEGIDAS
@login_required
def dashboard(request):
    return render(request, "panel/dashboard.html")


@login_required
def raciones(request):
    return render(request, "panel/raciones.html")


@login_required
def proyecciones(request):
    return render(request, "panel/proyecciones.html")


@login_required
def registros(request):
    return render(request, "panel/registros.html")


@login_required
def configuraciones(request):
    return render(request, "panel/configuraciones.html")

def perfil_usuario(request):
    return render(request, "panel/perfil_usuario.html")