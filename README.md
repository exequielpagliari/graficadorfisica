# Asistente IA - Física Interactiva v0.2.0 🚀

**Herramienta educativa integral para docentes de física.** Este proyecto automatiza la creación de guías y exámenes personalizados para el nivel secundario (6to año - PBA Argentina), vinculando motores de cálculo físico con generación de gráficos dinámicos y plantillas profesionales en LaTeX.

## 🐛 Cambios en v0.2.0

- **Manejo de errores unificado**: Nueva excepción `CalculationError` para todos los calculators
- **Error handling consistente**: Todos los calculators ahora lanzan excepciones en lugar de retornar `None` o crashear
- **Logging estructurado**: Sistema de logging integrado para mejor debugging

## 🌐 Acceso Web (PyScript)
¡Usa la aplicación directamente desde tu navegador sin instalar nada!
**[Link a la Web App](https://exequielpagliari.github.io/graficadorfisica/)**

## 🚀 Características Principales
- **Generación Multimodelo**: Crea exámenes únicos con datos aleatorios pero físicamente coherentes.
- **Cobertura Curricular (v0.2.0)**:
    - **Cinemática**: MRU, MRUA y Tiro Oblicuo.
    - **Vectores**: Operaciones 2D, magnitudes y ángulos.
    - **Dinámica**: Leyes de Newton, Rozamiento, Ley de Hooke y Planos Inclinados (DCL).
    - **Energía y Trabajo**: Energía Cinética, Potencial (Gravitatoria/Elástica) y Trabajo Mecánico.
- **Visualización Dinámica**: Generación automática de gráficos (Trayectorias, Vectores, Diagramas de Cuerpo Libre).
- **Exportación Profesional**: Salida en código LaTeX listo para compilar en Overleaf o TeXLive.
- **Vista Previa en Tiempo Real**: Visualiza enunciados y gráficos antes de descargar el archivo final.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.11+
- **Cálculo Científico:** NumPy
- **Visualización:** Matplotlib
- **Frontend Web:** PyScript (Python en el navegador)
- **Documentación:** LaTeX
- **Persistencia de Datos:** JSON (Banco de ejercicios administrable)

## 📖 Guía de Uso

### Interfaz Web
1. Ingresa las cantidades deseadas para cada tema en el panel de configuración.
2. Haz clic en **"Generar Examen y Gráficos"**.
3. Revisa la **Vista Previa** de los enunciados y gráficos generados.
4. Copia el código LaTeX o descarga el archivo `.tex`.
5. *Tip:* Súbelo a [Overleaf](https://www.overleaf.com) para obtener tu PDF final.

### Interfaz de Línea de Comandos (CLI)
Para generar una guía rápida desde la terminal:
```bash
python generador_examen.py --mru 2 --newton 1 --energia 2 --out examen_final.tex
```

## 📂 Estructura del Sistema
- `web_app.py` / `index.html`: Orquestador de la interfaz web y lógica de PyScript.
- `generador_examen.py`: Motor principal para ejecución vía CLI.
- `graph_tool/`:
    - `physic_calculator.py`: Motores de cálculo de cinemática.
    - `energy_calculator.py`: Lógica de energías y trabajo.
    - `force_calculator.py`: Resolución de sistemas dinámicos.
    - `class_graph.py`: Generador de representaciones visuales (Matplotlib).
- `data/ejercicios.json`: Banco de plantillas de enunciados parametrizables.
- `templates/`: Fragmentos de código LaTeX para ensamblaje dinámico.

## 🧪 Validación y Pruebas
El proyecto incluye una suite de pruebas unitarias para garantizar la precisión de los cálculos físicos:
```bash
python -m unittest discover tests
```

## 📈 Roadmap (Mejoras Futuras)
- [ ] **Patrón Strategy:** Refactorizar `class_graph.py` para desacoplar tipos de gráficos.
- [ ] **Validación de Modelos:** Implementar Pydantic para asegurar coherencia en datos físicos.
- [ ] **Internacionalización (i18n):** Soporte para enunciados en múltiples idiomas.
- [ ] **Dificultad Gradual:** Etiquetado de ejercicios por nivel (Fácil, Medio, Difícil).

## 📄 Licencia
Distribuido bajo la Licencia MIT. Consulta `LICENSE` para más información.
