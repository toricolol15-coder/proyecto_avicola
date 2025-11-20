from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect


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


@login_required
def login_view(request):
    return render(request, "panel/login.html")


# SOLO ADMIN PUEDE VER DASHBOARD
@permission_required('panel.view_racion', raise_exception=True)
def dashboard(request):
    if not request.user.is_superuser:
        return redirect("raciones")  # redirigir al trabajador
    return render(request, "panel/dashboard.html")


# SOLO TRABAJADOR
@login_required
@permission_required('panel.view_racion', raise_exception=True)
def raciones(request):
    return render(request, "panel/raciones.html")


# SOLO ADMIN
@login_required
def proyecciones(request):
    if not request.user.is_superuser:
        return redirect("raciones")
    return render(request, "panel/proyecciones.html")


# SOLO ADMIN
@login_required
def registros(request):
    if not request.user.is_superuser:
        return redirect("raciones")
    return render(request, "panel/registros.html")


# SOLO ADMIN
@login_required
def configuraciones(request):
    if not request.user.is_superuser:
        return redirect("raciones")
    return render(request, "panel/configuraciones.html")
