import os
import json
import random
from graph_tool.physic_calculator import PhysicCalculator
from graph_tool.class_graph import GraphicGenerator

class GeneradorExamen:
    VERSION = "0.0.1"

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

    def generar_ejercicio(self, numero, tipo="mru"):
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

    def crear_examen(self, cant_mru=2, cant_mrua=2, filename="examen_generado.tex"):
        print(f"Generando examen con {cant_mru} MRU y {cant_mrua} MRUA...")
        
        ejercicios_tex = []
        respuestas_tex = []
        
        # Generar todos los bloques
        for i in range(1, cant_mru + 1):
            ej, res = self.generar_ejercicio(i, tipo="mru")
            ejercicios_tex.append(ej)
            respuestas_tex.append(res)
            
        for i in range(cant_mru + 1, cant_mru + cant_mrua + 1):
            ej, res = self.generar_ejercicio(i, tipo="mrua")
            ejercicios_tex.append(ej)
            respuestas_tex.append(res)

        # Montar en la base
        base = self._leer_archivo(self.template_base)
        base = base.replace("{{ CONTENIDO_EJERCICIOS }}", "\n".join(ejercicios_tex))
        base = base.replace("{{ CLAVE_RESPUESTAS }}", "\n".join(respuestas_tex))

        # Guardar resultado final
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(base)
        
        print(f"Examen generado exitosamente en: {output_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generador automático de exámenes de Física (Cinemática)")
    parser.add_argument("--mru", type=int, default=2, help="Número de ejercicios de MRU (por defecto: 2)")
    parser.add_argument("--mrua", type=int, default=2, help="Número de ejercicios de MRUA (por defecto: 2)")
    parser.add_argument("--out", type=str, default="examen_generado.tex", help="Nombre del archivo .tex de salida")
    parser.add_argument("--version", action="version", version=f"%(prog)s {GeneradorExamen.VERSION}")
    
    args = parser.parse_args()

    try:
        generador = GeneradorExamen()
        generador.crear_examen(cant_mru=args.mru, cant_mrua=args.mrua, filename=args.out)
    except Exception as e:
        print(f"Error al generar el examen: {e}")
