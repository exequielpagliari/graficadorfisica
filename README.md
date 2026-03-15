# Asistente IA - Generador de Ejercicios de Física (Cinemática) v0.0.3

Este proyecto es una herramienta automatizada diseñada para docentes de física. Permite generar guías de ejercicios de cinemática (MRU, MRUA, Vectores 2D y Tiro Oblicuo) en formato LaTeX, incluyendo enunciados aleatorios, gráficos dinámicos y una clave de respuestas.

## 🚀 Características

- **Motores Físicos Especializados**: 
    - MRU/MRUA: Resolución automática de variables lineales.
    - Vectores 2D: Suma, resta y operaciones con escalares.
    - Tiro Oblicuo: Cálculo de alcance, altura máxima y tiempo de vuelo.
- **Gráficos Dinámicos**: 
    - Posición vs Tiempo (MRU/MRUA).
    - Flechas vectoriales en plano cartesiano.
    - Trayectorias parabólicas (Y vs X) para proyectiles.
- **Gestión de Contenidos**: Herramienta CLI para administrar el banco de datos JSON.
- **Salida Profesional**: Documentos LaTeX listos para imprimir o convertir.

## 🛠️ Instalación

1. Asegúrate de tener Python 3.9 o superior.
2. Instala las dependencias:
   ```bash
   pip install numpy matplotlib
   ```

## 📖 Uso

### Generación de Exámenes
Generar un examen mixto (1 de cada tipo por defecto):
```bash
python generador_examen.py
```

Personalizar la cantidad de ejercicios:
```bash
python generador_examen.py --mru 2 --mrua 2 --vectores 2 --oblicuo 2 --out guia_completa.tex
```

### Gestión del Banco de Ejercicios
Utiliza `gestor_ejercicios.py` para administrar los enunciados:
- `python gestor_ejercicios.py listar`
- `python gestor_ejercicios.py agregar --tipo tiro_oblicuo --texto "Un proyectil..."`
- `python gestor_ejercicios.py borrar --tipo vectores --indice 0`

## 📂 Estructura del Proyecto

- `generador_examen.py`: Script principal (v0.0.3).
- `graph_tool/`: Motores de cálculo y graficación.
- `data/ejercicios.json`: Banco de datos.
- `templates/`: Plantillas LaTeX.
- `tests/`: Suite de pruebas unitarias.

## 🧪 Pruebas
Ejecuta todas las pruebas para validar la precisión física:
```bash
python -m unittest discover tests
```
