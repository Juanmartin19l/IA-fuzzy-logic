"""
Sistema Experto Difuso para determinar el perfil de un inversor
Implementación en Python del archivo FCL (Fuzzy Control Language)
"""

import numpy as np
from skfuzzy import control as ctrl
import skfuzzy as fuzz


class SistemaExpertoDifusoInversorFCL:
    """
    Sistema Experto Difuso para determinar el perfil de un inversor basado en:
    - Edad del inversor
    - Nivel de ingresos
    - Conocimiento financiero
    - Tolerancia al riesgo

    Implementación basada en el archivo FCL 'inv.fcl'
    """

    def __init__(self):
        """Inicializa el sistema experto difuso con todas las variables y reglas necesarias."""
        # Definir variables de entrada (universos de discurso)
        self.edad = ctrl.Antecedent(np.arange(20, 101, 1), "edad")
        self.ingresos = ctrl.Antecedent(np.arange(0, 15001, 100), "ingresos")
        self.conocimiento = ctrl.Antecedent(np.arange(0, 11, 1), "conocimiento")
        self.tolerancia = ctrl.Antecedent(np.arange(0, 11, 1), "tolerancia")

        # Definir variables de salida
        # El método de defuzzificación por centro de gravedad (centroid) calcula la abscisa (valor x)
        # del centro de masa del conjunto difuso resultante.
        # Por defecto, scikit-fuzzy utiliza este método por ser preciso y consistente
        self.potencial = ctrl.Consequent(np.arange(0, 11, 0.1), "potencial")
        self.riesgo = ctrl.Consequent(np.arange(0, 11, 0.1), "riesgo")
        self.perfil_inversor = ctrl.Consequent(np.arange(0, 11, 0.1), "perfil_inversor")

        # Definir las funciones de pertenencia para cada variable
        self.definir_funciones_membresia()

        # Definir reglas del sistema
        self.reglas = self.definir_reglas()

        # Crear sistemas de control para cada bloque de reglas
        try:
            self.sistema_ctrl = ctrl.ControlSystem(self.reglas)
            self.simulacion = ctrl.ControlSystemSimulation(self.sistema_ctrl)
        except Exception as e:
            print(f"Error al crear el sistema de control: {e}")

    def definir_funciones_membresia(self):
        """
        Define las funciones de membresía para todas las variables lingüísticas del sistema.

        Implementa funciones triangulares (trimf) y trapezoidales (trapmf) para modelar
        los conjuntos difusos correspondientes a cada término lingüístico.
        """
        # Funciones de membresía para variable EDAD
        self.edad["joven"] = fuzz.trapmf(
            self.edad.universe, [20, 20, 30, 40]
        )  # Hasta 40 años
        self.edad["medio"] = fuzz.trimf(
            self.edad.universe, [35, 45, 55]
        )  # Entre 35 y 55
        self.edad["mayor"] = fuzz.trapmf(
            self.edad.universe, [50, 60, 100, 100]
        )  # Desde 50

        # Funciones de membresía para variable INGRESOS (en unidades monetarias)
        self.ingresos["bajo"] = fuzz.trapmf(self.ingresos.universe, [0, 0, 1000, 2000])
        self.ingresos["medio"] = fuzz.trimf(self.ingresos.universe, [1500, 3000, 4500])
        self.ingresos["alto"] = fuzz.trapmf(
            self.ingresos.universe, [4000, 5000, 15000, 15000]
        )

        # Funciones de membresía para variable CONOCIMIENTO (escala 0-10)
        self.conocimiento["bajo"] = fuzz.trapmf(
            self.conocimiento.universe, [0, 0, 2, 4]
        )
        self.conocimiento["medio"] = fuzz.trimf(self.conocimiento.universe, [3, 5, 7])
        self.conocimiento["alto"] = fuzz.trapmf(
            self.conocimiento.universe, [6, 8, 10, 10]
        )

        # Funciones de membresía para variable TOLERANCIA AL RIESGO (escala 0-10)
        self.tolerancia["bajo"] = fuzz.trapmf(self.tolerancia.universe, [0, 0, 2, 4])
        self.tolerancia["medio"] = fuzz.trimf(self.tolerancia.universe, [3, 5, 7])
        self.tolerancia["alto"] = fuzz.trapmf(self.tolerancia.universe, [6, 8, 10, 10])

        # Funciones de membresía para variable POTENCIAL DE INVERSIÓN (escala 0-10)
        self.potencial["bajo"] = fuzz.trapmf(self.potencial.universe, [0, 0, 2, 4])
        self.potencial["medio"] = fuzz.trimf(self.potencial.universe, [3, 5, 7])
        self.potencial["alto"] = fuzz.trapmf(self.potencial.universe, [6, 8, 10, 10])

        # Funciones de membresía para variable RIESGO (escala 0-10)
        self.riesgo["bajo"] = fuzz.trapmf(self.riesgo.universe, [0, 0, 2, 4])
        self.riesgo["medio"] = fuzz.trimf(self.riesgo.universe, [3, 5, 7])
        self.riesgo["alto"] = fuzz.trapmf(self.riesgo.universe, [6, 8, 10, 10])

        # Funciones de membresía para variable PERFIL INVERSOR (escala 0-10)
        self.perfil_inversor["conservador"] = fuzz.trapmf(
            self.perfil_inversor.universe, [0, 0, 2.5, 4.5]
        )
        self.perfil_inversor["moderado"] = fuzz.trimf(
            self.perfil_inversor.universe, [3.5, 5, 7.5]
        )

        self.perfil_inversor["agresivo"] = fuzz.trapmf(
            self.perfil_inversor.universe, [6.5, 8.5, 10, 10]
        )

    def definir_reglas(self):
        """
        Define el conjunto de reglas difusas para el sistema según las tablas de decisión.

        Returns:
            list: Lista de reglas de inferencia usando operadores AND (&)
        """
        reglas = []

        # ----- Bloque 1: Reglas para determinar el potencial de inversión -----
        # Basadas en la edad y nivel de ingresos del inversor

        # Reglas para edad joven
        reglas.append(
            ctrl.Rule(
                self.edad["joven"] & self.ingresos["bajo"], self.potencial["bajo"]
            )
        )
        reglas.append(
            ctrl.Rule(
                self.edad["joven"] & self.ingresos["medio"], self.potencial["medio"]
            )
        )
        reglas.append(
            ctrl.Rule(
                self.edad["joven"] & self.ingresos["alto"], self.potencial["alto"]
            )
        )

        # Reglas para edad medio
        reglas.append(
            ctrl.Rule(
                self.edad["medio"] & self.ingresos["bajo"], self.potencial["bajo"]
            )
        )
        reglas.append(
            ctrl.Rule(
                self.edad["medio"] & self.ingresos["medio"], self.potencial["medio"]
            )
        )
        reglas.append(
            ctrl.Rule(
                self.edad["medio"] & self.ingresos["alto"], self.potencial["alto"]
            )
        )

        # Reglas para edad mayor
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"] & self.ingresos["bajo"], self.potencial["bajo"]
            )
        )
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"] & self.ingresos["medio"], self.potencial["bajo"]
            )
        )
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"] & self.ingresos["alto"], self.potencial["medio"]
            )
        )

        # ----- Bloque 2: Reglas para determinar el nivel de riesgo -----
        # Basadas en el conocimiento financiero y tolerancia al riesgo

        # Reglas para tolerancia bajo
        reglas.append(
            ctrl.Rule(
                self.tolerancia["bajo"] & self.conocimiento["bajo"],
                self.riesgo["medio"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.tolerancia["bajo"] & self.conocimiento["medio"],
                self.riesgo["bajo"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.tolerancia["bajo"] & self.conocimiento["alto"], self.riesgo["bajo"]
            )
        )

        # Reglas para tolerancia medio
        reglas.append(
            ctrl.Rule(
                self.tolerancia["medio"] & self.conocimiento["bajo"],
                self.riesgo["alto"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.tolerancia["medio"] & self.conocimiento["medio"],
                self.riesgo["medio"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.tolerancia["medio"] & self.conocimiento["alto"],
                self.riesgo["medio"],
            )
        )

        # Reglas para tolerancia alto
        reglas.append(
            ctrl.Rule(
                self.tolerancia["alto"] & self.conocimiento["bajo"], self.riesgo["alto"]
            )
        )
        reglas.append(
            ctrl.Rule(
                self.tolerancia["alto"] & self.conocimiento["medio"],
                self.riesgo["alto"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.tolerancia["alto"] & self.conocimiento["alto"],
                self.riesgo["medio"],
            )
        )

        # ----- Bloque 3: Reglas finales para determinar el perfil de inversor -----
        # Basadas en potencial de inversión y nivel de riesgo

        # Reglas para potencial bajo
        reglas.append(
            ctrl.Rule(
                self.potencial["bajo"] & self.riesgo["bajo"],
                self.perfil_inversor["conservador"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.potencial["bajo"] & self.riesgo["medio"],
                self.perfil_inversor["conservador"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.potencial["bajo"] & self.riesgo["alto"],
                self.perfil_inversor["conservador"],
            )
        )

        # Reglas para potencial medio
        reglas.append(
            ctrl.Rule(
                self.potencial["medio"] & self.riesgo["bajo"],
                self.perfil_inversor["moderado"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.potencial["medio"] & self.riesgo["medio"],
                self.perfil_inversor["moderado"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.potencial["medio"] & self.riesgo["alto"],
                self.perfil_inversor["agresivo"],
            )
        )

        # Reglas para potencial alto
        reglas.append(
            ctrl.Rule(
                self.potencial["alto"] & self.riesgo["bajo"],
                self.perfil_inversor["moderado"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.potencial["alto"] & self.riesgo["medio"],
                self.perfil_inversor["agresivo"],
            )
        )
        reglas.append(
            ctrl.Rule(
                self.potencial["alto"] & self.riesgo["alto"],
                self.perfil_inversor["agresivo"],
            )
        )

        return reglas

    def evaluar(self, edad, ingresos, conocimiento, tolerancia):
        """
        Evalúa el perfil de inversión con los valores dados aplicando inferencia difusa.

        Args:
            edad (int): Edad del inversor (20-100 años)
            ingresos (int): Ingresos mensuales (1-15,000 unidades monetarias)
            conocimiento (float): Nivel de conocimiento financiero (escala 1-10)
            tolerancia (float): Tolerancia al riesgo (escala 1-10)

        Returns:
            dict: Diccionario con los resultados de la evaluación:
                - perfil (str): Descripción lingüística del perfil ("Conservador", "Moderado", "Agresivo")
                - valor_perfil (float): Valor numérico del perfil en escala 0-10
                - potencial (float): Valor numérico del potencial de inversión en escala 0-10
                - riesgo (float): Valor numérico del nivel de riesgo en escala 0-10

        Raises:
            ValueError: Si algún parámetro está fuera de los rangos permitidos
        """
        # Validación de parámetros de entrada
        if not (20 <= edad <= 100):
            raise ValueError("La edad debe estar entre 20 y 100 años")
        if not (1 <= ingresos <= 15000):
            raise ValueError("Los ingresos deben estar entre 1 y 15,000")
        if not (1 <= conocimiento <= 10):
            raise ValueError("El conocimiento financiero debe estar entre 1 y 10")
        if not (1 <= tolerancia <= 10):
            raise ValueError("La tolerancia al riesgo debe estar entre 1 y 10")

        try:
            # Asignar valores a las variables de entrada
            self.simulacion.input["edad"] = edad
            self.simulacion.input["ingresos"] = ingresos
            self.simulacion.input["conocimiento"] = conocimiento
            self.simulacion.input["tolerancia"] = tolerancia

            # Ejecutar el sistema de inferencia difusa
            self.simulacion.compute()

            # Obtener resultados
            valor_potencial = self.simulacion.output["potencial"]
            valor_riesgo = self.simulacion.output["riesgo"]
            valor_perfil = self.simulacion.output["perfil_inversor"]

            # Preparar diccionario de resultados
            resultados = {
                "valor_perfil": valor_perfil,
                "potencial": valor_potencial,
                "riesgo": valor_riesgo,
            }

            return resultados

        except Exception as e:
            raise Exception(f"Error en la evaluación del perfil: {str(e)}")
