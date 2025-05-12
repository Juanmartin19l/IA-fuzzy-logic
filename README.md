# Sistema Experto Difuso para Perfiles de Inversión

Este proyecto implementa un Sistema Experto Difuso (Fuzzy Logic) para determinar el perfil de un inversor basado en diferentes variables como edad, ingresos, tolerancia al riesgo y conocimiento financiero.

## Descripción

El sistema utiliza lógica difusa para clasificar a un inversor en uno de los siguientes perfiles:

- **Conservador**: Inversores con baja tolerancia al riesgo, generalmente enfocados en preservar capital.
- **Moderado**: Inversores que buscan un equilibrio entre rendimiento y seguridad.
- **Agresivo/Arriesgado**: Inversores dispuestos a asumir riesgos considerables para obtener mayores rendimientos.

## Implementaciones

El proyecto contiene dos implementaciones del sistema experto:

### 1. Sistema Experto Difuso en Python (scikit-fuzzy)

Implementado en el archivo `sistema_experto_inversor.py`. Esta implementación utiliza la biblioteca scikit-fuzzy para desarrollar el sistema de inferencia difusa Mamdani desde cero.

**Variables de entrada**:

- Edad del inversor (18-90 años)
- Ingresos mensuales (0-150,000)
- Tolerancia al riesgo (0-10)
- Horizonte de inversión (1-40 años)

**Variable de salida**:

- Perfil de inversión (0-100, clasificado como Conservador, Moderado o Arriesgado)

### 2. Implementación Python del archivo FCL

Implementado en el archivo `perfil_inversor.py`. Esta versión es una traducción a Python del archivo de Control de Lógica Difusa (FCL) `inv.fcl`, que define otro sistema experto difuso similar.

**Variables de entrada**:

- Edad del inversor (18-100 años)
- Ingresos mensuales (0-15,000)
- Conocimiento financiero (0-10)
- Tolerancia al riesgo (0-10)

**Variables de salida**:

- Potencial de inversión (0-10)
- Riesgo (0-10)
- Perfil de inversión (0-3, clasificado como Conservador, Moderado o Agresivo)

## Archivos del proyecto

- `sistema_experto_inversor.py`: Implementación principal del sistema experto en Python
- `perfil_inversor.py`: Implementación Python del archivo FCL
- `inv.fcl`: Archivo de Control de Lógica Difusa (Fuzzy Control Language)
- `test_perfiles_inversor.py`: Tests para la primera implementación
- `test_perfil_inversor_fcl.py`: Tests para la implementación basada en FCL
- `requirements.txt`: Dependencias del proyecto

## Requisitos

- Python 3.6 o superior
- Dependencias:
  - numpy >= 1.20.0
  - scikit-fuzzy >= 0.4.2
  - scipy >= 1.7.0
  - matplotlib >= 3.4.0
  - networkx >= 2.6.0

## Instalación

1. Clonar este repositorio
2. Crear un entorno virtual:
   ```
   python -m venv .venv
   ```
3. Activar el entorno virtual:

   ```
   # En Windows
   .venv\Scripts\activate

   # En macOS/Linux
   source .venv/bin/activate
   ```

4. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

### Ejecutar el sistema experto principal:

```
python sistema_experto_inversor.py
```

Siga las instrucciones en pantalla para ingresar los datos del inversor:

- Edad (18-90 años)
- Ingresos mensuales (0-150,000)
- Tolerancia al riesgo (0-10)
- Horizonte de inversión (1-40 años)

### Ejecutar el sistema experto basado en FCL:

```
python perfil_inversor.py
```

Siga las instrucciones para ingresar:

- Edad (18-100 años)
- Ingresos mensuales (0-15,000)
- Conocimiento financiero (0-10)
- Tolerancia al riesgo (0-10)

### Ejecutar los tests:

```
# Tests para el sistema experto principal
python test_perfiles_inversor.py

# Tests para la implementación FCL (con gráficas)
python test_perfil_inversor_fcl.py --graficas
```

Los tests ejecutarán varios casos de prueba que abarcan perfiles conservadores, moderados y arriesgados/agresivos, incluyendo casos límite.

## Funcionamiento del Sistema

Los sistemas expertos difusos utilizan conjuntos difusos y reglas lingüísticas para modelar el proceso de toma de decisiones. En este caso:

1. Se definen conjuntos difusos para variables como edad, ingresos, tolerancia al riesgo, etc.
2. Se establecen reglas tipo: "Si la edad es mayor Y la tolerancia al riesgo es baja, ENTONCES el perfil es conservador"
3. Se aplica el proceso de inferencia difusa (Mamdani)
4. Se obtiene un valor numérico que se traduce a un perfil lingüístico (conservador, moderado o agresivo/arriesgado)

### Reglas del Sistema Experto Principal

El sistema incluye más de 20 reglas difusas que evalúan todas las combinaciones relevantes de las variables de entrada. Algunas de las reglas más importantes son:

1. Si es joven, ingresos altos, tolerancia alta y horizonte largo, entonces perfil arriesgado
2. Si es mayor, ingresos bajos y tolerancia baja, entonces perfil conservador
3. Si es medio, ingresos medios y tolerancia media, entonces perfil moderado

### Reglas del Sistema FCL

El sistema basado en FCL implementa un enfoque de dos niveles:

1. Primero evalúa el potencial de inversión basado en edad e ingresos
2. Luego evalúa el riesgo basado en conocimiento y tolerancia
3. Finalmente, combina ambos para determinar el perfil del inversor

## Ejemplos de uso

### Sistema Experto Principal

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

### Sistema basado en FCL

```
============================================================
   SISTEMA EXPERTO DIFUSO PARA PERFILES DE INVERSIÓN
   Implementación Python del archivo FCL
============================================================

Ingrese los datos del inversor (o 'salir' para terminar):

- Edad (18-100 años): 30
- Ingresos mensuales (0-15,000): 6000
- Conocimiento financiero (0-10): 7
- Tolerancia al riesgo (0-10): 8

------------------------------------------------------------
Resultado del análisis para el inversor:
------------------------------------------------------------
Edad: 30 años
Ingresos mensuales: $6000
Conocimiento financiero: 7.0/10
Tolerancia al riesgo: 8.0/10
------------------------------------------------------------
Potencial de inversión: 8.25/10
Nivel de riesgo: 5.75/10
Perfil del inversor: Agresivo
Valor numérico: 2.45/3
```

## Personalización

Para modificar o ampliar las reglas del sistema:

- En `sistema_experto_inversor.py`: edite el método `definir_reglas()` en la clase `SistemaExpertoDifusoInversor`
- En `perfil_inversor.py`: edite el método `definir_reglas()` en la clase `SistemaExpertoDifusoInversorFCL`
- En `inv.fcl`: modifique las reglas en los RULEBLOCK

## Manejo de errores

Ambos sistemas incluyen mecanismos de respaldo para manejar casos donde la inferencia difusa podría fallar, asegurando que siempre se obtenga un perfil de inversor válido.

## Licencia

Este proyecto está licenciado bajo la licencia MIT.
