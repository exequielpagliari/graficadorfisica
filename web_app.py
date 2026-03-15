import json
import random
import base64
import math
from io import BytesIO
from pyscript import document, display, window
from graph_tool.physic_calculator import PhysicCalculator
from graph_tool.class_graph import GraphicGenerator
from graph_tool.vector_calculator import Vector2D, VectorCalculator
from graph_tool.projectile_calculator import ProjectileCalculator
from graph_tool.force_calculator import ForceCalculator

class WebOrchestrator:
    VERSION = "0.1.0"
    def __init__(self):
        with open("data/ejercicios.json", "r", encoding="utf-8") as f:
            self.pool = json.load(f)
        self.templates = {
            "base": open("templates/examen_base.tex", encoding="utf-8").read(),
            "ejercicio": open("templates/ejercicio_fragmento.tex", encoding="utf-8").read(),
            "respuesta": open("templates/respuesta_fragmento.tex", encoding="utf-8").read()
        }
        self.final_tex = ""

    def fig_to_base64(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        import matplotlib.pyplot as plt
        plt.close(fig)
        return img_str

    def generar_y_mostrar(self, counts):
        ejercicios_tex = []
        respuestas_tex = []
        n = 1
        document.getElementById("graph-preview").innerHTML = ""
        
        # Diccionario de mapeo de funciones
        mapping = [
            (counts['mru'], "mru"),
            (counts['mrua'], "mrua"),
            (counts['vectores'], "vectores"),
            (counts['oblicuo'], "oblicuo"),
            (counts['newton'], "newton"),
            (counts['plano'], "plano")
        ]

        for cant, tipo in mapping:
            for _ in range(cant):
                bloque, res, fig = self.resolver_ejercicio(n, tipo)
                ejercicios_tex.append(bloque)
                respuestas_tex.append(res)
                
                # Renderizar en la web
                img = document.createElement("img")
                img.src = f"data:image/png;base64,{self.fig_to_base64(fig)}"
                img.style.margin = "10px"
                img.title = f"Ejercicio {n}"
                document.getElementById("graph-preview").appendChild(img)
                n += 1

        self.final_tex = self.templates["base"].replace("{{ CONTENIDO_EJERCICIOS }}", "\n".join(ejercicios_tex))
        self.final_tex = self.final_tex.replace("{{ CLAVE_RESPUESTAS }}", "\n".join(respuestas_tex))
        
        document.getElementById("output-tex").value = self.final_tex
        document.getElementById("result-card").style.display = "block"

    def resolver_ejercicio(self, n, tipo):
        gen_graf = GraphicGenerator()
        resultado = ""
        enunciado = ""
        fig = None

        if tipo in ["mru", "mrua"]:
            if tipo == "mru":
                v, t, pi = random.randint(5, 30), random.randint(5, 60), random.choice([0, 10, 50])
                calc = PhysicCalculator(posicion_inicial=pi, velocidad=v, tiempo=t, aceleracion=0)
                enunciado_raw = random.choice(self.pool["mru"])
            else:
                vi, a, t = random.randint(0, 25), random.randint(1, 10), random.randint(2, 15)
                calc = PhysicCalculator(posicion_inicial=0.0, velocidad_inicial=vi, aceleracion=a, tiempo=t)
                enunciado_raw = random.choice(self.pool["mrua"])
            
            calc.calcular()
            enunciado = enunciado_raw.format(
                v=f"{calc.velocidad:.1f}" if calc.velocidad else "0",
                vi=f"{calc.velocidad_inicial:.1f}" if calc.velocidad_inicial else "0",
                vf=f"{calc.velocidad_final:.1f}" if calc.velocidad_final else "0",
                a=f"{calc.aceleracion:.1f}" if calc.aceleracion else "0",
                t=f"{calc.tiempo:.1f}" if calc.tiempo else "0",
                pi=f"{calc.posicion_inicial:.1f}" if calc.posicion_inicial else "0",
                pf=f"{calc.posicion_final:.1f}" if calc.posicion_final else "0"
            )
            gen_graf = GraphicGenerator(posicion_inicial=calc.posicion_inicial or 0, velocidad_inicial=calc.velocidad_inicial or 0, aceleracion=calc.aceleracion or 0, tiempo=calc.tiempo or 10, velocidad_mru=calc.velocidad)
            fig = gen_graf.generate(save=False)
            resultado = f"Posición Final: {calc.posicion_final:.2f} m, Velocidad Final: {calc.velocidad_final:.2f} m/s"

        elif tipo == "vectores":
            op = random.choice(["suma", "resta", "multiplicacion", "division"])
            v1, v2, s = Vector2D(random.randint(-10, 10), random.randint(-10, 10)), Vector2D(random.randint(-10, 10), random.randint(-10, 10)), random.randint(2, 5)
            calc = VectorCalculator(v1=v1, v2=v2, escalar=s, operacion=op)
            res_v = calc.calcular()
            enunciados = self.pool["vectores"]
            idx = ["suma", "resta", "multiplicacion", "division"].index(op)
            enunciado = enunciados[idx].format(v1=str(v1), v2=str(v2), s=str(s), res=str(res_v))
            if op in ["suma", "resta"]: fig = gen_graf.generate_vector_graph([v1, v2, res_v], ["A", "B", "R"], save=False)
            else: fig = gen_graf.generate_vector_graph([v1, res_v], ["V", "R"], save=False)
            resultado = f"Vector R: {res_v}, Magnitud: {res_v.magnitud:.2f}, Ángulo: {res_v.angulo:.2f}°"

        elif tipo == "oblicuo":
            v0, ang = random.randint(15, 60), random.choice([15, 30, 45, 60, 75])
            calc = ProjectileCalculator(v0=v0, angulo_deg=ang); res = calc.calcular()
            enunciado = random.choice(self.pool["tiro_oblicuo"]).format(v0=f"{v0:.1f}", ang=f"{ang:.1f}", h0="0.0", range=f"{res['alcance_max']:.2f}", height=f"{res['altura_max']:.2f}", time=f"{res['tiempo_vuelo']:.2f}")
            x_pts, y_pts = calc.obtener_trayectoria()
            fig = gen_graf.generate_projectile_graph(x_pts, y_pts, filename="web.png", save=False)
            resultado = f"Alcance: {res['alcance_max']:.2f} m, Altura Máx: {res['altura_max']:.2f} m, Tiempo: {res['tiempo_vuelo']:.2f} s"

        elif tipo == "newton":
            m, a, mu = random.randint(2, 50), random.randint(1, 10), random.choice([0.0, 0.1, 0.2])
            calc = ForceCalculator(masa=m, aceleracion=a, mu=mu); res = calc.calcular_newton()
            enunciado = random.choice(self.pool["leyes_newton"]).format(m=m, f=f"{res['fuerza']:.1f}", a=a, mu=mu)
            f_v = [Vector2D(res['fuerza'], 0), Vector2D(0, -m*9.8), Vector2D(0, m*9.8)]
            labels = ["F aplicada", "Peso", "Normal"]
            if mu > 0: f_v.append(Vector2D(-res['rozamiento'], 0)); labels.append("Rozamiento")
            fig = gen_graf.generate_dcl_graph(f_v, labels, save=False)
            resultado = f"Aceleración: {res['aceleracion']:.2f} m/s², Fuerza: {res['fuerza']:.2f} N"

        elif tipo == "plano":
            m, ang, mu = random.randint(2, 20), random.choice([15, 30, 45]), random.choice([0.0, 0.1, 0.2])
            calc = ForceCalculator(masa=m, angulo=ang, mu=mu); res = calc.calcular_plano_inclinado()
            enunciado = self.pool["plano_inclinado"][1].format(m=m, ang=ang, mu=mu)
            f_v = [Vector2D(res['peso_x'], -res['peso_y']), Vector2D(0, res['normal']), Vector2D(-res['rozamiento'], 0)]
            fig = gen_graf.generate_inclined_plane_graph(ang, f_v, ["Peso", "Normal", "Rozamiento"], save=False)
            resultado = f"Aceleración: {res['aceleracion']:.2f} m/s², Px: {res['peso_x']:.1f} N, Py: {res['peso_y']:.1f} N"

        # Ensamblar bloque LaTeX
        bloque = self.templates["ejercicio"].replace("{{ NUMERO }}", str(n)).replace("{{ ENUNCIADO }}", enunciado).replace("{{ RUTA_GRAFICO }}", f"grafico_{n}.png").replace("{{ RESULTADO_REFERENCIA }}", resultado)
        res_tex = self.templates["respuesta"].replace("{{ RESULTADO }}", resultado)
        
        return bloque, res_tex, fig

orchestrator = WebOrchestrator()

def main_web(event):
    status = document.getElementById("status")
    status.innerHTML = "Generando ejercicios aleatorios... por favor espere."
    
    counts = {
        "mru": int(document.getElementById("mru").value),
        "mrua": int(document.getElementById("mrua").value),
        "vectores": int(document.getElementById("vectores").value),
        "oblicuo": int(document.getElementById("oblicuo").value),
        "newton": int(document.getElementById("newton").value),
        "plano": int(document.getElementById("plano").value),
    }
    
    try:
        orchestrator.generar_y_mostrar(counts)
        status.innerHTML = "¡Examen generado con éxito! Revise el código abajo y los gráficos."
    except Exception as e:
        status.innerHTML = f"❌ Error: {str(e)}"

def download_tex(event):
    tex_content = document.getElementById("output-tex").value
    blob = window.Blob.new([tex_content], { "type": "text/plain" })
    url = window.URL.createObjectURL(blob)
    link = document.createElement("a")
    link.href = url
    link.download = "examen_fisica.tex"
    link.click()
    window.URL.revokeObjectURL(url)
