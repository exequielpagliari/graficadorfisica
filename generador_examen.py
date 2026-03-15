import os
import json
import random
from graph_tool.physic_calculator import PhysicCalculator
from graph_tool.class_graph import GraphicGenerator
from graph_tool.vector_calculator import Vector2D, VectorCalculator
from graph_tool.projectile_calculator import ProjectileCalculator

class GeneradorExamen:
    VERSION = "0.0.3"

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

        # 4. Crear bloque LaTeX del ejercicio
        bloque_ej = self._leer_archivo(self.template_ejercicio)
        bloque_ej = bloque_ej.replace("{{ NUMERO }}", str(numero))
        bloque_ej = bloque_ej.replace("{{ ENUNCIADO }}", enunciado)
        bloque_ej = bloque_ej.replace("{{ RUTA_GRAFICO }}", graph_filename)

        # 5. Crear respuesta
        res_tex = self._leer_archivo(self.template_respuesta)
        res_num = f"Posición Final: {calc.posicion_final:.2f} m, Velocidad Final: {calc.velocidad_final:.2f} m/s"
        res_tex = res_tex.replace("{{ RESULTADO }}", res_num)

        return bloque_ej, res_tex

    def generar_ejercicio_vector(self, numero):
        # 1. Elegir operación aleatoria
        op = random.choice(["suma", "resta", "multiplicacion", "division"])
        
        v1 = Vector2D(random.randint(-10, 10), random.randint(-10, 10))
        v2 = Vector2D(random.randint(-10, 10), random.randint(-10, 10))
        escalar = random.randint(2, 5)
        
        calc = VectorCalculator(v1=v1, v2=v2, escalar=escalar, operacion=op)
        res_vector = calc.calcular()
        
        # 2. Elegir enunciado
        enunciados = self.ejercicios_pool["vectores"]
        if op == "suma": enunciado_raw = enunciados[0]
        elif op == "resta": enunciado_raw = enunciados[1]
        elif op == "multiplicacion": enunciado_raw = enunciados[2]
        else: enunciado_raw = enunciados[3]
        
        enunciado = enunciado_raw.format(
            v1=str(v1),
            v2=str(v2),
            s=str(escalar),
            res=str(res_vector)
        )
        
        # 3. Gráfico Vectorial
        graph_filename = f"grafico_{numero}.png"
        graph_path = os.path.join(self.output_dir, graph_filename)
        gen_graf = GraphicGenerator()
        
        if op in ["suma", "resta"]:
            gen_graf.generate_vector_graph([v1, v2, res_vector], ["A", "B", "R"], filename=graph_path)
        else:
            gen_graf.generate_vector_graph([v1, res_vector], ["V", "R"], filename=graph_path)
            
        # 4. Bloque LaTeX
        bloque_ej = self._leer_archivo(self.template_ejercicio)
        bloque_ej = bloque_ej.replace("{{ NUMERO }}", str(numero))
        bloque_ej = bloque_ej.replace("{{ ENUNCIADO }}", enunciado)
        bloque_ej = bloque_ej.replace("{{ RUTA_GRAFICO }}", graph_filename)
        
        # 5. Respuesta
        res_tex = self._leer_archivo(self.template_respuesta)
        res_num = f"Vector R: {res_vector}, Magnitud: {res_vector.magnitud:.2f}, Ángulo: {res_vector.angulo:.2f}°"
        res_tex = res_tex.replace("{{ RESULTADO }}", res_num)
        
        return bloque_ej, res_tex

    def generar_ejercicio_oblicuo(self, numero):
        # 1. Generar datos aleatorios
        v0 = random.randint(15, 60)
        ang = random.choice([15, 30, 45, 60, 75])
        
        calc = ProjectileCalculator(v0=v0, angulo_deg=ang)
        res = calc.calcular()
        
        # 2. Elegir enunciado
        enunciado_raw = random.choice(self.ejercicios_pool["tiro_oblicuo"])
        enunciado = enunciado_raw.format(
            v0=f"{v0:.1f}",
            ang=f"{ang:.1f}",
            h0="0.0",
            range=f"{res['alcance_max']:.2f}",
            height=f"{res['altura_max']:.2f}",
            time=f"{res['tiempo_vuelo']:.2f}"
        )
        
        # 3. Gráfico de trayectoria
        graph_filename = f"grafico_{numero}.png"
        graph_path = os.path.join(self.output_dir, graph_filename)
        x_pts, y_pts = calc.obtener_trayectoria()
        gen_graf = GraphicGenerator()
        gen_graf.generate_projectile_graph(x_pts, y_pts, filename=graph_path)
        
        # 4. Bloque LaTeX
        bloque_ej = self._leer_archivo(self.template_ejercicio)
        bloque_ej = bloque_ej.replace("{{ NUMERO }}", str(numero))
        bloque_ej = bloque_ej.replace("{{ ENUNCIADO }}", enunciado)
        bloque_ej = bloque_ej.replace("{{ RUTA_GRAFICO }}", graph_filename)
        
        # 5. Respuesta
        res_tex = self._leer_archivo(self.template_respuesta)
        res_num = f"Alcance: {res['alcance_max']:.2f} m, Altura Máx: {res['altura_max']:.2f} m, Tiempo: {res['tiempo_vuelo']:.2f} s"
        res_tex = res_tex.replace("{{ RESULTADO }}", res_num)
        
        return bloque_ej, res_tex

    def crear_examen(self, cant_mru=0, cant_mrua=0, cant_vectores=0, cant_oblicuo=0, filename="examen_generado.tex"):
        print(f"Generando examen: MRU={cant_mru}, MRUA={cant_mrua}, Vectores={cant_vectores}, Oblicuo={cant_oblicuo}")
        
        ejercicios_tex = []
        respuestas_tex = []
        n = 1
        
        # Generar MRU
        for _ in range(cant_mru):
            ej, res = self.generar_ejercicio_fisica(n, tipo="mru")
            ejercicios_tex.append(ej); respuestas_tex.append(res); n += 1
            
        # Generar MRUA
        for _ in range(cant_mrua):
            ej, res = self.generar_ejercicio_fisica(n, tipo="mrua")
            ejercicios_tex.append(ej); respuestas_tex.append(res); n += 1
            
        # Generar Vectores
        for _ in range(cant_vectores):
            ej, res = self.generar_ejercicio_vector(n)
            ejercicios_tex.append(ej); respuestas_tex.append(res); n += 1
            
        # Generar Tiro Oblicuo
        for _ in range(cant_oblicuo):
            ej, res = self.generar_ejercicio_oblicuo(n)
            ejercicios_tex.append(ej); respuestas_tex.append(res); n += 1

        # Montar en la base
        base = self._leer_archivo(self.template_base)
        base = base.replace("{{ CONTENIDO_EJERCICIOS }}", "\n".join(ejercicios_tex))
        base = base.replace("{{ CLAVE_RESPUESTAS }}", "\n".join(respuestas_tex))

        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(base)
        
        print(f"Examen v{self.VERSION} generado exitosamente en: {output_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generador automático de exámenes de Física v0.0.3")
    parser.add_argument("--mru", type=int, default=0, help="Número de ejercicios de MRU")
    parser.add_argument("--mrua", type=int, default=0, help="Número de ejercicios de MRUA")
    parser.add_argument("--vectores", type=int, default=0, help="Número de ejercicios de Vectores")
    parser.add_argument("--oblicuo", type=int, default=0, help="Número de ejercicios de Tiro Oblicuo")
    parser.add_argument("--out", type=str, default="examen_generado.tex", help="Nombre del archivo de salida")
    parser.add_argument("--version", action="version", version=f"%(prog)s {GeneradorExamen.VERSION}")
    
    args = parser.parse_args()

    # Si no se especifica nada, generar 1 de cada uno por defecto
    if args.mru == 0 and args.mrua == 0 and args.vectores == 0 and args.oblicuo == 0:
        args.mru, args.mrua, args.vectores, args.oblicuo = 1, 1, 1, 1

    try:
        generador = GeneradorExamen()
        generador.crear_examen(cant_mru=args.mru, cant_mrua=args.mrua, 
                               cant_vectores=args.vectores, cant_oblicuo=args.oblicuo, 
                               filename=args.out)
    except Exception as e:
        print(f"Error al generar el examen: {e}")
        import traceback
        traceback.print_exc()
