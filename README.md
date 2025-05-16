# Sistema Experto Difuso para Perfiles de Inversión

Este proyecto implementa un Sistema Experto basado en Lógica Difusa (Fuzzy Logic) que determina el perfil de un inversor a partir de características personales como edad, nivel de ingresos, conocimiento financiero y tolerancia al riesgo. El sistema está implementado en Python utilizando la biblioteca scikit-fuzzy.

## Descripción

El sistema utiliza principios de lógica difusa para modelar el razonamiento humano en la clasificación de inversores. A diferencia de la lógica binaria tradicional (verdadero/falso), la lógica difusa permite el manejo de conceptos imprecisos como "joven", "ingresos altos" o "baja tolerancia al riesgo" mediante grados de pertenencia a conjuntos difusos.

## Estructura del Proyecto

El proyecto ha sido organizado de forma modular para facilitar su mantenimiento y comprensión:

- `main.py`: Punto de entrada principal del sistema. Contiene la función `ejecutar_sistema()` que gestiona la interacción con el usuario mediante una interfaz de consola.
- `sistema_experto.py`: Contiene la implementación principal del sistema experto difuso (`SistemaExpertoDifusoInversorFCL`) con todas las variables, funciones de membresía y reglas de inferencia.
- `visualizacion.py`: Módulo para la visualización de funciones de membresía y resultados de inferencia mediante gráficos.
- `utils.py`: Funciones de utilidad generales para el sistema.

## Variables de entrada

1. **Edad del inversor (20-100 años)**:

   - Joven: 20-40 años (pertenencia máxima entre 20-30)
   - Medio: 35-55 años (pertenencia máxima alrededor de 45)
   - Mayor: 50-100 años (pertenencia máxima a partir de 60)

2. **Ingresos mensuales (0-15,000 unidades monetarias)**:

   - Bajo: 0-2,000 (pertenencia máxima entre 0-1,000)
   - Medio: 1,500-4,500 (pertenencia máxima en 3,000)
   - Alto: 4,000-15,000 (pertenencia máxima a partir de 5,000)

3. **Conocimiento financiero (escala 0-10)**:

   - Bajo: 0-4 (pertenencia máxima entre 0-2)
   - Medio: 3-7 (pertenencia máxima en 5)
   - Alto: 6-10 (pertenencia máxima a partir de 8)

4. **Tolerancia al riesgo (escala 0-10)**:
   - Baja: 0-4 (pertenencia máxima entre 0-2)
   - Media: 3-7 (pertenencia máxima en 5)
   - Alta: 6-10 (pertenencia máxima a partir de 8)

## Variables intermedias

1. **Potencial de inversión (escala 0-10)**:

   - Bajo: 0-4
   - Medio: 3-7
   - Alto: 6-10

2. **Nivel de riesgo (escala 0-10)**:
   - Bajo: 0-4
   - Medio: 3-7
   - Alto: 6-10

## Variable de salida

**Perfil de inversor (escala 0-10)**:

- Conservador
- Moderado
- Agresivo

## Modelo de inferencia difusa

El sistema implementa 27 reglas de inferencia distribuidas en tres bloques:

1. **Bloque para calcular el potencial de inversión** (9 reglas)

   - Combina edad e ingresos para determinar el potencial económico del inversor
   - Ejemplo: "IF edad IS joven AND ingresos IS alto THEN potencial IS alto"

2. **Bloque para calcular el nivel de riesgo** (9 reglas)

   - Combina conocimiento financiero y tolerancia al riesgo
   - Ejemplo: "IF tolerancia IS bajo AND conocimiento IS alto THEN riesgo IS bajo"

3. **Bloque para determinar el perfil final del inversor** (9 reglas)
   - Combina potencial de inversión y nivel de riesgo
   - Ejemplo: "IF potencial IS alto AND riesgo IS alto THEN perfil_inversor IS agresivo"

## Requisitos

Para ejecutar el sistema se necesita:

- Python 3.10 o superior
- NumPy
- scikit-fuzzy
- Matplotlib

## Instalación

1. **Clone el repositorio o descargue los archivos del proyecto**

2. **Cree y active un entorno virtual (recomendado)**:

   ```bash
   # Crear el entorno virtual
   python -m venv .venv
   ```

   ```bash
   # Activar el entorno virtual en macOS/Linux
   source .venv/bin/activate
   ```

   ```bash
   # Activar el entorno virtual en Windows
   .\.venv\Scripts\activate

   ```

