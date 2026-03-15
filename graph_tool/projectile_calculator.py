import math

class ProjectileCalculator:
    def __init__(self, v0=0.0, angulo_deg=45.0, h0=0.0, g=9.8):
        self.v0 = float(v0)
        self.angulo = float(angulo_deg)
        self.h0 = float(h0)
        self.g = float(g)
        
        # Componentes iniciales
        rad = math.radians(self.angulo)
        self.v0x = self.v0 * math.cos(rad)
        self.v0y = self.v0 * math.sin(rad)
        
        # Resultados
        self.tiempo_vuelo = 0.0
        self.alcance_max = 0.0
        self.altura_max = 0.0

    def calcular(self):
        """Calcula los parámetros del tiro oblicuo."""
        # Tiempo de vuelo (usando la fórmula cuadrática para y = 0)
        # 0 = h0 + v0y*t - 0.5*g*t^2  =>  0.5*g*t^2 - v0y*t - h0 = 0
        a = 0.5 * self.g
        b = -self.v0y
        c = -self.h0
        
        discriminante = b**2 - 4*a*c
        if discriminante >= 0:
            t1 = (-b + math.sqrt(discriminante)) / (2*a)
            t2 = (-b - math.sqrt(discriminante)) / (2*a)
            self.tiempo_vuelo = max(t1, t2)
        
        # Alcance máximo
        self.alcance_max = self.v0x * self.tiempo_vuelo
        
        # Altura máxima (v_y = 0)
        tiempo_pico = self.v0y / self.g
        self.altura_max = self.h0 + self.v0y * tiempo_pico - 0.5 * self.g * (tiempo_pico**2)
        
        return {
            "tiempo_vuelo": self.tiempo_vuelo,
            "alcance_max": self.alcance_max,
            "altura_max": self.altura_max,
            "v0x": self.v0x,
            "v0y": self.v0y
        }

    def obtener_trayectoria(self, puntos=100):
        """Genera puntos (x, y) para graficar la parábola."""
        tiempos = [t * (self.tiempo_vuelo / (puntos-1)) for t in range(puntos)]
        x = [self.v0x * t for t in tiempos]
        y = [self.h0 + self.v0y * t - 0.5 * self.g * (t**2) for t in tiempos]
        return x, y
