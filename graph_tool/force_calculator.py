import math

class ForceCalculator:
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
        """
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
        """Resuelve F = m * a considerando rozamiento si mu > 0."""
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
