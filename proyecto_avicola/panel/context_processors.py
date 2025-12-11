from .models import Insumo


def stock_summary(request):
    """Context processor que agrega un resumen de insumos y alertas de stock."""
    insumos_qs = Insumo.objects.all()
    insumos = {}
    alertas_stock = []

    for ins in insumos_qs:
        # calcular nivel de alerta
        try:
            stock_actual = float(ins.stock_actual)
            stock_minimo = float(ins.stock_minimo)
        except Exception:
            stock_actual = ins.stock_actual
            stock_minimo = ins.stock_minimo

        if stock_actual <= stock_minimo:
            nivel = 'CRITICO'
        elif stock_actual <= stock_minimo * 2:
            nivel = 'BAJO'
        else:
            nivel = 'NORMAL'

        insumos[ins.nombre] = {
            'stock_actual': ins.stock_actual,
            'unidad': ins.unidad,
            'nivel_alerta': nivel,
        }

        if nivel in ('CRITICO', 'BAJO'):
            alertas_stock.append({
                'nombre': ins.nombre,
                'stock_actual': ins.stock_actual,
                'nivel': nivel,
            })

    # ordenar alertas por nivel (CRITICO primero)
    alertas_stock.sort(key=lambda x: 0 if x['nivel'] == 'CRITICO' else 1)

    return {
        'insumos': insumos,
        'alertas_stock': alertas_stock,
    }
