# Asistente IA - Generador de Ejercicios de Física (Cinemática) v0.0.1

Este proyecto es una herramienta automatizada diseñada para docentes de física. Permite generar guías de ejercicios de cinemática (MRU y MRUA) en formato LaTeX, incluyendo enunciados aleatorios, gráficos dinámicos y una clave de respuestas para el docente.

## 🚀 Características

- **Motor Físico Robusto**: Resolución automática de variables cinemáticas (MRU/MRUA).
- **Gráficos Dinámicos**: Generación de gráficas Posición vs. Tiempo usando Matplotlib.
- **Banco de Ejercicios**: Pool de enunciados personalizables en formato JSON.
- **Gestión de Contenidos**: Herramienta CLI para administrar (agregar/borrar/listar) ejercicios.
- **Salida Profesional**: Documentos maquetados en LaTeX listos para imprimir o convertir a PDF/Word.
- **CLI Versátil**: Control total sobre la cantidad y tipo de ejercicios desde la terminal.

## 🛠️ Instalación

1. Asegúrate de tener Python 3.9 o superior instalado.
2. Instala las dependencias necesarias:
   ```bash
   pip install numpy matplotlib
   ```
3. (Opcional) Para generar PDFs directamente, asegúrate de tener instalado un compilador de LaTeX (como MiKTeX o TeX Live) o Pandoc.

## 📖 Uso

### Generación de Exámenes
Para generar un examen por defecto (2 ejercicios de cada tipo):
```bash
python generador_examen.py
```

Para personalizar la cantidad de ejercicios y el nombre del archivo:
```bash
python generador_examen.py --mru 5 --mrua 3 --out guia_cinematica.tex
```

### Gestión del Banco de Ejercicios
Utiliza `gestor_ejercicios.py` para administrar los enunciados:

- **Listar ejercicios actuales**:
  ```bash
  python gestor_ejercicios.py listar
  ```
- **Agregar un nuevo ejercicio**:
  ```bash
  python gestor_ejercicios.py agregar --tipo mrua --texto "Un móvil acelera a {a} m/s²..."
  ```
- **Borrar un ejercicio por su índice**:
  ```bash
  python gestor_ejercicios.py borrar --tipo mru --indice 2
  ```

## 📂 Estructura del Proyecto

- `generador_examen.py`: Script principal (orquestador).
- `gestor_ejercicios.py`: Herramienta de administración del banco de datos.
- `graph_tool/`:
    - `physic_calculator.py`: Motor de cálculo cinemático.
    - `class_graph.py`: Generador de gráficas con Matplotlib.
- `data/`: Contiene `ejercicios.json` con los enunciados base.
- `templates/`: Plantillas de LaTeX para el documento final.
- `tests/`: Suite de pruebas unitarias para validación física.
- `output/`: Carpeta donde se generan los exámenes y gráficos.

## 🧪 Pruebas

El proyecto incluye pruebas automatizadas para asegurar la precisión de los cálculos físicos. Puedes ejecutarlas localmente con:
```bash
python -m unittest discover tests
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
