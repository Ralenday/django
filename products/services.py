# products/services.py
# Capa de servicios: aquí vive la lógica de negocio (cálculos y decisiones),
# separada de las vistas.


# Patrón de comportamiento (Strategy): cada clase encapsula una forma
# distinta de calcular el precio y todas comparten la misma interfaz
class EstrategiaDescuento:
    def calcular(self, precio):
        raise NotImplementedError


class DescuentoElectronica(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * 0.90  # 10% de descuento


class DescuentoRopa(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * 0.80  # 20% de descuento


class SinDescuento(EstrategiaDescuento):
    def calcular(self, precio):
        return precio


def obtener_estrategia(categoria_nombre):
    # Selecciona la estrategia según el nombre de la categoría del producto
    estrategias = {
        'Electronica': DescuentoElectronica(),
        'Ropa': DescuentoRopa(),
    }
    return estrategias.get(categoria_nombre, SinDescuento())
