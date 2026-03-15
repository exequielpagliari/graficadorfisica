import os
import json
import random
from graph_tool.physic_calculator import PhysicCalculator
from graph_tool.class_graph import GraphicGenerator
from graph_tool.vector_calculator import Vector2D, VectorCalculator
from graph_tool.projectile_calculator import ProjectileCalculator
from graph_tool.force_calculator import ForceCalculator

class GeneradorExamen:
    VERSION = "0.1.0"

    def __init__(self):
        # Rutas de archivos y carpetas
        self.template_base = "templates/examen_base.tex"
        self.template_ejercicio = "templates/ejercicio_fragmento.tex"
        self.template_respuesta = "templates/respuesta_fragmento.tex"
        self.data_ejercicios = "data/ejercicios.json"
        self.output_dir = "output"
        
        # Cargar enunciados desde JSON
        self.ejercicios_pool = self._cargar_ejercicios()

    def _cargar_ejercicios(self):
        """Carga el banco de ejercicios desde el archivo JSON."""
        if not os.path.exists(self.data_ejercicios):
            raise FileNotFoundError(f"No se encontró el archivo: {self.data_ejercicios}")
        with open(self.data_ejercicios, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _leer_archivo(self, ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()

    def generar_ejercicio_fisica(self, numero, tipo="mru"):
        # 1. Generar datos aleatorios coherentes
        if tipo == "mru":
            v = random.randint(5, 30)
            t = random.randint(5, 60)
            pi = random.choice([0, 10, 50, 100])
            calc = PhysicCalculator(posicion_inicial=pi, velocidad=v, tiempo=t, aceleracion=0)
            calc.calcular()
            enunciado_raw = random.choice(self.ejercicios_pool["mru"])
        else:
            vi = random.randint(0, 25)
            a = random.randint(1, 10)
            t = random.randint(2, 15)
            calc = PhysicCalculator(posicion_inicial=0.0, velocidad_inicial=vi, aceleracion=a, tiempo=t)
            calc.calcular()
            enunciado_raw = random.choice(self.ejercicios_pool["mrua"])

        # 2. Reemplazar valores en el enunciado dinámicamente
        enunciado = enunciado_raw.format(
            v=f"{calc.velocidad:.1f}" if calc.velocidad is not None else "0",
            vi=f"{calc.velocidad_inicial:.1f}" if calc.velocidad_inicial is not None else "0",
            vf=f"{calc.velocidad_final:.1f}" if calc.velocidad_final is not None else "0",
            a=f"{calc.aceleracion:.1f}" if calc.aceleracion is not None else "0",
            t=f"{calc.tiempo:.1f}" if calc.tiempo is not None else "0",
            pi=f"{calc.posicion_inicial:.1f}" if calc.posicion_inicial is not None else "0",
            pf=f"{calc.posicion_final:.1f}" if calc.posicion_final is not None else "0"
        )

        # 3. Generar Gráfico
        graph_filename = f"grafico_{numero}.png"
        graph_path = os.path.join(self.output_dir, graph_filename)
        gen_graf = GraphicGenerator(
            posicion_inicial=calc.posicion_inicial or 0,
            velocidad_inicial=calc.velocidad_inicial or 0,
            aceleracion=calc.aceleracion or 0,
            tiempo=calc.tiempo or 10,
            velocidad_mru=calc.velocidad
        )
        gen_graf.generate(graph_path)

        resultado_sugerido = f"Posición Final: {calc.posicion_final:.2f} m, Velocidad Final: {calc.velocidad_final:.2f} m/s"
        return self._ensamblar_bloque_latex(numero, enunciado, graph_filename, resultado_sugerido)

    def generar_ejercicio_vector(self, numero):
        op = random.choice(["suma", "resta", "multiplicacion", "division"])
        v1 = Vector2D(random.randint(-10, 10), random.randint(-10, 10))
        v2 = Vector2D(random.randint(-10, 10), random.randint(-10, 10))
        escalar = random.randint(2, 5)
        calc = VectorCalculator(v1=v1, v2=v2, escalar=escalar, operacion=op)
        res_vector = calc.calcular()
        
        enunciado = random.choice(self.ejercicios_pool["vectores"]).format(v1=str(v1), v2=str(v2), s=str(escalar), res=str(res_vector))
        graph_filename = f"grafico_{numero}.png"
        graph_path = os.path.join(self.output_dir, graph_filename)
        gen_graf = GraphicGenerator()
        if op in ["suma", "resta"]:
            gen_graf.generate_vector_graph([v1, v2, res_vector], ["A", "B", "R"], filename=graph_path)
        else:
            gen_graf.generate_vector_graph([v1, res_vector], ["V", "R"], filename=graph_path)
            
        resultado_sugerido = f"Vector R: {res_vector}, Magnitud: {res_vector.magnitud:.2f}, Ángulo: {res_vector.angulo:.2f}°"
        return self._ensamblar_bloque_latex(numero, enunciado, graph_filename, resultado_sugerido)

    def generar_ejercicio_oblicuo(self, numero):
        v0 = random.randint(15, 60); ang = random.choice([15, 30, 45, 60, 75])
        calc = ProjectileCalculator(v0=v0, angulo_deg=ang)
        res = calc.calcular()
        enunciado = random.choice(self.ejercicios_pool["tiro_oblicuo"]).format(v0=f"{v0:.1f}", ang=f"{ang:.1f}", h0="0.0", range=f"{res['alcance_max']:.2f}", height=f"{res['altura_max']:.2f}", time=f"{res['tiempo_vuelo']:.2f}")
        graph_filename = f"grafico_{numero}.png"; graph_path = os.path.join(self.output_dir, graph_filename)
        x_pts, y_pts = calc.obtener_trayectoria()
        GraphicGenerator().generate_projectile_graph(x_pts, y_pts, filename=graph_path)
        resultado_sugerido = f"Alcance: {res['alcance_max']:.2f} m, Altura Máx: {res['altura_max']:.2f} m, Tiempo: {res['tiempo_vuelo']:.2f} s"
        return self._ensamblar_bloque_latex(numero, enunciado, graph_filename, resultado_sugerido)

    def generar_ejercicio_dinamica(self, numero, tipo="newton"):
        m = random.randint(2, 50); a = random.randint(1, 10); mu = random.choice([0.0, 0.1, 0.2, 0.3])
        graph_filename = f"grafico_{numero}.png"; graph_path = os.path.join(self.output_dir, graph_filename)
        
        if tipo == "newton":
            calc = ForceCalculator(masa=m, aceleracion=a, mu=mu)
            res = calc.calcular_newton()
            enunciado = random.choice(self.ejercicios_pool["leyes_newton"]).format(m=m, f=f"{res['fuerza']:.1f}", a=a, mu=mu)
            f_vector = [Vector2D(res['fuerza'], 0), Vector2D(0, -m*9.8), Vector2D(0, m*9.8)]
            labels = ["F aplicada", "Peso", "Normal"]
            if mu > 0: f_vector.append(Vector2D(-res['rozamiento'], 0)); labels.append("Rozamiento")
            GraphicGenerator().generate_dcl_graph(f_vector, labels, filename=graph_path)
            resultado_sugerido = f"Aceleración: {res['aceleracion']:.2f} m/s², Fuerza: {res['fuerza']:.2f} N"
        
        elif tipo == "hooke":
            k = random.randint(100, 1000); x = random.uniform(0.05, 0.5)
            calc = ForceCalculator(k=k, x=x); res = calc.calcular_hooke()
            enunciado = self.ejercicios_pool["elasticidad"][0].format(k=k, x=f"{x:.2f}")
            GraphicGenerator().generate_dcl_graph([Vector2D(0, -res['fuerza']), Vector2D(0, res['fuerza'])], ["Peso", "F Elástica"], filename=graph_path)
            resultado_sugerido = f"Fuerza Elástica: {res['fuerza']:.2f} N"
        
        return self._ensamblar_bloque_latex(numero, enunciado, graph_filename, resultado_sugerido)

    def generar_ejercicio_plano(self, numero):
        m = random.randint(2, 20); ang = random.choice([15, 30, 45]); mu = random.choice([0.0, 0.1, 0.2])
        calc = ForceCalculator(masa=m, angulo=ang, mu=mu)
        res = calc.calcular_plano_inclinado(sentido="descenso")
        
        enunciado = self.ejercicios_pool["plano_inclinado"][1].format(m=m, ang=ang, mu=mu)
        graph_filename = f"grafico_{numero}.png"; graph_path = os.path.join(self.output_dir, graph_filename)
        
        # Fuerzas en el plano (Ejes rotados para el DCL)
        f_vector = [Vector2D(res['peso_x'], -res['peso_y']), Vector2D(0, res['normal']), Vector2D(-res['rozamiento'], 0)]
        labels = ["Peso", "Normal", "Rozamiento"]
        GraphicGenerator().generate_inclined_plane_graph(ang, f_vector, labels, filename=graph_path)
        
        resultado_sugerido = f"Aceleración: {res['aceleracion']:.2f} m/s², Px: {res['peso_x']:.1f} N, Py: {res['peso_y']:.1f} N"
        return self._ensamblar_bloque_latex(numero, enunciado, graph_filename, resultado_sugerido)

    def _ensamblar_bloque_latex(self, numero, enunciado, graph_filename, resultado_sugerido):
        bloque_ej = self._leer_archivo(self.template_ejercicio)
        bloque_ej = bloque_ej.replace("{{ NUMERO }}", str(numero)).replace("{{ ENUNCIADO }}", enunciado).replace("{{ RUTA_GRAFICO }}", graph_filename).replace("{{ RESULTADO_REFERENCIA }}", resultado_sugerido)
        res_tex = self._leer_archivo(self.template_respuesta).replace("{{ RESULTADO }}", resultado_sugerido)
        return bloque_ej, res_tex

    def crear_examen(self, mru=0, mrua=0, vectores=0, oblicuo=0, newton=0, hooke=0, plano=0, filename="examen_generado.tex"):
        print(f"Generando examen v{self.VERSION}...")
        ejercicios_tex = []; respuestas_tex = []; n = 1
        
        for cant, tipo in [(mru, "mru"), (mrua, "mrua")]:
            for _ in range(cant):
                ej, res = self.generar_ejercicio_fisica(n, tipo=tipo)
                ejercicios_tex.append(ej); respuestas_tex.append(res); n += 1
        
        for _ in range(vectores):
            ej, res = self.generar_ejercicio_vector(n)
            ejercicios_tex.append(ej); respuestas_tex.append(res); n += 1
            
        for _ in range(oblicuo):
            ej, res = self.generar_ejercicio_oblicuo(n)
            ejercicios_tex.append(ej); respuestas_tex.append(res); n += 1
            
        for _ in range(newton):
            ej, res = self.generar_ejercicio_dinamica(n, tipo="newton")
            ejercicios_tex.append(ej); respuestas_tex.append(res); n += 1

        for _ in range(hooke):
            ej, res = self.generar_ejercicio_dinamica(n, tipo="hooke")
            ejercicios_tex.append(ej); respuestas_tex.append(res); n += 1
            
        for _ in range(plano):
            ej, res = self.generar_ejercicio_plano(n)
            ejercicios_tex.append(ej); respuestas_tex.append(res); n += 1

        base = self._leer_archivo(self.template_base).replace("{{ CONTENIDO_EJERCICIOS }}", "\n".join(ejercicios_tex)).replace("{{ CLAVE_RESPUESTAS }}", "\n".join(respuestas_tex))
        with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f: f.write(base)
        print(f"Examen generado en: {filename}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generador automático de exámenes de Física v0.0.6")
    parser.add_argument("--mru", type=int, default=0); parser.add_argument("--mrua", type=int, default=0)
    parser.add_argument("--vectores", type=int, default=0); parser.add_argument("--oblicuo", type=int, default=0)
    parser.add_argument("--newton", type=int, default=0); parser.add_argument("--hooke", type=int, default=0)
    parser.add_argument("--plano", type=int, default=0)
    parser.add_argument("--out", type=str, default="examen_generado.tex")
    args = parser.parse_args()
    if all(v == 0 for v in [args.mru, args.mrua, args.vectores, args.oblicuo, args.newton, args.hooke, args.plano]):
        args.mru, args.mrua, args.newton, args.hooke, args.plano = 1, 1, 1, 1, 1
    GeneradorExamen().crear_examen(mru=args.mru, mrua=args.mrua, vectores=args.vectores, oblicuo=args.oblicuo, newton=args.newton, hooke=args.hooke, plano=args.plano, filename=args.out)
