import math

class EnergyCalculator:
    def __init__(self, masa=None, velocidad=None, altura=None, 
                 k=None, x=None, g=9.8):
        self.m = masa
        self.v = velocidad
        self.h = altura
        self.k = k
        self.x = x
        self.g = g

    def calcular_cinetica(self):
        """Ec = 0.5 * m * v^2"""
        if self.m is not None and self.v is not None:
            return 0.5 * self.m * (self.v**2)
        return None

    def calcular_potencial_gravitatoria(self):
        """Epg = m * g * h"""
        if self.m is not None and self.h is not None:
            return self.m * self.g * self.h
        return None

    def calcular_potencial_elastica(self):
        """Epe = 0.5 * k * x^2"""
        if self.k is not None and self.x is not None:
            return 0.5 * self.k * (self.x**2)
        return None

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
