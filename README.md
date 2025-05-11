# Sistema Experto Difuso para Perfiles de Inversión

Este proyecto implementa un Sistema Experto Difuso (SED) utilizando la librería `scikit-fuzzy` para determinar el perfil de un inversor (conservador, moderado o arriesgado) basado en diferentes variables de entrada.

## Características

- Evaluación difusa del perfil inversor utilizando el método Mamdani
- Variables de entrada:
  - Edad del inversor (joven, medio, mayor)
  - Nivel de ingresos mensuales (bajo, medio, alto)
  - Tolerancia al riesgo (baja, media, alta)
  - Horizonte de inversión (corto, medio, largo plazo)
- Variable de salida: perfil de inversor (conservador, moderado, arriesgado)
- Implementación de más de 20 reglas difusas
- Visualización de funciones de membresía
- Interfaz de consola para ingresar datos

## Requisitos

- Python 3.6 o superior
- Dependencias:
  - numpy
  - scipy
  - networkx
  - scikit-fuzzy
  - matplotlib

## Instalación

1. Clone este repositorio o descargue los archivos
2. **Se recomienda usar un entorno virtual**:

   ```bash
   # Crear un entorno virtual
   python -m venv venv

   # Activar el entorno virtual
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. Instale todas las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Ejecución del sistema principal

Para usar el sistema interactivo y evaluar perfiles de inversión:

```bash
python sistema_experto_inversor.py
```

Siga las instrucciones en pantalla para ingresar los datos del inversor:

- Edad (18-90 años)
- Ingresos mensuales (0-150,000)
- Tolerancia al riesgo (0-10)
- Horizonte de inversión (1-40 años)

### Ejecución de pruebas automáticas

Para ejecutar pruebas con casos predefinidos que cubren diferentes perfiles:

```bash
python test_perfiles_inversor.py
```

Este script ejecutará 10 casos de prueba que abarcan perfiles conservadores, moderados y arriesgados, incluyendo casos límite.

## Reglas del Sistema Experto

El sistema incluye más de 20 reglas difusas que evalúan todas las combinaciones relevantes de las variables de entrada. Algunas de las reglas más importantes son:

1. Si es joven, ingresos altos, tolerancia alta y horizonte largo, entonces perfil arriesgado
2. Si es mayor, ingresos bajos y tolerancia baja, entonces perfil conservador
3. Si es medio, ingresos medios y tolerancia media, entonces perfil moderado

## Ejemplo de uso

```
========================================================
   SISTEMA EXPERTO DIFUSO PARA PERFILES DE INVERSIÓN
========================================================

Ingrese los datos del inversor (o 'salir' para terminar):

- Edad (18-90 años): 35
- Ingresos mensuales (0-150,000): 70000
- Tolerancia al riesgo (0-10): 7
- Horizonte de inversión (1-40 años): 15

------------------------------------------------------------
Resultado del análisis para el inversor:
------------------------------------------------------------
Edad: 35 años
Ingresos mensuales: $70000
Tolerancia al riesgo: 7/10
Horizonte de inversión: 15 años
------------------------------------------------------------
Perfil del inversor: Moderado
Valor numérico: 55.63/100
```

## Personalización

Para modificar o ampliar las reglas del sistema, edite el método `definir_reglas()` en la clase `SistemaExpertoDifusoInversor`. Puede agregar nuevas reglas siguiendo el formato existente.

## Manejo de errores

El sistema incluye un mecanismo de respaldo para manejar casos donde la inferencia difusa podría fallar, asegurando que siempre se obtenga un perfil de inversor válido.

## Licencia

Este proyecto es de uso libre para fines educativos y académicos.
