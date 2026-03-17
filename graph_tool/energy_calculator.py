import logging
import math

from graph_tool.exceptions import CalculationError

logger = logging.getLogger(__name__)

class EnergyCalculator:
    """Calculadora de energía para física.
    
    Calcula energía cinética, potencial gravitatoria y potencial elástica.
    Todos los métodos de cálculo lanzan CalculationError cuando faltan
    parámetros requeridos.
    
    Attributes:
        masa: Masa en kilogramos (kg).
        velocidad: Velocidad en metros por segundo (m/s).
        altura: Altura en metros (m).
        k: Constante elástica del resorte (N/m).
        x: Elongación del resorte (m).
        g: Aceleración gravitacional (m/s²), por defecto 9.8.
    """
    
    def __init__(self, masa=None, velocidad=None, altura=None, 
                 k=None, x=None, g=9.8):
        self.m = masa
        self.v = velocidad
        self.h = altura
        self.k = k
        self.x = x
        self.g = g

    def calcular_cinetica(self):
        """Ec = 0.5 * m * v^2
        
        Raises:
            CalculationError: Si falta 'masa' o 'velocidad'.
        """
        if self.m is None:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "Cálculo de energía cinética fallido: falta masa",
                    extra={"operation": "calcular_cinetica", "masa": None, "velocidad": self.v}
                )
            raise CalculationError(
                "Falta el parámetro requerido 'masa' para calcular energía cinética.",
                operation="calcular_cinetica",
                context={"masa": None, "velocidad": self.v}
            )
        
        if self.v is None:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "Cálculo de energía cinética fallido: falta velocidad",
                    extra={"operation": "calcular_cinetica", "masa": self.m, "velocidad": None}
                )
            raise CalculationError(
                "Falta el parámetro requerido 'velocidad' para calcular energía cinética.",
                operation="calcular_cinetica",
                context={"masa": self.m, "velocidad": None}
            )
        
        return 0.5 * self.m * (self.v**2)

    def calcular_potencial_gravitatoria(self):
        """Epg = m * g * h
        
        Raises:
            CalculationError: Si falta 'masa' o 'altura'.
        """
        if self.m is None:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "Cálculo de energía potencial gravitatoria fallido: falta masa",
                    extra={"operation": "calcular_potencial_gravitatoria", "masa": None, "altura": self.h}
                )
            raise CalculationError(
                "Falta el parámetro requerido 'masa' para calcular energía potencial gravitatoria.",
                operation="calcular_potencial_gravitatoria",
                context={"masa": None, "altura": self.h}
            )
        
        if self.h is None:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "Cálculo de energía potencial gravitatoria fallido: falta altura",
                    extra={"operation": "calcular_potencial_gravitatoria", "masa": self.m, "altura": None}
                )
            raise CalculationError(
                "Falta el parámetro requerido 'altura' para calcular energía potencial gravitatoria.",
                operation="calcular_potencial_gravitatoria",
                context={"masa": self.m, "altura": None}
            )
        
        return self.m * self.g * self.h

    def calcular_potencial_elastica(self):
        """Epe = 0.5 * k * x^2
        
        Raises:
            CalculationError: Si falta 'k' (constante elástica) o 'x' (elongación).
        """
        if self.k is None:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "Cálculo de energía potencial elástica fallido: falta constante k",
                    extra={"operation": "calcular_potencial_elastica", "k": None, "x": self.x}
                )
            raise CalculationError(
                "Falta el parámetro requerido 'k' (constante elástica) para calcular energía potencial elástica.",
                operation="calcular_potencial_elastica",
                context={"k": None, "x": self.x}
            )
        
        if self.x is None:
            if logger.isEnabledFor(logging.ERROR):
                logger.error(
                    "Cálculo de energía potencial elástica fallido: falta elongación x",
                    extra={"operation": "calcular_potencial_elastica", "k": self.k, "x": None}
                )
            raise CalculationError(
                "Falta el parámetro requerido 'x' (elongación) para calcular energía potencial elástica.",
                operation="calcular_potencial_elastica",
                context={"k": self.k, "x": None}
            )
        
        return 0.5 * self.k * (self.x**2)

    def resolver_variable(self, tipo_energia, valor_energia):
        """Despeja una variable faltante dado el valor de la energía."""
        if tipo_energia == "cinetica":
            if self.m is None and self.v: self.m = (2 * valor_energia) / (self.v**2)
            elif self.v is None and self.m: self.v = math.sqrt((2 * valor_energia) / self.m)
        elif tipo_energia == "gravitatoria":
            if self.m is None and self.h: self.m = valor_energia / (self.g * self.h)
            elif self.h is None and self.m: self.h = valor_energia / (self.m * self.g)
        elif tipo_energia == "elastica":
            if self.k is None and self.x: self.k = (2 * valor_energia) / (self.x**2)
            elif self.x is None and self.k: self.x = math.sqrt((2 * valor_energia) / self.k)
