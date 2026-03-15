import math

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
            raise ValueError("División por cero no permitida.")
        return Vector2D(self.x / scalar, self.y / scalar)

    @staticmethod
    def desde_polar(magnitud, angulo_deg):
        rad = math.radians(angulo_deg)
        return Vector2D(magnitud * math.cos(rad), magnitud * math.sin(rad))

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

class VectorCalculator:
    def __init__(self, v1=None, v2=None, escalar=None, operacion=None):
        self.v1 = v1  # Objeto Vector2D
        self.v2 = v2  # Objeto Vector2D
        self.escalar = escalar
        self.operacion = operacion
        self.resultado = None

    def calcular(self):
        """Realiza la operación especificada."""
        if self.operacion == "suma" and self.v1 and self.v2:
            self.resultado = self.v1 + self.v2
        elif self.operacion == "resta" and self.v1 and self.v2:
            self.resultado = self.v1 - self.v2
        elif self.operacion == "multiplicacion" and self.v1 and self.escalar is not None:
            self.resultado = self.v1 * self.escalar
        elif self.operacion == "division" and self.v1 and self.escalar is not None:
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
