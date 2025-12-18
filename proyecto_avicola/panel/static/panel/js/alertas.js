// Sistema de alertas animadas para toda la aplicación
// Versión: 1.0

function mostrarMensaje(tipo, mensaje) {
    // Buscar o crear el contenedor de alertas
    let alerta = document.getElementById("mensaje-alerta-global");
    if (!alerta) {
        alerta = document.createElement("div");
        alerta.id = "mensaje-alerta-global";
        alerta.className = "alert";
        alerta.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            min-width: 300px;
            max-width: 500px;
            display: none;
        `;
        document.body.appendChild(alerta);
    }

    let texto = alerta.querySelector(".mensaje-texto");
    if (!texto) {
        texto = document.createElement("span");
        texto.className = "mensaje-texto";
        alerta.appendChild(texto);
    }

    // Limpiar clases anteriores
    alerta.className = "alert";

    // Agregar clase según tipo
    if (tipo === "error") {
        alerta.classList.add("alert-warning");
    } else if (tipo === "warning") {
        alerta.classList.add("alert-warning");
    } else if (tipo === "success") {
        alerta.classList.add("alert-success");
    } else {
        alerta.classList.add("alert-info");
    }

    // Agregar animación
    if (tipo === "error") {
        alerta.classList.add("alerta-bounce");
        // Para errores, agregar también shake después del bounce
        setTimeout(() => {
            alerta.classList.add("alerta-shake");
        }, 600);
    } else {
        alerta.classList.add("alerta-bounce");
    }

    texto.innerHTML = mensaje;
    alerta.style.display = "block";

    // Remover las animaciones después de que terminen
    setTimeout(() => {
        alerta.classList.remove("alerta-bounce", "alerta-shake");
    }, 1100);

    // Auto-ocultar después de 5 segundos para errores/warnings
    if (tipo === "error" || tipo === "warning") {
        setTimeout(() => {
            ocultarMensajeGlobal();
        }, 5000);
    }
}

function ocultarMensajeGlobal() {
    const alerta = document.getElementById("mensaje-alerta-global");
    if (alerta) {
        alerta.style.display = "none";
    }
}

function confirmarAccion(mensaje, callback) {
    mostrarMensaje("warning", mensaje + "\n\n¿Confirmar acción?", "confirm");
    // Para simplificar, por ahora usamos confirm tradicional
    // pero podemos mejorar esto después
    if (confirm(mensaje)) {
        callback(true);
    } else {
        callback(false);
    }
}

// Función para validar números con comas/puntos
function parseNumber(value, fieldName) {
    if (!value || value.trim() === "") {
        throw new Error(`El campo ${fieldName} es obligatorio`);
    }

    // Convertir comas a puntos
    let normalizedValue = value.replace(',', '.');

    let num = parseFloat(normalizedValue);
    if (isNaN(num)) {
        throw new Error(`El campo ${fieldName} debe ser un número válido`);
    }

    return num;
}

// Función para validar formularios con animaciones
function validarFormulario(formElement, reglasValidacion) {
    try {
        const formData = new FormData(formElement);

        for (const [campo, regla] of Object.entries(reglasValidacion)) {
            const valor = formData.get(campo);

            if (regla.required && (!valor || valor.trim() === "")) {
                throw new Error(`El campo ${regla.label || campo} es obligatorio`);
            }

            if (regla.type === "number" && valor) {
                const num = parseNumber(valor, regla.label || campo);
                if (regla.min !== undefined && num < regla.min) {
                    throw new Error(`El campo ${regla.label || campo} debe ser mayor o igual a ${regla.min}`);
                }
                if (regla.max !== undefined && num > regla.max) {
                    throw new Error(`El campo ${regla.label || campo} debe ser menor o igual a ${regla.max}`);
                }
            }

            if (regla.pattern && !regla.pattern.test(valor)) {
                throw new Error(regla.message || `El formato del campo ${regla.label || campo} es inválido`);
            }
        }

        return true;
    } catch (error) {
        mostrarMensaje("error", error.message);
        return false;
    }
}