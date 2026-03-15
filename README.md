# Asistente IA - Física Interactiva v0.1.0 🚀

Herramienta educativa integral para docentes de física. Genera guías de ejercicios personalizadas con cálculos precisos y gráficos dinámicos para el nivel secundario (6to año - PBA Argentina).

## 🌐 Acceso Web (GitHub Pages)
¡Ahora puedes usar la aplicación directamente desde tu navegador!
**[Link a la Web App](https://exequielpagliari.github.io/graficadorfisica/)** *(Reemplaza con tu URL real)*

## 🚀 Características
- **Multientorno**: Úsalo desde la terminal (CLI) o como aplicación web (PyScript).
- **Cobertura Curricular Completa**:
    - **Cinemática**: MRU, MRUA, Tiro Oblicuo.
    - **Vectores**: Operaciones en 2D (Suma, Resta, Escalares).
    - **Dinámica**: Leyes de Newton, Rozamiento, Ley de Hooke.
    - **Sistemas**: Planos Inclinados con Diagramas de Cuerpo Libre (DCL).
- **Gráficos Profesionales**: Generación automática de trayectorias, vectores y esquemas de fuerzas.
- **Resultados de Referencia**: Incluye soluciones sugeridas para autoevaluación del alumno.

## 📖 Uso

### Modo Web
1. Abre el sitio en GitHub Pages.
2. Elige la cantidad de ejercicios por tema.
3. Haz clic en "Generar" para previsualizar los gráficos.
4. Descarga el archivo `.tex` listo para compilar.

### Modo CLI (Terminal)
Generar un examen personalizado:
```bash
python generador_examen.py --mru 2 --newton 2 --plano 1 --out guia_final.tex
```

## 📂 Estructura del Proyecto
- `index.html` / `web_app.py`: Interfaz web interactiva.
- `generador_examen.py`: Motor de orquestación CLI.
- `graph_tool/`: Motores de cálculo físico y generadores de gráficos.
- `data/ejercicios.json`: Banco de enunciados administrable.
- `templates/`: Plantillas LaTeX profesionales.

## 🧪 Pruebas
Valida la precisión del motor físico:
```bash
python -m unittest discover tests
```

## 📄 Licencia
Este proyecto está bajo la Licencia MIT.