3. **Instale las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución y Uso

Para ejecutar el sistema, utilice:

```bash
python main.py
```

El programa solicitará los siguientes datos:

- Edad del inversor (entre 20 y 100 años)
- Ingresos mensuales (entre 1 y 15,000 unidades monetarias)
- Nivel de conocimiento financiero (entre 1 y 10)
- Tolerancia al riesgo (entre 1 y 10)

Después de procesar los datos, el sistema mostrará:

- El perfil del inversor determinado (Conservador, Moderado o Agresivo)
- El valor numérico del perfil en escala de 0-10
- El potencial de inversión calculado (0-10)
- El nivel de riesgo calculado (0-10)
- Opción para visualizar gráficamente las funciones de membresía y resultados de la inferencia

## Características principales

- Evaluación de perfiles de inversión basada en 4 variables de entrada
- Categorización en 3 perfiles de inversor: Conservador, Moderado y Agresivo
- Visualización de las funciones de membresía y resultados mediante gráficos
- Interfaz de usuario por consola, interactiva y amigable
- Sistema de respaldo basado en reglas heurísticas simplificadas

## Implementación técnica

El código está estructurado en clases modulares:

### Clase SistemaExpertoDifusoInversorFCL

- Definición de variables lingüísticas (Antecedentes y Consecuentes)
- Configuración de funciones de membresía triangulares (trimf) y trapezoidales (trapmf)
- Establecimiento de reglas difusas mediante operadores AND (&)
- Creación del sistema de control difuso y simulación
- Método `evaluar()` para procesar entradas y obtener el perfil resultante

### Clase VisualizadorSistemaExperto

- Visualización de todas las funciones de membresía del sistema
- Representación gráfica del proceso de defuzzificación
- Visualización de resultados con indicadores para los valores obtenidos

### Elementos clave del código

- **Inicialización**: Define los universos de discurso para cada variable.
- **Funciones de membresía**: Implementa las funciones de pertenencia usando trimf y trapmf.
- **Reglas difusas**: Crea 27 reglas usando el operador AND (&) entre condiciones.
- **Evaluación**: Método que valida entradas, ejecuta la inferencia difusa y devuelve los resultados.
- **Visualización**: Métodos para mostrar gráficamente las funciones de membresía y resultados.

### Manejo de errores

El sistema implementa un mecanismo robusto de manejo de errores:

- Validación de rango para todas las variables de entrada
- Manejo de errores durante la inferencia difusa con mecanismo de reglas por defecto
- Tratamiento de excepciones durante la visualización

## Visualización

El módulo de visualización (`visualizacion.py`) proporciona dos tipos principales de visualizaciones:

1. **Visualización de variables lingüísticas**: Muestra las funciones de membresía de todas las variables del sistema:

   - Variables de entrada: Edad, Ingresos, Conocimiento y Tolerancia
   - Variables intermedias: Potencial y Riesgo
   - Variable de salida: Perfil de inversor

2. **Visualización de resultados**: Muestra gráficamente el proceso de inferencia y los valores resultantes:
   - Gráfico del potencial de inversión inferido con valor numérico
   - Gráfico del nivel de riesgo inferido con valor numérico
   - Gráfico del perfil resultante con indicación del tipo (Conservador, Moderado o Agresivo)

## Ejemplos de perfiles

1. **Perfil Conservador**

   - Personas mayores (>60 años) con ingresos bajos/medios
   - Personas con bajo potencial de inversión independientemente del riesgo
   - Recomendable para inversores que priorizan la seguridad sobre la rentabilidad

2. **Perfil Moderado**

   - Personas con potencial medio y riesgo bajo/medio
   - Adultos con ingresos medios y conocimiento financiero medio
   - Balance entre seguridad y rentabilidad

3. **Perfil Agresivo**
   - Jóvenes con altos ingresos y alta tolerancia al riesgo
   - Personas con alto potencial de inversión y conocimiento financiero
   - Personas con potencial medio pero alto nivel de riesgo
   - Enfocado en maximizar la rentabilidad aceptando mayor volatilidad

## Referencias

El sistema está basado en los principios de la lógica difusa y utiliza conceptos de la teoría de conjuntos difusos desarrollada por Lotfi Zadeh. La implementación se apoya en la biblioteca scikit-fuzzy de Python.
