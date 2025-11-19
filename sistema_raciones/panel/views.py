from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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
