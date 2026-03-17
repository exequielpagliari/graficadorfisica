import logging
import math

from graph_tool.exceptions import CalculationError

logger = logging.getLogger(__name__)

class ForceCalculator:
    """Calculadora de fuerzas para física.
    
    Calcula fuerzas usando la segunda ley de Newton, ley de Hooke,
    y dinámica en planos inclinados.
    Todos los métodos de cálculo lanzan CalculationError cuando faltan
    parámetros requeridos.
    
    Attributes:
        masa: Masa en kilogramos (kg).
        fuerza: Fuerza en newtons (N).
        aceleracion: Aceleración en m/s².
        mu: Coeficiente de rozamiento.
        k: Constante elástica del resorte (N/m).
        x: Elongación del resorte (m).
        angulo: Ángulo de inclinación en grados.
        g: Aceleración gravitacional (m/s²), por defecto 9.8.
    """
    
    def __init__(self, masa=None, fuerza=None, aceleracion=None, 
                 mu=0.0, k=None, x=None, angulo=0.0, g=9.8):
        self.m = masa
        self.f = fuerza
        self.a = aceleracion
        self.mu = mu  
        self.k = k    
        self.x = x    
        self.angulo = angulo # Ángulo de inclinación en grados
        self.g = g

    def calcular_plano_inclinado(self, sentido="descenso"):
        """
        Resuelve la dinámica en un plano inclinado.
        Sentido 'descenso' (baja por el plano) o 'ascenso' (se empuja hacia arriba).
        
        Raises:
            CalculationError: Si falta 'masa' o 'angulo'.
        """
        # Validar parámetros requeridos
        if self.m is None:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "Cálculo de plano inclinado fallido: falta masa",
                    extra={"operation": "calcular_plano_inclinado", "masa": None, "angulo": self.angulo}
                )
            raise CalculationError(
                "Falta el parámetro requerido 'masa' para calcular plano inclinado.",
                operation="calcular_plano_inclinado",
                context={"masa": None, "angulo": self.angulo}
            )
        
        if self.angulo is None:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "Cálculo de plano inclinado fallido: falta ángulo",
                    extra={"operation": "calcular_plano_inclinado", "masa": self.m, "angulo": None}
                )
            raise CalculationError(
                "Falta el parámetro requerido 'angulo' para calcular plano inclinado.",
                operation="calcular_plano_inclinado",
                context={"masa": self.m, "angulo": None}
            )
        
        rad = math.radians(self.angulo)
        px = self.m * self.g * math.sin(rad)
        py = self.m * self.g * math.cos(rad)
        normal = py
        f_roz = self.mu * normal
        
        # Fuerza neta en el eje X del plano
        # Si baja: F_neta = F_aplicada + Px - F_roz
        # Si sube: F_neta = F_aplicada - Px - F_roz
        f_aplicada = self.f if self.f else 0.0
        
        if sentido == "descenso":
            f_neta = f_aplicada + px - f_roz
        else:
            f_neta = f_aplicada - px - f_roz
            
        if self.a is None:
            self.a = f_neta / self.m
            if self.a < 0: self.a = 0.0
            
        return {
            "aceleracion": self.a,
            "peso_x": px,
            "peso_y": py,
            "normal": normal,
            "rozamiento": f_roz,
            "fuerza_neta": f_neta
        }

    def calcular_newton(self):
        """Resuelve F = m * a considerando rozamiento si mu > 0.
        
        Raises:
            CalculationError: Si falta 'masa' cuando es necesaria para el cálculo.
        """
        # Validar que tenemos al menos masa o fuerza y aceleración
        # Si se va a calcular aceleración, necesitamos masa
        if self.a is None and self.f is not None and self.m is None:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "Cálculo de Newton fallido: falta masa para calcular aceleración",
                    extra={"operation": "calcular_newton", "masa": None, "fuerza": self.f, "aceleracion": None}
                )
            raise CalculationError(
                "Falta el parámetro requerido 'masa' para calcular aceleración con la segunda ley de Newton.",
                operation="calcular_newton",
                context={"masa": None, "fuerza": self.f, "aceleracion": None}
            )
        
        # Si se va a calcular masa, necesitamos fuerza y aceleración
        if self.m is None and self.f is not None and self.a is not None:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "Cálculo de Newton fallido: falta masa para calcular fuerza",
                    extra={"operation": "calcular_newton", "masa": None, "fuerza": self.f, "aceleracion": self.a}
                )
            raise CalculationError(
                "Falta el parámetro requerido 'masa' para calcular fuerza con la segunda ley de Newton.",
                operation="calcular_newton",
                context={"masa": None, "fuerza": self.f, "aceleracion": self.a}
            )
        
        # Peso y Normal (asumiendo plano horizontal)
        peso = self.m * self.g if self.m else None
        f_roz = self.mu * peso if (self.mu and peso) else 0.0

        if self.f is None and self.m is not None and self.a is not None:
            self.f = (self.m * self.a) + f_roz
        elif self.m is None and self.f is not None and self.a is not None:
            self.m = self.f / (self.a + (self.mu * self.g if self.mu else 0))
        elif self.a is None and self.m is not None and self.f is not None:
            self.a = (self.f - f_roz) / self.m
            if self.a < 0: self.a = 0.0 # No hay fuerza suficiente para mover
            
        return {"fuerza": self.f, "masa": self.m, "aceleracion": self.a, "rozamiento": f_roz}

    def calcular_hooke(self):
        """Resuelve F = k * x (Ley de Hooke)."""
        if self.f is None and self.k and self.x:
            self.f = self.k * self.x
        elif self.k is None and self.f and self.x:
            self.k = self.f / self.x
        elif self.x is None and self.f and self.k:
            self.x = self.f / self.k
        return {"fuerza": self.f, "constante_k": self.k, "elongacion_x": self.x}
