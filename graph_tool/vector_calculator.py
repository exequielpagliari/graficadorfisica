import logging
import math

from graph_tool.exceptions import CalculationError

logger = logging.getLogger(__name__)

class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    @property
    def magnitud(self):
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def angulo(self):
        """Devuelve el ángulo en grados (0 a 360)."""
        ang = math.degrees(math.atan2(self.y, self.x))
        return ang if ang >= 0 else ang + 360

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        if scalar == 0:
            raise CalculationError("División por cero no permitida.")
        return Vector2D(self.x / scalar, self.y / scalar)

    @staticmethod
    def desde_polar(magnitud, angulo_deg):
        rad = math.radians(angulo_deg)
        return Vector2D(magnitud * math.cos(rad), magnitud * math.sin(rad))

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

class VectorCalculator:
    """Calculadora de vectores 2D.
    
    Realiza operaciones vectoriales como suma, resta, multiplicación
    y división por escalar.
    El método calcular() lanza CalculationError cuando faltan
    parámetros requeridos o hay división por cero.
    
    Attributes:
        v1: Primer vector (Vector2D).
        v2: Segundo vector (Vector2D).
        escalar: Escalar para multiplicación/división.
        operacion: Operación a realizar ('suma', 'resta', 'multiplicacion', 'division').
        resultado: Resultado de la última operación.
    """
    
    def __init__(self, v1=None, v2=None, escalar=None, operacion=None):
        self.v1 = v1  # Objeto Vector2D
        self.v2 = v2  # Objeto Vector2D
        self.escalar = escalar
        self.operacion = operacion
        self.resultado = None

    def calcular(self):
        """Realiza la operación especificada.
        
        Raises:
            CalculationError: Si falta algún parámetro requerido para la operación.
        """
        # Validar que se proporcionó la operación
        if self.operacion is None:
            raise CalculationError(
                "Se requiere especificar una operación.",
                operation="calcular",
                context={"operacion": self.operacion}
            )
        
        # Validar parámetros según la operación
        if self.operacion in ("suma", "resta") and (self.v1 is None or self.v2 is None):
            raise CalculationError(
                f"Se requieren dos vectores (v1 y v2) para la operación '{self.operacion}'.",
                operation="calcular",
                context={"operacion": self.operacion, "v1": self.v1, "v2": self.v2}
            )
        
        if self.operacion in ("multiplicacion", "division") and self.v1 is None:
            raise CalculationError(
                f"Se requiere un vector (v1) para la operación '{self.operacion}'.",
                operation="calcular",
                context={"operacion": self.operacion, "v1": self.v1}
            )
        
        if self.operacion in ("multiplicacion", "division") and self.escalar is None:
            raise CalculationError(
                f"Se requiere un escalar para la operación '{self.operacion}'.",
                operation="calcular",
                context={"operacion": self.operacion, "escalar": self.escalar}
            )
        
        if self.operacion == "division" and self.escalar == 0:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "División por cero en VectorCalculator.calcular()",
                    extra={"operation": "calcular", "operacion": self.operacion, "escalar": 0}
                )
            raise CalculationError(
                "División por cero no permitida.",
                operation="calcular",
                context={"operacion": self.operacion, "escalar": 0}
            )
        
        # Realizar la operación
        if self.operacion == "suma":
            self.resultado = self.v1 + self.v2
        elif self.operacion == "resta":
            self.resultado = self.v1 - self.v2
        elif self.operacion == "multiplicacion":
            self.resultado = self.v1 * self.escalar
        elif self.operacion == "division":
            self.resultado = self.v1 / self.escalar
        
        return self.resultado

    def imprimirResultados(self):
        if self.resultado:
            print(f"--- Resultado Vectorial ({self.operacion}) ---")
            print(f"Componentes: {self.resultado}")
            print(f"Magnitud: {self.resultado.magnitud:.2f}")
            print(f"Ángulo: {self.resultado.angulo:.2f}°")
        else:
            print("No se ha realizado ningún cálculo.")
