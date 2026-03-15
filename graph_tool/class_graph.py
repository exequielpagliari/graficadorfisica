import numpy as np
import matplotlib.pyplot as plt

class GraphicGenerator:
    def __init__(self, posicion_inicial=0.0, velocidad_inicial=0.0, 
                 aceleracion=0.0, tiempo=10.0, velocidad_mru=None):
        """
        Generador de gráficos cinemáticos.
        Si aceleracion es 0, se comporta como MRU.
        """
        self.posicion_inicial = posicion_inicial
        self.velocidad_inicial = velocidad_inicial
        self.aceleracion = aceleracion
        self.tiempo = tiempo
        # Para MRU, si se pasa velocidad_mru, se usa como velocidad constante
        self.velocidad_mru = velocidad_mru if velocidad_mru is not None else velocidad_inicial

    def _preparar_datos(self):
        """Genera los arrays de tiempo y posición basados en la física actual."""
        t = np.linspace(0, self.tiempo if self.tiempo > 0 else 10, 100)
        
        if self.aceleracion == 0:
            # Ecuación MRU: x = x0 + v * t
            x = self.posicion_inicial + self.velocidad_mru * t
            titulo = 'Gráfica Posición vs Tiempo (MRU)'
        else:
            # Ecuación MRUA: x = x0 + v0*t + 0.5*a*t^2
            x = self.posicion_inicial + self.velocidad_inicial * t + 0.5 * self.aceleracion * (t**2)
            titulo = 'Gráfica Posición vs Tiempo (MRUA)'
        
        return t, x, titulo

    def generate(self, filename="grafico_ejercicio.png", show=False):
        """Genera y guarda el gráfico en el archivo especificado."""
        t, x, titulo = self._preparar_datos()

        fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
        ax.plot(t, x, label='Posición $x(t)$', color='blue', linewidth=2)
        
        # Estética del gráfico
        ax.set_xlabel('Tiempo [s]')
        ax.set_ylabel('Posición [m]')
        ax.set_title(titulo)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()

        # Añadir anotaciones de valores iniciales y finales si es relevante
        ax.scatter([t[0], t[-1]], [x[0], x[-1]], color='red')
        
        print(f"Guardando gráfico en {filename}...")
        plt.savefig(filename, dpi=300)
        
        if show:
            plt.show()
        
        plt.close(fig) # Liberar memoria

    def generate_velocity_graph(self, filename="grafico_velocidad.png"):
        """Genera un gráfico de Velocidad vs Tiempo."""
        t = np.linspace(0, self.tiempo if self.tiempo > 0 else 10, 100)
        
        if self.aceleracion == 0:
            v = np.full_like(t, self.velocidad_mru)
            titulo = 'Gráfica Velocidad vs Tiempo (MRU)'
        else:
            v = self.velocidad_inicial + self.aceleracion * t
            titulo = 'Gráfica Velocidad vs Tiempo (MRUA)'

        fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
        ax.plot(t, v, label='Velocidad $v(t)$', color='green', linewidth=2)
        
        ax.set_xlabel('Tiempo [s]')
        ax.set_ylabel('Velocidad [m/s]')
        ax.set_title(titulo)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()

        plt.savefig(filename, dpi=300)
        plt.close(fig)
