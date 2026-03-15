import math

class PhysicCalculator:
    def __init__(self, posicion_inicial=None, posicion_final=None, 
                 velocidad_inicial=None, velocidad_final=None, aceleracion=None, 
                 tiempo=None, velocidad=None):
        self.posicion_inicial = posicion_inicial
        self.posicion_final = posicion_final
        self.velocidad_inicial = velocidad_inicial
        self.velocidad_final = velocidad_final
        self.aceleracion = aceleracion
        self.tiempo = tiempo
        self.velocidad = velocidad 

    def _get_value(self, val):
        return val if val is not None else 0.0

    def calcular(self):
        print("Iniciando motor de cálculo físico (MRU/MRUA)...")
        
        # 1. Sincronización inicial para MRU
        # Si la aceleración es 0 o las velocidades son iguales, es MRU
        if self.aceleracion == 0 or (self.velocidad_inicial is not None and self.velocidad_final is not None and self.velocidad_inicial == self.velocidad_final):
            self.aceleracion = 0.0
            v_values = [v for v in [self.velocidad, self.velocidad_inicial, self.velocidad_final] if v is not None]
            if v_values:
                self.velocidad = self.velocidad_inicial = self.velocidad_final = v_values[0]

        # Desplazamiento (dx)
        dx = None
        if self.posicion_inicial is not None and self.posicion_final is not None:
            dx = self.posicion_final - self.posicion_inicial

        # 2. Resolución iterativa (Ecuaciones de cinemática)
        # Se realizan varias pasadas para resolver variables dependientes
        for _ in range(3): 
            cambio = False
            
            # --- Ecuación 1: vf = vi + a*t ---
            if self.velocidad_final is None and all(v is not None for v in [self.velocidad_inicial, self.aceleracion, self.tiempo]):
                self.velocidad_final = self.velocidad_inicial + self.aceleracion * self.tiempo
                cambio = True
            if self.velocidad_inicial is None and all(v is not None for v in [self.velocidad_final, self.aceleracion, self.tiempo]):
                self.velocidad_inicial = self.velocidad_final - self.aceleracion * self.tiempo
                cambio = True
            if self.aceleracion is None and all(v is not None for v in [self.velocidad_final, self.velocidad_inicial, self.tiempo]) and self.tiempo != 0:
                self.aceleracion = (self.velocidad_final - self.velocidad_inicial) / self.tiempo
                cambio = True
            if self.tiempo is None and all(v is not None for v in [self.velocidad_final, self.velocidad_inicial, self.aceleracion]) and self.aceleracion != 0:
                self.tiempo = (self.velocidad_final - self.velocidad_inicial) / self.aceleracion
                cambio = True

            # --- Ecuación 2: dx = vi*t + 0.5*a*t^2 ---
            if dx is None and all(v is not None for v in [self.velocidad_inicial, self.aceleracion, self.tiempo]):
                dx = self.velocidad_inicial * self.tiempo + 0.5 * self.aceleracion * (self.tiempo**2)
                cambio = True
            if self.velocidad_inicial is None and all(v is not None for v in [dx, self.aceleracion, self.tiempo]) and self.tiempo != 0:
                self.velocidad_inicial = (dx - 0.5 * self.aceleracion * (self.tiempo**2)) / self.tiempo
                cambio = True
            if self.aceleracion is None and all(v is not None for v in [dx, self.velocidad_inicial, self.tiempo]) and self.tiempo != 0:
                self.aceleracion = 2 * (dx - self.velocidad_inicial * self.tiempo) / (self.tiempo**2)
                cambio = True
            # Resolver t (cuadrática: 0.5*a*t^2 + vi*t - dx = 0)
            if self.tiempo is None and all(v is not None for v in [dx, self.velocidad_inicial, self.aceleracion]) and self.aceleracion != 0:
                A, B, C = 0.5 * self.aceleracion, self.velocidad_inicial, -dx
                disc = B**2 - 4*A*C
                if disc >= 0:
                    t1 = (-B + math.sqrt(disc)) / (2*A)
                    t2 = (-B - math.sqrt(disc)) / (2*A)
                    self.tiempo = t1 if t1 >= 0 else (t2 if t2 >= 0 else None)
                    if self.tiempo is not None: cambio = True

            # --- Ecuación 3: vf^2 = vi^2 + 2*a*dx ---
            if self.velocidad_final is None and all(v is not None for v in [self.velocidad_inicial, self.aceleracion, dx]):
                res = self.velocidad_inicial**2 + 2 * self.aceleracion * dx
                if res >= 0: 
                    self.velocidad_final = math.sqrt(res)
                    cambio = True
            if self.velocidad_inicial is None and all(v is not None for v in [self.velocidad_final, self.aceleracion, dx]):
                res = self.velocidad_final**2 - 2 * self.aceleracion * dx
                if res >= 0: 
                    self.velocidad_inicial = math.sqrt(res)
                    cambio = True
            if dx is None and all(v is not None for v in [self.velocidad_final, self.velocidad_inicial, self.aceleracion]) and self.aceleracion != 0:
                dx = (self.velocidad_final**2 - self.velocidad_inicial**2) / (2 * self.aceleracion)
                cambio = True
            if self.aceleracion is None and all(v is not None for v in [self.velocidad_final, self.velocidad_inicial, dx]) and dx != 0:
                self.aceleracion = (self.velocidad_final**2 - self.velocidad_inicial**2) / (2 * dx)
                cambio = True

            # --- Ecuación 4: dx = (vi + vf)/2 * t ---
            if dx is None and all(v is not None for v in [self.velocidad_inicial, self.velocidad_final, self.tiempo]):
                dx = ((self.velocidad_inicial + self.velocidad_final) / 2) * self.tiempo
                cambio = True
            if self.tiempo is None and all(v is not None for v in [dx, self.velocidad_inicial, self.velocidad_final]) and (self.velocidad_inicial + self.velocidad_final) != 0:
                self.tiempo = (2 * dx) / (self.velocidad_inicial + self.velocidad_final)
                cambio = True

            if not cambio: 
                break

        # 3. Sincronización final
        if dx is not None:
            if self.posicion_inicial is not None and self.posicion_final is None: 
                self.posicion_final = self.posicion_inicial + dx
            if self.posicion_final is not None and self.posicion_inicial is None: 
                self.posicion_inicial = self.posicion_final - dx
        
        if self.aceleracion == 0:
            if self.velocidad is None: 
                self.velocidad = self.velocidad_inicial if self.velocidad_inicial is not None else self.velocidad_final
            self.velocidad_inicial = self.velocidad_final = self.velocidad

    def imprimirResultados(self):
        print("\n--- Resultados de la Simulación ---")
        def f(val, unit): return f"{val:.2f} {unit}" if val is not None else "N/A"
        print(f"Posición Inicial:  {f(self.posicion_inicial, 'm')}")
        print(f"Posición Final:    {f(self.posicion_final, 'm')}")
        print(f"Velocidad Inicial: {f(self.velocidad_inicial, 'm/s')}")
        print(f"Velocidad Final:   {f(self.velocidad_final, 'm/s')}")
        print(f"Aceleración:       {f(self.aceleracion, 'm/s²')}")
        print(f"Tiempo:            {f(self.tiempo, 's')}")
        if self.aceleracion == 0:
            print(f"Velocidad Const:   {f(self.velocidad, 'm/s')}")
