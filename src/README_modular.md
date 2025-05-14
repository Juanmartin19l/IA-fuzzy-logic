# Sistema Experto Difuso para Perfiles de Inversión

Este sistema utiliza lógica difusa (fuzzy logic) para determinar el perfil de un inversor basado en varios parámetros como edad, ingresos, conocimiento financiero y tolerancia al riesgo.

## Estructura del Proyecto

El proyecto ha sido organizado de forma modular para facilitar su mantenimiento y comprensión:

- `main.py`: Punto de entrada principal, contiene la función `ejecutar_sistema()` que orquesta la interacción con el usuario.
- `sistema_experto.py`: Contiene la implementación principal del sistema experto difuso (`SistemaExpertoDifusoInversorFCL`).
- `visualizacion.py`: Módulo para la visualización de funciones de membresía y resultados de inferencia.
- `utils.py`: Funciones de utilidad generales para el sistema.
- `perfil_inversor.py`: Archivo original mantenido por compatibilidad.
- `modular_main.py`: Punto de entrada alternativo que utiliza la estructura modularizada.

## Ejecución del Sistema

Para ejecutar el sistema, puedes usar cualquiera de estas opciones:

```bash
python main.py
# o
python modular_main.py
# o
python perfil_inversor.py
```

## Requisitos

Los requisitos del sistema están especificados en el archivo `requirements.txt`. Para instalarlos:

```bash
pip install -r requirements.txt
```

## Funcionalidades

El sistema implementa:

1. Evaluación del perfil de inversor mediante lógica difusa
2. Visualización de funciones de membresía
3. Visualización del proceso de inferencia
4. Recomendaciones personalizadas basadas en el perfil obtenido

## Perfiles de Inversor

El sistema determina entre 5 perfiles:

- Muy Conservador
- Conservador
- Moderado
- Agresivo
- Muy Agresivo

## Implementación

El sistema utiliza la biblioteca scikit-fuzzy para la implementación de lógica difusa y matplotlib para la visualización de resultados.
