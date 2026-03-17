import json
import os
import argparse

class GestorEjercicios:
    def __init__(self, ruta_json="data/ejercicios.json"):
        self.ruta_json = ruta_json
        self.data = self._cargar_data()

    def _cargar_data(self):
        if not os.path.exists(self.ruta_json):
            return {
                "mru": [], "mrua": [], "vectores": [], "tiro_oblicuo": [],
                "leyes_newton": [], "estatica": [], "elasticidad": [],
                "plano_inclinado": [], "energia": []
            }
        with open(self.ruta_json, "r", encoding="utf-8") as f:
            return json.load(f)

    def _guardar_data(self):
        with open(self.ruta_json, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        print(f"✅ Cambios guardados en {self.ruta_json}")

    def listar(self, tipo=None):
        tipos = [tipo] if tipo else ["mru", "mrua", "vectores", "tiro_oblicuo", "leyes_newton", "estatica", "elasticidad", "plano_inclinado", "energia"]
        for t in tipos:
            if t in self.data:
                print(f"\n--- Ejercicios de {t.upper()} ---")
                for i, ejercicio in enumerate(self.data.get(t, [])):
                    print(f"[{i}] {ejercicio}")
        print("")

    def agregar(self, tipo, texto):
        if tipo not in self.data:
            print(f"❌ Error: El tipo debe ser uno de {list(self.data.keys())}.")
            return
        self.data[tipo].append(texto)
        self._guardar_data()
        print(f"🚀 Ejercicio agregado a {tipo.upper()}.")

    def borrar(self, tipo, indice):
        try:
            if tipo not in self.data:
                print(f"❌ Error: El tipo debe ser uno de {list(self.data.keys())}.")
                return
            eliminado = self.data[tipo].pop(indice)
            self._guardar_data()
            print(f"🗑️  Ejercicio eliminado: {eliminado}")
        except IndexError:
            print(f"❌ Error: El índice {indice} no existe para el tipo {tipo}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gestor de Banco de Ejercicios JSON v0.0.3")
    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponibles")

    # Comando Listar
    subparsers.add_parser("listar", help="Lista todos los ejercicios")

    # Comando Agregar
    parser_add = subparsers.add_parser("agregar", help="Agrega un nuevo ejercicio")
    parser_add.add_argument("--tipo", choices=["mru", "mrua", "vectores", "tiro_oblicuo", "leyes_newton", "estatica", "elasticidad", "plano_inclinado", "energia"], required=True, help="Tipo de ejercicio")
    parser_add.add_argument("--texto", required=True, help="Texto del enunciado")

    # Comando Borrar
    parser_del = subparsers.add_parser("borrar", help="Elimina un ejercicio por su índice")
    parser_del.add_argument("--tipo", choices=["mru", "mrua", "vectores", "tiro_oblicuo", "leyes_newton", "estatica", "elasticidad", "plano_inclinado", "energia"], required=True, help="Tipo de ejercicio")
    parser_del.add_argument("--indice", type=int, required=True, help="Índice del ejercicio a borrar")

    args = parser.parse_args()
    gestor = GestorEjercicios()

    if args.comando == "listar":
        gestor.listar()
    elif args.comando == "agregar":
        gestor.agregar(args.tipo, args.texto)
    elif args.comando == "borrar":
        gestor.borrar(args.tipo, args.indice)
    else:
        parser.print_help()
