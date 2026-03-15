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

    def generate(self, filename="grafico_ejercicio.png", show=False, save=True):
        """Genera el gráfico. En web, save=False."""
        t, x, titulo = self._preparar_datos()
        fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
        ax.plot(t, x, label='Posición $x(t)$', color='blue', linewidth=2)
        ax.set_xlabel('Tiempo [s]'); ax.set_ylabel('Posición [m]'); ax.set_title(titulo)
        ax.grid(True, linestyle='--', alpha=0.7); ax.legend()
        ax.scatter([t[0], t[-1]], [x[0], x[-1]], color='red')
        
        if save:
            plt.savefig(filename, dpi=300)
            if show: plt.show()
            plt.close(fig)
        return fig

    def generate_velocity_graph(self, filename="grafico_velocidad.png", save=True):
        t = np.linspace(0, self.tiempo if self.tiempo > 0 else 10, 100)
        v = np.full_like(t, self.velocidad_mru) if self.aceleracion == 0 else self.velocidad_inicial + self.aceleracion * t
        fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
        ax.plot(t, v, label='Velocidad $v(t)$', color='green', linewidth=2)
        ax.set_xlabel('Tiempo [s]'); ax.set_ylabel('Velocidad [m/s]'); ax.set_title('Gráfica Velocidad')
        ax.grid(True, linestyle='--', alpha=0.7); ax.legend()
        
        if save:
            plt.savefig(filename, dpi=300)
            plt.close(fig)
        return fig

    def generate_vector_graph(self, vectores, labels, titulo="Gráfico de Vectores", filename="grafico_vector.png", save=True):
        fig, ax = plt.subplots(figsize=(6, 6))
        max_val = max([max(abs(v.x), abs(v.y), 1.0) for v in vectores]) * 1.2
        colores = ['blue', 'green', 'red', 'purple', 'orange']
        for i, v in enumerate(vectores):
            ax.quiver(0, 0, v.x, v.y, angles='xy', scale_units='xy', scale=1, color=colores[i % len(colores)], label=labels[i])
        ax.set_xlim(-max_val, max_val); ax.set_ylim(-max_val, max_val)
        ax.axhline(0, color='black', lw=1); ax.axvline(0, color='black', lw=1)
        ax.grid(True, alpha=0.6); ax.set_aspect('equal'); ax.set_title(titulo); ax.legend()
        
        if save:
            plt.savefig(filename, dpi=300); plt.close(fig)
        return fig

    def generate_projectile_graph(self, x, y, titulo="Trayectoria", filename="grafico_proyectil.png", save=True):
        fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
        ax.plot(x, y, color='darkorange', lw=2.5); ax.fill_between(x, y, color='orange', alpha=0.2)
        ax.set_xlabel('Distancia [m]'); ax.set_ylabel('Altura [m]'); ax.set_title(titulo); ax.grid(True, alpha=0.6)
        if min(y) >= 0: ax.set_ylim(bottom=0)
        
        if save:
            plt.savefig(filename, dpi=300); plt.close(fig)
        return fig

    def generate_dcl_graph(self, fuerzas, labels, titulo="DCL", filename="grafico_dcl.png", save=True):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.add_patch(plt.Rectangle((-0.5, -0.5), 1, 1, color='lightgray', ec='black', lw=2))
        ax.text(0, 0, "m", ha='center', va='center', fontweight='bold')
        colores = ['red', 'blue', 'green', 'purple', 'orange']
        for i, f in enumerate(fuerzas):
            mag = np.sqrt(f.x**2 + f.y**2)
            if mag == 0: continue
            vx, vy = (f.x/mag) * 1.5, (f.y/mag) * 1.5
            ax.quiver(f.x/mag * 0.5, f.y/mag * 0.5, vx, vy, angles='xy', scale_units='xy', scale=1, color=colores[i % len(colores)], width=0.015)
            ax.text(vx + (f.x/mag * 1.15), vy + (f.y/mag * 0.6), labels[i], color=colores[i % len(colores)], fontweight='bold')
        ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.axis('off'); ax.set_title(titulo, pad=20, fontweight='bold')
        
        if save:
            plt.savefig(filename, dpi=300); plt.close(fig)
        return fig

    def generate_inclined_plane_graph(self, angulo, fuerzas, labels, filename="grafico_plano.png", save=True):
        fig, ax = plt.subplots(figsize=(8, 6))
        rad = np.radians(angulo); base_long = 5; h = base_long * np.tan(rad)
        ax.add_patch(plt.Polygon([[0, 0], [base_long, 0], [base_long, h]], color='#dfe6e9', ec='black', lw=2))
        from matplotlib.transforms import Affine2D
        px, py = base_long/2, h/2
        ax.add_patch(plt.Rectangle((-0.5, 0), 1.0, 0.6, color='#b2bec3', ec='black', lw=1.5, transform=Affine2D().rotate(rad).translate(px, py) + ax.transData))
        cx, cy = px - 0.3 * np.sin(rad), py + 0.3 * np.cos(rad)
        colores = ['#d63031', '#0984e3', '#00b894', '#6c5ce7', '#e17055']
        for i, f in enumerate(fuerzas):
            mag = np.sqrt(f.x**2 + f.y**2)
            if mag == 0: continue
            vx, vy = (f.x/mag) * 1.2, (f.y/mag) * 1.2
            ax.quiver(cx, cy, vx, vy, angles='xy', scale_units='xy', scale=1, color=colores[i % len(colores)], width=0.012, zorder=5)
            ax.text(cx + vx*1.2, cy + vy*1.2, labels[i], color=colores[i % len(colores)], fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        ax.set_xlim(-1, base_long+1); ax.set_ylim(-1, max(h+1, 4)); ax.set_aspect('equal'); ax.axis('off')
        
        if save:
            plt.savefig(filename, dpi=300, bbox_inches='tight'); plt.close(fig)
        return fig
